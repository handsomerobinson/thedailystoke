"""Cryptographic primitives, with NO hand-rolled crypto (BUILD ROUND, MC6/MC16).

The standard library has hashing and HMAC but no AEAD cipher and no public-key signatures.  This module therefore:

  * uses `hmac`/`hashlib`/`secrets` from the stdlib for MACs, verifiers and nonces;
  * uses the vetted `cryptography` package, IF it is installed, for Ed25519 signatures and AES-256-GCM;
  * otherwise falls back to HMAC-SHA256 "signatures" (symmetric: the verifier holds the same key, kept outside the
    database, in the trust directory) and REFUSES to run encrypted-at-rest mode.  It never implements a cipher or a
    signature scheme itself.

`HAVE_CRYPTOGRAPHY` says which world you are in; `mind status` prints it.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
from abc import ABC, abstractmethod

def _import_cryptography():
    """Import the optional `cryptography` package.  A broken install (e.g. a Rust panic because _cffi_backend is
    missing) must read as 'absent', silently: fd 2 is muted during the attempt because pyo3 writes there directly."""
    saved = None
    try:
        saved = os.dup(2)
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 2)
        os.close(devnull)
    except OSError:
        saved = None
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        return InvalidSignature, serialization, Ed25519PrivateKey, Ed25519PublicKey, AESGCM
    except BaseException:  # noqa: BLE001 - ImportError, or a pyo3 PanicException (a BaseException)
        return None
    finally:
        if saved is not None:
            os.dup2(saved, 2)
            os.close(saved)


_mods = None if os.environ.get("MIND_NO_CRYPTOGRAPHY") == "1" else _import_cryptography()
HAVE_CRYPTOGRAPHY = _mods is not None
if HAVE_CRYPTOGRAPHY:
    _InvalidSignature, _ser, Ed25519PrivateKey, Ed25519PublicKey, AESGCM = _mods


def crypto_available() -> bool:
    """Indirection so tests can simulate a host without `cryptography` (MIND_SIMULATE_NO_CRYPTOGRAPHY=1)."""
    return HAVE_CRYPTOGRAPHY and os.environ.get("MIND_SIMULATE_NO_CRYPTOGRAPHY") != "1"


def mac_hex(key: bytes, data: bytes) -> str:
    return hmac.new(key, data, hashlib.sha256).hexdigest()


def mac_ok(key: bytes, data: bytes, tag: str) -> bool:
    return hmac.compare_digest(mac_hex(key, data), str(tag or ""))


# --------------------------------------------------------------------------------------------------
# Signatures (credential keys held by an authenticator)
# --------------------------------------------------------------------------------------------------
def signature_alg() -> str:
    return "ed25519" if crypto_available() else "hmac-sha256"


def new_signing_key(alg: str) -> tuple[bytes, str]:
    """Returns (private key bytes, public credential hex).  For hmac-sha256 the 'public' part is only a key id."""
    if alg == "ed25519":
        if not crypto_available():
            raise RuntimeError("ed25519 needs the `cryptography` package")
        sk = Ed25519PrivateKey.generate()
        raw = sk.private_bytes(_ser.Encoding.Raw, _ser.PrivateFormat.Raw, _ser.NoEncryption())
        pub = sk.public_key().public_bytes(_ser.Encoding.Raw, _ser.PublicFormat.Raw)
        return raw, pub.hex()
    if alg == "hmac-sha256":
        raw = secrets.token_bytes(32)
        return raw, hashlib.sha256(b"key-id:" + raw).hexdigest()
    raise ValueError(f"unknown signature algorithm {alg!r}")


def sign(alg: str, private: bytes, message: bytes) -> str:
    if alg == "ed25519":
        return Ed25519PrivateKey.from_private_bytes(private).sign(message).hex()
    if alg == "hmac-sha256":
        return mac_hex(private, message)
    raise ValueError(f"unknown signature algorithm {alg!r}")


def verify_signature(alg: str, public_hex: str, message: bytes, signature_hex: str, secret: bytes | None = None) -> bool:
    """Ed25519: verify with the public key.  hmac-sha256: needs the shared secret (kept in the trust directory)."""
    try:
        if alg == "ed25519":
            if not HAVE_CRYPTOGRAPHY:
                return False
            Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_hex)).verify(bytes.fromhex(signature_hex), message)
            return True
        if alg == "hmac-sha256":
            if secret is None or hashlib.sha256(b"key-id:" + secret).hexdigest() != public_hex:
                return False
            return mac_ok(secret, message, signature_hex)
    except (_InvalidSignature if HAVE_CRYPTOGRAPHY else ValueError, ValueError, TypeError):
        return False
    return False


# --------------------------------------------------------------------------------------------------
# At-rest encryption (MC6): pluggable, and refuses to pretend
# --------------------------------------------------------------------------------------------------
class EncryptionUnavailable(RuntimeError):
    pass


class Cipher(ABC):
    name = "cipher"
    encrypted = False

    @abstractmethod
    def encrypt(self, plaintext: str, aad: str = "") -> str: ...

    @abstractmethod
    def decrypt(self, token: str, aad: str = "") -> str: ...

    def tag(self, text: str) -> str:
        """Deterministic tag for equality (dedupe) without storing plaintext."""
        return text


class PlaintextCipher(Cipher):
    """The default: NOT encrypted.  Named honestly so `mind status` can say so."""
    name = "plaintext (NOT encrypted at rest)"

    def encrypt(self, plaintext: str, aad: str = "") -> str:
        return plaintext

    def decrypt(self, token: str, aad: str = "") -> str:
        return token


class AESGCMCipher(Cipher):
    """AES-256-GCM from the `cryptography` package (vetted).  Tokens are 'v1:' + base64(nonce || ciphertext+tag)."""
    name = "aes-256-gcm (cryptography)"
    encrypted = True

    def __init__(self, key: bytes, tag_key: bytes):
        if not crypto_available():
            raise EncryptionUnavailable("encrypted mode needs the vetted `cryptography` package; this build will not "
                                        "hand-roll a cipher. Install it (pip install cryptography) or run unencrypted.")
        if len(key) != 32:
            raise ValueError("AES-256-GCM needs a 32-byte key")
        self._aead = AESGCM(key)
        self._tag_key = tag_key

    def encrypt(self, plaintext: str, aad: str = "") -> str:
        nonce = secrets.token_bytes(12)
        ct = self._aead.encrypt(nonce, plaintext.encode("utf-8"), aad.encode("utf-8"))
        return "v1:" + base64.b64encode(nonce + ct).decode("ascii")

    def decrypt(self, token: str, aad: str = "") -> str:
        if not token.startswith("v1:"):
            raise ValueError("not an encrypted token (plaintext row in an encrypted store?)")
        raw = base64.b64decode(token[3:])
        return self._aead.decrypt(raw[:12], raw[12:], aad.encode("utf-8")).decode("utf-8")

    def tag(self, text: str) -> str:
        return "t1:" + mac_hex(self._tag_key, text.encode("utf-8"))


def make_cipher(mode: str, key: bytes | None = None, tag_key: bytes | None = None) -> Cipher:
    """mode 'off' -> PlaintextCipher; 'required' -> AES-GCM or EncryptionUnavailable (never a silent downgrade)."""
    mode = (mode or "off").lower()
    if mode in ("off", "plaintext", "none", ""):
        return PlaintextCipher()
    if mode in ("required", "on", "aes-gcm"):
        if key is None or tag_key is None:
            raise EncryptionUnavailable("encrypted mode needs a user-held key")
        return AESGCMCipher(key, tag_key)
    raise ValueError(f"unknown encryption mode {mode!r} (use off | required)")
