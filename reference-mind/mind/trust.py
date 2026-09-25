"""The trust root: everything that must live OUTSIDE the data directory (BUILD ROUND: MC6, MC16, MC17, MC18).

    <trust dir>/secrets/*          32-byte keys (0600): ticket-verifier HMAC key, lineage MAC key, per-user data keys
    <trust dir>/credentials.json   enrolled credentials (public keys, or HMAC key ids) per party
    <trust dir>/authenticator/*    SoftAuthenticator private keys  -- TEST DOUBLE, see below
    <trust dir>/anchor.jsonl       FileAnchor: append-only, hash-chained anchor log (stand-in for a transparency log)
    <trust dir>/tiers.json         the signed tool-tier registry (tiers.py)

Default location: a sibling of the data dir (`<data>.trust`), or $MIND_TRUST_DIR.  The point of the split is that
read or write access to the data directory (charter.db, lineage.jsonl, memory.db, audit.jsonl) is not enough to forge
a consent, recover a removal phrase, or delete the seed without it showing.  Someone who controls BOTH directories
(and the anchor) controls this mind; that residual is stated in BUILD-ROUND.md.

What is a test double here, honestly:
  * SoftAuthenticator stands in for WebAuthn/passkeys (MC17).  It signs challenges with a per-party key kept in the
    trust dir.  It has NO user-presence check, NO origin binding and NO attestation.  The Authenticator interface
    is what a real WebAuthn/passkey bridge must implement.
  * FileAnchor / MemoryAnchor stand in for an external transparency log (MC6/MC16).  A real deployment publishes the
    same records to a log the operator cannot rewrite (e.g. a witnessed Merkle log).
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import secrets
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from . import crypto

GENESIS = "0" * 64


class TrustError(Exception):
    pass


def _canon(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _write_private(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".{secrets.token_hex(4)}.tmp")
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)
    try:
        os.link(str(tmp), str(path))  # never overwrite an existing key (first writer wins)
    except FileExistsError:
        pass
    finally:
        tmp.unlink(missing_ok=True)


class SecretStore:
    """Named 32-byte secrets, created on first use.  Never stored in any database."""

    def __init__(self, directory: Path):
        self.dir = Path(directory)
        self._cache: dict[str, bytes] = {}
        self._lock = threading.Lock()

    def _path(self, name: str) -> Path:
        return self.dir / (re.sub(r"[^A-Za-z0-9_.-]", "_", name) + ".key")

    def get(self, name: str, create: bool = True) -> bytes:
        with self._lock:
            if name in self._cache:
                return self._cache[name]
            p = self._path(name)
            if not p.exists():
                if not create:
                    raise TrustError(f"secret {name!r} does not exist")
                self.dir.mkdir(parents=True, exist_ok=True)
                os.chmod(self.dir, 0o700)
                _write_private(p, secrets.token_bytes(32))
            raw = p.read_bytes()
            if len(raw) != 32:
                raise TrustError(f"secret {name!r} is corrupt")
            self._cache[name] = raw
            return raw


# --------------------------------------------------------------------------------------------------
# Anchors (external heads)
# --------------------------------------------------------------------------------------------------
class AnchorLog(ABC):
    """Interface for an external, append-only record of heads and published hashes."""

    @abstractmethod
    def publish(self, stream: str, record: dict[str, Any]) -> dict[str, Any]: ...

    @abstractmethod
    def entries(self, stream: str | None = None) -> list[dict[str, Any]]: ...

    def latest(self, stream: str) -> dict[str, Any] | None:
        items = self.entries(stream)
        return items[-1] if items else None

    def verify(self) -> tuple[bool, str]:
        return True, "ok"


class MemoryAnchor(AnchorLog):
    """Test double: an in-process anchor that nobody else can touch."""

    def __init__(self) -> None:
        self._items: list[dict[str, Any]] = []
        self._lock = threading.Lock()

    def publish(self, stream: str, record: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            e = {"stream": stream, "ts": round(time.time(), 3), **record}
            self._items.append(e)
            return e

    def entries(self, stream: str | None = None) -> list[dict[str, Any]]:
        return [dict(e) for e in self._items if stream is None or e["stream"] == stream]


class FileAnchor(AnchorLog):
    """Append-only, hash-chained JSONL.  Opened only in append mode; a broken chain raises on read (fail closed)."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self._lock = threading.Lock()

    def publish(self, stream: str, record: dict[str, Any]) -> dict[str, Any]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock, open(self.path, "a+b") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            try:
                fh.seek(0)
                lines = [ln for ln in fh.read().split(b"\n") if ln.strip()]
                prev = json.loads(lines[-1])["hash"] if lines else GENESIS
                body = {"stream": stream, "seq": len(lines) + 1, "ts": round(time.time(), 3), **record}
                entry = {**body, "prev": prev, "hash": hashlib.sha256(prev.encode() + _canon(body)).hexdigest()}
                fh.seek(0, 2)
                fh.write(_canon(entry) + b"\n")
                fh.flush()
                os.fsync(fh.fileno())
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)
        return entry

    def _all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        out, prev = [], GENESIS
        for i, line in enumerate(self.path.read_bytes().split(b"\n")):
            if not line.strip():
                continue
            try:
                e = json.loads(line)
            except ValueError as exc:
                raise TrustError(f"anchor log line {i + 1} unparseable") from exc
            body = {k: v for k, v in e.items() if k not in ("prev", "hash")}
            if e.get("prev") != prev or hashlib.sha256(prev.encode() + _canon(body)).hexdigest() != e.get("hash"):
                raise TrustError(f"anchor log chain broken at line {i + 1}")
            prev = e["hash"]
            out.append(e)
        return out

    def entries(self, stream: str | None = None) -> list[dict[str, Any]]:
        return [e for e in self._all() if stream is None or e["stream"] == stream]

    def verify(self) -> tuple[bool, str]:
        try:
            n = len(self._all())
        except TrustError as exc:
            return False, str(exc)
        return True, f"ok ({n} anchor entries)"


# --------------------------------------------------------------------------------------------------
# Credentials and authenticators (MC17)
# --------------------------------------------------------------------------------------------------
@dataclass
class Credential:
    party: str
    credential_id: str
    alg: str
    public: str  # ed25519 public key hex, or the hmac key id


@dataclass
class Assertion:
    party: str
    credential_id: str
    alg: str
    challenge: str  # hex
    signature: str  # hex

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Assertion":
        return cls(**{k: str(d.get(k, "")) for k in ("party", "credential_id", "alg", "challenge", "signature")})


class Authenticator(ABC):
    """What a WebAuthn/passkey bridge must provide.  get_assertion must require the party's presence."""

    @abstractmethod
    def enroll(self, party: str) -> Credential: ...

    @abstractmethod
    def get_assertion(self, party: str, challenge: bytes) -> Assertion: ...


class CredentialRegistry:
    """Enrolled credentials, in the trust dir; each enrolment is anchored so a swapped key is visible."""

    def __init__(self, path: Path, anchor: AnchorLog, secrets_store: SecretStore):
        self.path = Path(path)
        self.anchor = anchor
        self.secrets = secrets_store
        self._lock = threading.Lock()

    def _load(self) -> dict[str, dict[str, str]]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def get(self, party: str) -> Credential | None:
        d = self._load().get(party)
        return Credential(**d) if d else None

    def register(self, cred: Credential) -> Credential:
        with self._lock:
            data = self._load()
            if cred.party in data and data[cred.party]["public"] != cred.public:
                raise TrustError(f"party {cred.party!r} already has a different credential; re-enrolment is a "
                                 f"recorded procedure, not an overwrite")
            data[cred.party] = asdict(cred)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, indent=1, sort_keys=True), encoding="utf-8")
            os.replace(tmp, self.path)
            self.anchor.publish("credentials", {"party": cred.party, "credential_id": cred.credential_id,
                                                "alg": cred.alg, "public_sha": hashlib.sha256(cred.public.encode()).hexdigest()})
            return cred

    def verify(self, assertion: Assertion | None, challenge: bytes, party: str | None = None) -> tuple[bool, str]:
        if not isinstance(assertion, Assertion):
            return False, "no authenticator assertion (a name string is not authentication)"
        if party is not None and assertion.party != party:
            return False, f"assertion is by {assertion.party!r}, the ticket is bound to {party!r}"
        if assertion.challenge != challenge.hex():
            return False, "assertion is for a different challenge"
        cred = self.get(assertion.party)
        if cred is None or cred.credential_id != assertion.credential_id or cred.alg != assertion.alg:
            return False, f"no enrolled credential {assertion.credential_id!r} for {assertion.party!r}"
        anchored = [e for e in self.anchor.entries("credentials") if e.get("party") == cred.party]
        if not anchored or anchored[-1].get("public_sha") != hashlib.sha256(cred.public.encode()).hexdigest():
            return False, "credential is not the anchored one (credential file edited?)"
        secret = self.secrets.get(f"cred-{cred.credential_id}", create=False) if cred.alg == "hmac-sha256" else None
        ok = crypto.verify_signature(cred.alg, cred.public, challenge, assertion.signature, secret)
        return (True, "ok") if ok else (False, "signature does not verify")


class SoftAuthenticator(Authenticator):
    """TEST DOUBLE for a passkey/WebAuthn authenticator.  NOT a security boundary: no presence, origin or attestation."""

    def __init__(self, trust: "Trust"):
        self.trust = trust
        self.dir = trust.dir / "authenticator"

    def _key_path(self, party: str) -> Path:
        return self.dir / (hashlib.sha256(party.encode()).hexdigest()[:24] + ".json")

    def enroll(self, party: str) -> Credential:
        existing = self.trust.credentials.get(party)
        if existing is not None and self._key_path(party).exists():
            return existing
        alg = crypto.signature_alg()
        private, public = crypto.new_signing_key(alg)
        cid = secrets.token_hex(16)
        if alg == "hmac-sha256":
            _write_private(self.trust.secrets._path(f"cred-{cid}"), private)
        _write_private(self._key_path(party), _canon({"party": party, "credential_id": cid, "alg": alg,
                                                        "private": private.hex(), "public": public}))
        return self.trust.credentials.register(Credential(party, cid, alg, public))

    def get_assertion(self, party: str, challenge: bytes) -> Assertion:
        p = self._key_path(party)
        if not p.exists():
            raise TrustError(f"{party!r} is not enrolled on this authenticator")
        k = json.loads(p.read_text(encoding="utf-8"))
        sig = crypto.sign(k["alg"], bytes.fromhex(k["private"]), challenge)
        return Assertion(party, k["credential_id"], k["alg"], challenge.hex(), sig)


# --------------------------------------------------------------------------------------------------
class Trust:
    """Bundle: secrets + anchor + credentials rooted at one directory outside the data dir."""

    def __init__(self, directory: Path, anchor: AnchorLog | None = None):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.dir, 0o700)
        except OSError:
            pass
        self.secrets = SecretStore(self.dir / "secrets")
        self.anchor = anchor if anchor is not None else FileAnchor(self.dir / "anchor.jsonl")
        self.credentials = CredentialRegistry(self.dir / "credentials.json", self.anchor, self.secrets)

    @staticmethod
    def default_dir(data_dir: Path) -> Path:
        env = os.environ.get("MIND_TRUST_DIR")
        if env:
            return Path(env)
        data_dir = Path(data_dir).resolve()
        return data_dir.parent / (data_dir.name + ".trust")

    @classmethod
    def for_data_dir(cls, data_dir: Path) -> "Trust":
        return cls(cls.default_dir(data_dir))

    def mac(self, key_name: str, obj: Any) -> str:
        return crypto.mac_hex(self.secrets.get(key_name), _canon(obj))

    def mac_ok(self, key_name: str, obj: Any, tag: str) -> bool:
        return crypto.mac_ok(self.secrets.get(key_name), _canon(obj), tag)


def canon(obj: Any) -> bytes:
    return _canon(obj)
