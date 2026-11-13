#!/usr/bin/env python3
"""Validate Trend Radar state files.  Standard library only.

Exit code 0 if no errors (warnings allowed), 1 otherwise.
"""
import json
import pathlib
import re
import sys
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / "state"

errors, warnings = [], []
err = errors.append
warn = warnings.append

FULL_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PART_DATE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")
TREND_ID = re.compile(r"^(DM|AI|AG)-\d{2}$")
EV_ID = re.compile(r"^EV-\d{4}$")
W_ID = re.compile(r"^W-\d{2}$")
CATEGORY = {"DM": "data_management", "AI": "ai_ml", "AG": "agentic"}
MOMENTUM = {"baseline", "rising", "stable", "fading"}
CONFIDENCE = {"high", "medium", "low"}
STATUS = {"active", "merged", "retired"}
W_STATUS = {"watching", "promoted", "dropped"}
TREND_FIELDS = [
    "trend_id", "status", "category", "title", "definition", "importance",
    "importance_prev", "industry_relevance", "momentum", "confidence",
    "rationale", "industry_note", "evidence_ids", "counter_evidence_ids",
    "first_seen", "last_changed", "last_evidence_date", "merged_into", "history",
]


def norm_url(url):
    p = urlsplit(url.strip())
    return f"{p.netloc.lower().removeprefix('www.')}{p.path.rstrip('/')}"


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        err(f"{path.relative_to(ROOT)}: cannot parse JSON ({exc})")
        return None


def load_jsonl(path):
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception as exc:  # noqa: BLE001
            err(f"{path.relative_to(ROOT)} line {n}: cannot parse JSON ({exc})")
    return rows


def score(value, name, ctx):
    if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
        err(f"{ctx}: {name} must be an integer 1-5, got {value!r}")


# ---------------------------------------------------------------- run log
run_log = load_jsonl(STATE / "run_log.jsonl")
run_ids = [r.get("run_id") for r in run_log]
for r in run_log:
    if not FULL_DATE.match(str(r.get("run_id", ""))):
        err(f"run_log: bad run_id {r.get('run_id')!r}")
if len(set(run_ids)) != len(run_ids):
    err("run_log: duplicate run_id")
if run_ids != sorted(run_ids):
    err("run_log: run_ids not in ascending order")
latest = run_ids[-1] if run_ids else None

# ---------------------------------------------------------------- watch list
wl = load_json(STATE / "watchlist.json") or {"items": []}
watch_ids = set()
for w in wl.get("items", []):
    wid = w.get("id", "")
    if not W_ID.match(wid):
        err(f"watchlist: bad id {wid!r}")
    if wid in watch_ids:
        err(f"watchlist: duplicate id {wid}")
    watch_ids.add(wid)
    if w.get("status") not in W_STATUS:
        err(f"watchlist {wid}: bad status {w.get('status')!r}")

# ---------------------------------------------------------------- register
reg = load_json(STATE / "register.json") or {"trends": []}
trend_ids = set()
trends = reg.get("trends", [])
for t in trends:
    tid = t.get("trend_id", "?")
    ctx = f"register {tid}"
    missing = [f for f in TREND_FIELDS if f not in t]
    if missing:
        err(f"{ctx}: missing fields {missing}")
        continue
    if not TREND_ID.match(tid):
        err(f"{ctx}: bad trend_id")
    elif CATEGORY[tid[:2]] != t["category"]:
        err(f"{ctx}: category {t['category']!r} does not match prefix")
    if tid in trend_ids:
        err(f"{ctx}: duplicate trend_id")
    trend_ids.add(tid)
    if t["status"] not in STATUS:
        err(f"{ctx}: bad status")
    score(t["importance"], "importance", ctx)
    score(t["industry_relevance"], "industry_relevance", ctx)
    if t["importance_prev"] is not None:
        score(t["importance_prev"], "importance_prev", ctx)
        if abs(t["importance"] - t["importance_prev"]) > 2:
            err(f"{ctx}: importance moved by more than 2 in one run")
    if t["momentum"] not in MOMENTUM:
        err(f"{ctx}: bad momentum")
    if t["confidence"] not in CONFIDENCE:
        err(f"{ctx}: bad confidence")
    for f in ("first_seen", "last_changed"):
        if not FULL_DATE.match(str(t[f])):
            err(f"{ctx}: bad {f}")
    if t["last_evidence_date"] and not PART_DATE.match(str(t["last_evidence_date"])):
        err(f"{ctx}: bad last_evidence_date")
    if t["status"] == "active" and not t["evidence_ids"]:
        err(f"{ctx}: active trend has no evidence")
    if t["status"] == "merged" and not t["merged_into"]:
        err(f"{ctx}: merged trend needs merged_into")
    if not t["history"]:
        err(f"{ctx}: empty history")
    else:
        for h in t["history"]:
            if h.get("run_id") not in run_ids:
                err(f"{ctx}: history run_id {h.get('run_id')!r} not in run_log")
        if t["status"] == "active" and latest and t["history"][-1].get("run_id") != latest:
            err(f"{ctx}: no history entry for latest run {latest}")
        if t["history"][-1].get("importance") != t["importance"]:
            err(f"{ctx}: latest history importance differs from current importance")
    if t["momentum"] == "baseline" and len(t["history"]) > 1:
        warn(f"{ctx}: momentum still 'baseline' after first run")
for t in trends:
    if t.get("merged_into") and t["merged_into"] not in trend_ids:
        err(f"register {t['trend_id']}: merged_into {t['merged_into']} not found")

# ---------------------------------------------------------------- ledger
ledger = load_jsonl(STATE / "ledger.jsonl")
ev_ids, urls = set(), {}
valid_targets = trend_ids | watch_ids
for n, e in enumerate(ledger, 1):
    eid = e.get("evidence_id", "?")
    ctx = f"ledger {eid}"
    if not EV_ID.match(eid):
        err(f"{ctx}: bad evidence_id")
    elif int(eid[3:]) != n:
        err(f"{ctx}: evidence IDs must be sequential (expected EV-{n:04d})")
    if eid in ev_ids:
        err(f"{ctx}: duplicate evidence_id")
    ev_ids.add(eid)
    for f in ("url", "publisher", "title", "summary", "retrieved_date"):
        if not e.get(f):
            err(f"{ctx}: missing {f}")
    u = norm_url(e.get("url", ""))
    if u in urls:
        err(f"{ctx}: duplicate URL (already {urls[u]})")
    urls[u] = eid
    if e.get("tier") not in (1, 2, 3, 4):
        err(f"{ctx}: tier must be 1-4")
    if e.get("published_date") is not None and not PART_DATE.match(str(e["published_date"])):
        err(f"{ctx}: bad published_date")
    if not FULL_DATE.match(str(e.get("retrieved_date", ""))):
        err(f"{ctx}: bad retrieved_date")
    elif e["retrieved_date"] not in run_ids:
        warn(f"{ctx}: retrieved_date {e['retrieved_date']} is not a logged run")
    if len(e.get("summary", "")) > 400:
        err(f"{ctx}: summary over 400 characters (paraphrase more tightly)")
    if e.get("quote") and len(e["quote"].split()) >= 15:
        err(f"{ctx}: quote must be under 15 words")
    for ref in e.get("supports", []) + e.get("contradicts", []):
        if ref not in valid_targets:
            err(f"{ctx}: references unknown trend or watch item {ref}")
    if not e.get("supports") and not e.get("contradicts"):
        warn(f"{ctx}: tagged to nothing")
    if e.get("tier") == 4 and not e.get("notes"):
        warn(f"{ctx}: tier 4 source without a note")

for t in trends:
    for ref in t.get("evidence_ids", []) + t.get("counter_evidence_ids", []):
        if ref not in ev_ids:
            err(f"register {t['trend_id']}: evidence {ref} not in ledger")
for w in wl.get("items", []):
    for ref in w.get("evidence_ids", []):
        if ref not in ev_ids:
            err(f"watchlist {w.get('id')}: evidence {ref} not in ledger")

# ---------------------------------------------------------------- run outputs
if latest:
    run_dir = ROOT / "runs" / latest
    mode = run_log[-1].get("mode")
    for f in ("snapshot.json", "briefing.md"):
        if not (run_dir / f).exists():
            err(f"runs/{latest}/{f} missing")
    if mode == "scheduled" and not (run_dir / "blind_scan.md").exists():
        err(f"runs/{latest}/blind_scan.md missing for a scheduled run")
    snap_path = run_dir / "snapshot.json"
    if snap_path.exists():
        snap = load_json(snap_path)
        if snap and snap.get("register") != reg:
            warn(f"runs/{latest}/snapshot.json register differs from state/register.json "
                 "(re-run make_snapshot.py after final edits)")

# ---------------------------------------------------------------- report
for w in warnings:
    print(f"WARNING: {w}")
for e in errors:
    print(f"ERROR: {e}")
print(f"\n{len(trends)} trends, {len(watch_ids)} watch items, {len(ledger)} evidence entries, "
      f"{len(run_ids)} runs.  {len(errors)} errors, {len(warnings)} warnings.")
sys.exit(1 if errors else 0)
