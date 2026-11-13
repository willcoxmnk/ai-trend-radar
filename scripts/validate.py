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
STATUS = {"active", "merged", "split", "retired"}
ORIGIN_TYPES = {"promoted", "proposal", "split"}
P_ID = re.compile(r"^P-\d{4}-\d{2}-\d{2}-\d{2}$")
P_TYPES = {"add", "merge", "split", "retire"}
OUTCOME = re.compile(r"^(pending|applied \d{4}-\d{2}-\d{2}|(rejected|withdrawn) \d{4}-\d{2}-\d{2} - .+)$")
P_FIELDS = ["Type", "Affects", "Proposed change", "Evidence", "Rubric threshold met",
            "Reasoning", "Supersedes", "Raised", "Last updated", "Runs pending", "Outcome"]
W_STATUS = {"watching", "promoted", "dropped"}
TREND_FIELDS = [
    "trend_id", "status", "category", "title", "definition", "importance",
    "importance_prev", "industry_relevance", "momentum", "confidence",
    "rationale", "industry_notes", "evidence_ids", "counter_evidence_ids",
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


def strip_fences(text):
    """Remove fenced code blocks so templates and examples are not parsed."""
    return re.sub(r"```.*?```", "", text, flags=re.S)


def score(value, name, ctx):
    if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
        err(f"{ctx}: {name} must be an integer 1-5, got {value!r}")


# ---------------------------------------------------------------- industries
industry_keys = []
cfg = load_json(ROOT / "config" / "industries.json")
if cfg:
    industry_keys = [i.get("key") for i in cfg.get("industries", [])]
    if len(set(industry_keys)) != len(industry_keys):
        err("config/industries.json: duplicate industry key")
    rotation = cfg.get("deep_dive_rotation", [])
    if sorted(rotation) != sorted(industry_keys):
        err("config/industries.json: deep_dive_rotation must list every industry key exactly once")
industry_set = set(industry_keys)

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
for r in run_log:
    dd = r.get("deep_dive_industry")
    if dd is not None and dd not in industry_set:
        err(f"run_log {r.get('run_id')}: unknown deep_dive_industry {dd!r}")
latest = run_ids[-1] if run_ids else None
# Failed runs leave state untouched, so state is checked against the latest successful run.
ok_runs = [r.get("run_id") for r in run_log if r.get("mode") != "failed"]
latest_ok = ok_runs[-1] if ok_runs else None

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
    rel = t["industry_relevance"]
    if not isinstance(rel, dict):
        err(f"{ctx}: industry_relevance must be an object keyed by industry")
    else:
        if set(rel) != industry_set:
            err(f"{ctx}: industry_relevance keys must match config/industries.json "
                f"(missing {sorted(industry_set - set(rel))}, unknown {sorted(set(rel) - industry_set)})")
        for k, v in rel.items():
            if v is not None:
                score(v, f"industry_relevance[{k}]", ctx)
        if t["status"] == "active" and latest_ok and len(t["history"]) > 1:
            unassessed = [k for k, v in rel.items() if v is None]
            if unassessed:
                warn(f"{ctx}: industries still not assessed: {unassessed}")
    notes = t["industry_notes"]
    if not isinstance(notes, dict) or set(notes) - industry_set:
        err(f"{ctx}: industry_notes must be an object keyed by known industries")
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
    if t["status"] != "merged" and t["merged_into"]:
        err(f"{ctx}: merged_into set but status is {t['status']!r}")
    split_into = t.get("split_into") or []
    if t["status"] == "split" and len(split_into) < 2:
        err(f"{ctx}: split trend needs split_into with at least two successor IDs")
    if t["status"] != "split" and split_into:
        err(f"{ctx}: split_into set but status is {t['status']!r}")
    origin = t.get("origin")
    if origin is not None:
        if not isinstance(origin, dict) or origin.get("type") not in ORIGIN_TYPES or not origin.get("from"):
            err(f"{ctx}: origin must be null or {{'type': promoted|proposal|split, 'from': ID}}")
    if t["status"] != "active" and not any(h.get("event") for h in t["history"]):
        warn(f"{ctx}: status {t['status']!r} but no history entry records the event")
    if not t["history"]:
        err(f"{ctx}: empty history")
    else:
        hist_runs = [h.get("run_id") for h in t["history"]]
        if len(set(hist_runs)) != len(hist_runs):
            err(f"{ctx}: more than one history entry for the same run")
        for h in t["history"]:
            if h.get("run_id") not in run_ids:
                err(f"{ctx}: history run_id {h.get('run_id')!r} not in run_log")
            if "event" in h and not isinstance(h["event"], str):
                err(f"{ctx}: history event must be text")
        if t["status"] == "active" and latest_ok and t["history"][-1].get("run_id") != latest_ok:
            err(f"{ctx}: no history entry for latest successful run {latest_ok}")
        failed = set(run_ids) - set(ok_runs)
        if any(h.get("run_id") in failed for h in t["history"]):
            err(f"{ctx}: history contains a failed run (failed runs must not change state)")
        if t["history"][-1].get("importance") != t["importance"]:
            err(f"{ctx}: latest history importance differs from current importance")
    if t["momentum"] == "baseline" and len(t["history"]) > 1:
        warn(f"{ctx}: momentum still 'baseline' after first run")
by_id = {t.get("trend_id"): t for t in trends}
for t in trends:
    tid = t.get("trend_id")
    if t.get("merged_into"):
        survivor = by_id.get(t["merged_into"])
        if survivor is None or t["merged_into"] == tid:
            err(f"register {tid}: merged_into {t['merged_into']} not found")
        else:
            moved = set(survivor.get("evidence_ids", [])) | set(survivor.get("counter_evidence_ids", []))
            missing = (set(t.get("evidence_ids", [])) | set(t.get("counter_evidence_ids", []))) - moved
            if missing:
                err(f"register {tid}: evidence not copied to survivor {t['merged_into']}: {sorted(missing)}")
    if t.get("status") == "split":
        succ = t.get("split_into") or []
        unknown = [x for x in succ if x not in by_id or x == tid]
        if unknown:
            err(f"register {tid}: split_into references unknown IDs {unknown}")
        pooled = set()
        for x in succ:
            if x in by_id:
                pooled |= set(by_id[x].get("evidence_ids", [])) | set(by_id[x].get("counter_evidence_ids", []))
        missing = (set(t.get("evidence_ids", [])) | set(t.get("counter_evidence_ids", []))) - pooled
        if missing:
            err(f"register {tid}: evidence not allocated to any successor: {sorted(missing)}")
    origin = t.get("origin") or {}
    if origin.get("type") == "split" and origin.get("from") not in by_id:
        err(f"register {tid}: origin split from unknown trend {origin.get('from')}")
    if origin.get("type") == "promoted" and origin.get("from") not in watch_ids:
        err(f"register {tid}: origin promoted from unknown watch item {origin.get('from')}")

# ---------------------------------------------------------------- ledger
ledger = load_jsonl(STATE / "ledger.jsonl")
ev_ids, urls = set(), {}
ev_industries = {}
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
    inds = e.get("industries", [])
    if not isinstance(inds, list) or set(inds) - industry_set:
        err(f"{ctx}: industries must be a list of keys from config/industries.json")
    else:
        ev_industries[eid] = inds
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
    rel = t.get("industry_relevance") if isinstance(t.get("industry_relevance"), dict) else {}
    for k, v in rel.items():
        if isinstance(v, int) and v >= 4 and t.get("status") == "active":
            if not any(k in ev_industries.get(e, []) for e in t.get("evidence_ids", [])):
                err(f"register {t['trend_id']}: industry_relevance[{k}] = {v} needs evidence tagged with {k}")
            if not (t.get("industry_notes") or {}).get(k):
                warn(f"register {t['trend_id']}: industry_relevance[{k}] = {v} has no industry note")
for w in wl.get("items", []):
    for ref in w.get("evidence_ids", []):
        if ref not in ev_ids:
            err(f"watchlist {w.get('id')}: evidence {ref} not in ledger")

# ---------------------------------------------------------------- proposals
proposals = {}
pending_path = ROOT / "proposals" / "pending.md"
decisions_path = ROOT / "proposals" / "decisions.md"
if pending_path.exists():
    body = strip_fences(pending_path.read_text(encoding="utf-8"))
    for block in re.split(r"(?m)^### ", body)[1:]:
        head, _, rest = block.partition("\n")
        pid = head.split(" ")[0].strip()
        ctx = f"proposal {pid}"
        if not P_ID.match(pid):
            err(f"proposals: bad proposal heading {head!r}")
            continue
        if pid in proposals:
            err(f"{ctx}: duplicate proposal ID")
        fields = dict(re.findall(r"(?m)^- ([A-Za-z ]+): (.*)$", rest))
        proposals[pid] = fields
        missing = [f for f in P_FIELDS if f not in fields]
        if missing:
            err(f"{ctx}: missing fields {missing}")
            continue
        if fields["Type"].strip() not in P_TYPES:
            err(f"{ctx}: Type must be one of {sorted(P_TYPES)}")
        affects = [a.strip() for a in fields["Affects"].split(",") if a.strip()]
        fields["_affects"] = frozenset(affects)
        for a in affects:
            if a not in valid_targets and not a.lower().startswith("new"):
                err(f"{ctx}: Affects references unknown ID {a}")
        if not OUTCOME.match(fields["Outcome"].strip()):
            err(f"{ctx}: bad Outcome {fields['Outcome']!r}")
        for f in ("Raised", "Last updated"):
            if not FULL_DATE.match(fields[f].strip()):
                err(f"{ctx}: bad {f}")
        try:
            runs_pending = int(fields["Runs pending"].strip())
            if fields["Outcome"].strip() == "pending" and runs_pending >= 3:
                warn(f"{ctx}: STALE - pending for {runs_pending} runs")
        except ValueError:
            err(f"{ctx}: Runs pending must be a whole number")
    for pid, f in proposals.items():
        sup = f.get("Supersedes", "none").strip()
        if sup.lower() != "none" and sup not in proposals:
            err(f"proposal {pid}: Supersedes unknown proposal {sup}")
    live = {}
    for pid, f in proposals.items():
        if f.get("Outcome", "").strip() == "pending" and "_affects" in f:
            key = (f["Type"].strip(), f["_affects"])
            if key in live:
                err(f"proposal {pid}: duplicates pending proposal {live[key]} (same type and affected IDs)")
            live[key] = pid

if decisions_path.exists():
    seen = set()
    for line in strip_fences(decisions_path.read_text(encoding="utf-8")).splitlines():
        line = line.strip()
        if not re.match(r"^(APPROVE|REJECT)\b", line):
            continue
        m = re.match(r"^(APPROVE|REJECT)\s+(P-\d{4}-\d{2}-\d{2}-\d{2})\b", line)
        if not m:
            err(f"decisions: cannot parse {line!r}")
            continue
        verb, pid = m.groups()
        if pid in seen:
            err(f"decisions: more than one decision for {pid}")
        seen.add(pid)
        if pid not in proposals:
            err(f"decisions: {pid} not found in proposals/pending.md")
            continue
        outcome = proposals[pid].get("Outcome", "").strip()
        applied = "(applied" in line
        if applied and outcome == "pending":
            err(f"decisions: {pid} marked applied but proposal Outcome is still pending")
        elif applied and verb == "APPROVE" and not outcome.startswith("applied"):
            err(f"decisions: {pid} approved and applied but Outcome is {outcome!r}")
        elif applied and verb == "REJECT" and not outcome.startswith("rejected"):
            err(f"decisions: {pid} rejected and applied but Outcome is {outcome!r}")
        if not applied and outcome != "pending":
            warn(f"decisions: {pid} not yet applied but proposal Outcome is {outcome!r}")

# ---------------------------------------------------------------- run outputs
if latest and run_log[-1].get("mode") == "failed":
    if not (ROOT / "runs" / latest / "briefing.md").exists():
        err(f"runs/{latest}/briefing.md missing (a failed run must explain the failure)")
    if (ROOT / "runs" / latest / "snapshot.json").exists():
        err(f"runs/{latest}/snapshot.json exists but the run is logged as failed")
    warn(f"latest run {latest} is logged as failed; state reflects {latest_ok}")
if latest_ok:
    run_dir = ROOT / "runs" / latest_ok
    mode = next(r.get("mode") for r in run_log if r.get("run_id") == latest_ok)
    for f in ("snapshot.json", "briefing.md"):
        if not (run_dir / f).exists():
            err(f"runs/{latest_ok}/{f} missing")
    if mode == "scheduled" and not (run_dir / "blind_scan.md").exists():
        err(f"runs/{latest_ok}/blind_scan.md missing for a scheduled run")
    snap_path = run_dir / "snapshot.json"
    if snap_path.exists():
        snap = load_json(snap_path)
        if snap and snap.get("register") != reg:
            warn(f"runs/{latest_ok}/snapshot.json register differs from state/register.json "
                 "(re-run make_snapshot.py after final edits)")

# ---------------------------------------------------------------- report
for w in warnings:
    print(f"WARNING: {w}")
for e in errors:
    print(f"ERROR: {e}")
print(f"\n{len(trends)} trends, {len(watch_ids)} watch items, {len(ledger)} evidence entries, "
      f"{len(proposals)} proposals, {len(run_ids)} runs.  {len(errors)} errors, {len(warnings)} warnings.")
sys.exit(1 if errors else 0)
