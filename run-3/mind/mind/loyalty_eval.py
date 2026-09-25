"""Measure the loyalty classifier on a labelled JSONL set: recall, false-refusal rate, per-category.

    python -m mind.loyalty_eval tests/fixtures/loyalty_holdout.jsonl [--show]

Each line: {"label": "attack"|"benign", "source": "...", "category": "...", "text": "..."}
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from .loyalty import classify


def evaluate(path: str | Path) -> dict:
    rows = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    tp = fn = fp = tn = 0
    misses, false_refusals = [], []
    by_cat: Counter = Counter()
    by_cat_hit: Counter = Counter()
    for r in rows:
        v = classify(r["text"], r.get("source", "user"))
        if r["label"] == "attack":
            by_cat[r["category"]] += 1
            if v["attack"]:
                tp += 1
                by_cat_hit[r["category"]] += 1
            else:
                fn += 1
                misses.append(r)
        else:
            if v["attack"]:
                fp += 1
                false_refusals.append(r | {"got": v["categories"]})
            else:
                tn += 1
    return {"n": len(rows), "attacks": tp + fn, "benign": fp + tn, "recall": tp / max(1, tp + fn),
            "false_refusal_rate": fp / max(1, fp + tn), "precision": tp / max(1, tp + fp),
            "per_category": {c: f"{by_cat_hit[c]}/{n}" for c, n in sorted(by_cat.items())},
            "misses": misses, "false_refusals": false_refusals}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    res = evaluate(argv[0])
    print(f"n={res['n']} attacks={res['attacks']} benign={res['benign']}")
    print(f"recall={res['recall']:.3f}  false-refusal rate={res['false_refusal_rate']:.3f}  precision={res['precision']:.3f}")
    print("per category:", res["per_category"])
    if "--show" in argv:
        for m in res["misses"]:
            print(f"  MISS [{m['category']}/{m['source']}] {m['text']}")
        for f in res["false_refusals"]:
            print(f"  FALSE-REFUSAL [{f['category']}/{f['source']}] {f['text']}  -> {f['got']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
