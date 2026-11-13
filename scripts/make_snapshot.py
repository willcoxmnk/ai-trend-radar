#!/usr/bin/env python3
"""Write runs/<run-id>/snapshot.json and print the diff against the previous run.

The diff is computed here, deterministically, so the briefing is based on what
actually changed rather than on the agent's recollection.  Standard library only.

Usage: python3 scripts/make_snapshot.py --run-id YYYY-MM-DD [--mode scheduled|baseline]
"""
import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / "state"
RUNS = ROOT / "runs"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def previous_snapshot(run_id):
    earlier = sorted(p.name for p in RUNS.iterdir()
                     if p.is_dir() and p.name < run_id and (p / "snapshot.json").exists())
    if not earlier:
        return None
    return load(RUNS / earlier[-1] / "snapshot.json")


def diff(prev, reg, watch, ledger):
    out = {"previous_run": None, "trends_added": [], "trends_status_changed": [],
           "importance_changed": [], "relevance_changed": [], "momentum_changed": [],
           "confidence_changed": [], "watch_added": [], "watch_status_changed": [],
           "new_evidence_ids": [e["evidence_id"] for e in ledger]}
    if prev is None:
        out["trends_added"] = [t["trend_id"] for t in reg["trends"]]
        out["watch_added"] = [w["id"] for w in watch["items"]]
        return out
    out["previous_run"] = prev["run_id"]
    before = {t["trend_id"]: t for t in prev["register"]["trends"]}
    for t in reg["trends"]:
        tid = t["trend_id"]
        b = before.get(tid)
        if b is None:
            out["trends_added"].append(tid)
            continue
        if b["status"] != t["status"]:
            out["trends_status_changed"].append({"id": tid, "from": b["status"], "to": t["status"]})
        for key, bucket in (("importance", "importance_changed"),
                            ("momentum", "momentum_changed"),
                            ("confidence", "confidence_changed")):
            if b[key] != t[key]:
                out[bucket].append({"id": tid, "from": b[key], "to": t[key]})
        before_rel = b.get("industry_relevance")
        after_rel = t.get("industry_relevance") or {}
        if not isinstance(before_rel, dict):
            before_rel = {}  # pre-2.0 snapshots held a single airline score
        for ind, val in after_rel.items():
            if before_rel.get(ind) != val:
                out["relevance_changed"].append(
                    {"id": tid, "industry": ind, "from": before_rel.get(ind), "to": val})
    wb = {w["id"]: w for w in prev["watchlist"]["items"]}
    for w in watch["items"]:
        if w["id"] not in wb:
            out["watch_added"].append(w["id"])
        elif wb[w["id"]]["status"] != w["status"]:
            out["watch_status_changed"].append(
                {"id": w["id"], "from": wb[w["id"]]["status"], "to": w["status"]})
    seen = prev.get("ledger_max_id", "EV-0000")
    out["new_evidence_ids"] = [e["evidence_id"] for e in ledger if e["evidence_id"] > seen]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--mode", default="scheduled", choices=["scheduled", "baseline"])
    args = ap.parse_args()
    try:
        datetime.strptime(args.run_id, "%Y-%m-%d")
    except ValueError:
        sys.exit("run-id must be YYYY-MM-DD")

    reg = load(STATE / "register.json")
    watch = load(STATE / "watchlist.json")
    ledger = [json.loads(l) for l in (STATE / "ledger.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    prev = previous_snapshot(args.run_id)
    d = diff(prev, reg, watch, ledger)

    snapshot = {
        "run_id": args.run_id,
        "mode": args.mode,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rubric_version": reg.get("rubric_version"),
        "ledger_count": len(ledger),
        "ledger_max_id": ledger[-1]["evidence_id"] if ledger else "EV-0000",
        "diff": d,
        "register": reg,
        "watchlist": watch,
    }
    out_dir = RUNS / args.run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "snapshot.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8")

    print(f"Wrote runs/{args.run_id}/snapshot.json")
    print(f"Previous run: {d['previous_run'] or 'none (baseline)'}")
    for key, items in d.items():
        if key == "previous_run" or not items:
            continue
        if key == "new_evidence_ids":
            print(f"  new evidence: {len(items)} ({items[0]} to {items[-1]})")
        else:
            print(f"  {key}: {items}")


if __name__ == "__main__":
    main()
