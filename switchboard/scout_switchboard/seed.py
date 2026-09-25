"""Load a roster file (see seeds/chester.example.json) into the store. Safe to re-run."""
import json
from pathlib import Path

from .db import Store


def load_seed(store: Store, path: str | Path) -> list[str]:
    data = json.loads(Path(path).read_text())
    loaded = []
    for t in data["tenants"]:
        tenant = store.upsert_tenant(t["slug"], t["name"], t.get("persona", "Scout"))
        for line in t.get("lines", []):
            store.add_line(line["number"], tenant, line.get("channel", "sms"), line.get("label", ""))
        ids: dict[str, int] = {}
        for p in t.get("people", []):
            pid = store.upsert_person(p["phone"], p["name"])
            store.add_member(tenant, pid, p["role"], p.get("status", "active"), p.get("alias"))
            ids[p["name"]] = pid
        for a, b in t.get("reach", []):
            store.allow(tenant, ids[a], ids[b], both_ways=True)
        for a, label, b in t.get("relationships", []):
            store.relate(tenant, ids[a], ids[b], label)
        for group, members in t.get("groups", {}).items():
            store.add_group(tenant, group, [ids[m] for m in members])
        loaded.append(tenant.slug)
    return loaded
