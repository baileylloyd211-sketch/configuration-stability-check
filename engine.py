import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

HISTORY_FILE = "history.jsonl"  # append-only log

KILL_SWITCH_PLAYBOOK = {
    "capacity": [
        "Cut scope to the smallest shippable unit.",
        "Freeze new commitments for 24 hours.",
        "Protect 1–2 core tasks only."
    ],
    "feedback": [
        "Stop guessing. Create a single measurable test.",
        "Reduce to one feedback channel.",
        "Shorten the loop (smaller experiments)."
    ],
    "coherence": [
        "Remove context switching: pick one thread and finish a chunk.",
        "Rewrite the goal in one sentence; delete tasks that don’t serve it.",
        "Schedule one deliberate block (no reacting)."
    ],
    "control": [
        "Write the top 3 constraints explicitly.",
        "Make one decision irreversible for today; defer the rest.",
        "Set a hard boundary for time/attention."
    ],
    "persistence": [
        "Lower pace to sustainable minimum.",
        "Plan only the next 6–12 hours.",
        "If endurance is hours, stop non-essential work immediately."
    ],
    "recovery": [
        "Mandatory recovery block (20–40 minutes minimum).",
        "Reduce spiral inputs; increase passive recovery.",
        "If severely deprived, do not attempt complex tasks."
    ],
    "error": [
        "Stop shipping new changes; stabilize and fix leaks.",
        "Add a checklist step before ‘done’.",
        "If rework dominates, reduce complexity and revert risky changes."
    ],
    "adaptation": [
        "Change one variable at a time.",
        "Prefer simplification over intensity.",
        "If you’re adding complexity, you’re probably losing—cut it."
    ]
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_questions(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path.name} (expected next to streamlit_app.py)")

    data = json.loads(path.read_text(encoding="utf-8"))

    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("questions.json must contain a non-empty 'items' list")

    for i, q in enumerate(items, start=1):
        for key in ("id", "type", "prompt", "choices", "weights"):
            if key not in q:
                raise ValueError(f"items[{i}] missing '{key}'")
        if q["type"] != "choice":
            raise ValueError(f"items[{i}] only supports type='choice' right now")
        if not isinstance(q["choices"], list) or not q["choices"]:
            raise ValueError(f"items[{i}] 'choices' must be a non-empty list")
        if not isinstance(q["weights"], dict) or not q["weights"]:
            raise ValueError(f"items[{i}] 'weights' must be a non-empty object")
        for c in q["choices"]:
            if c not in q["weights"]:
                raise ValueError(f"items[{i}] missing weight for choice: {c}")

    return data


def band(total: int, max_total: int) -> Tuple[str, str]:
    if max_total <= 0:
        return ("UNKNOWN", "No scoring range.")
    ratio = total / max_total
    # strain model: higher ratio = worse
    if ratio >= 0.70:
        return ("RED", "Overload likely. Reduce scope and protect core functions.")
    if ratio >= 0.45:
        return ("YELLOW", "Strain rising. Simplify and tighten the loop.")
    return ("GREEN", "Stable relative to current load.")


def compute_results(questions: Dict[str, Any], answers: Dict[str, str]) -> Dict[str, Any]:
    breakdown = []
    domain_totals: Dict[str, int] = {}
    domain_max: Dict[str, int] = {}

    total = 0
    max_total = 0

    for q in questions["items"]:
        qid = q["id"]
        ans = answers.get(qid)
        if ans is None:
            continue

        pts = int(q["weights"][ans])
        d = q.get("domain", "general")

        breakdown.append({
            "id": qid,
            "domain": d,
            "construct": q.get("construct"),
            "answer": ans,
            "points": pts
        })

        total += pts
        max_pts_for_q = max(int(v) for v in q["weights"].values())
        max_total += max_pts_for_q

        domain_totals[d] = domain_totals.get(d, 0) + pts
        domain_max[d] = domain_max.get(d, 0) + max_pts_for_q

    ratio = (total / max_total) if max_total else 0.0
    band_label, band_note = band(total, max_total)

    domain_report = []
    for d, pts in domain_totals.items():
        dmax = domain_max.get(d, 0)
        r = (pts / dmax) if dmax else 0.0
        domain_report.append({
            "domain": d,
            "points": pts,
            "max_points": dmax,
            "ratio": round(r, 3)
        })
    domain_report.sort(key=lambda x: x["ratio"], reverse=True)

    return {
        "ts": now_iso(),
        "total_points": total,
        "max_points": max_total,
        "ratio": round(ratio, 3),
        "band": band_label,
        "band_note": band_note,
        "domain_report": domain_report,
        "breakdown": breakdown
    }


def append_history(base: Path, record: Dict[str, Any]) -> None:
    path = base / HISTORY_FILE
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def read_history(base: Path, limit: int = 30) -> List[Dict[str, Any]]:
    path = base / HISTORY_FILE
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows[-limit:]


def trend(history: List[Dict[str, Any]]) -> Dict[str, Any]:
    ratios = [h.get("ratio", 0) for h in history if isinstance(h.get("ratio"), (int, float))]
    if len(ratios) < 2:
        return {"status": "insufficient", "note": "Need at least 2 runs."}

    last = ratios[-1]
    prev = ratios[:-1]
    prev_mean = sum(prev) / len(prev) if prev else last
    delta_vs_mean = last - prev_mean

    slope_note = "unknown"
    if len(ratios) >= 3:
        a, b, c = ratios[-3], ratios[-2], ratios[-1]
        if c > b > a:
            slope_note = "rising"
        elif c < b < a:
            slope_note = "falling"
        else:
            slope_note = "mixed"

    return {
        "status": "ok",
        "last_ratio": round(last, 3),
        "prev_mean_ratio": round(prev_mean, 3),
        "delta_vs_mean": round(delta_vs_mean, 3),
        "last3_pattern": slope_note
    }


def kill_switch_plan(band_label: str, domain_report: List[Dict[str, Any]], t: Dict[str, Any]) -> Dict[str, Any]:
    trigger = False
    reasons = []

    if band_label == "RED":
        trigger = True
        reasons.append("Band is RED (overload).")

    if t.get("status") == "ok":
        if t.get("last3_pattern") == "rising" and t.get("last_ratio", 0) >= 0.55:
            trigger = True
            reasons.append("Trend rising with elevated strain.")
        if t.get("delta_vs_mean", 0) >= 0.10:
            trigger = True
            reasons.append("Sharp spike vs recent baseline.")

    worst = sorted(domain_report, key=lambda r: r.get("ratio", 0), reverse=True)[:2]
    actions = []
    for w in worst:
        d = w["domain"]
        steps = KILL_SWITCH_PLAYBOOK.get(d, ["Cut scope.", "Protect core.", "Reduce complexity."])
        actions.append({"domain": d, "ratio": w.get("ratio"), "steps": steps})

    return {
        "triggered": trigger,
        "reasons": reasons,
        "focus_domains": actions
    }


def save_run(base: Path, label: str, context: str, answers: Dict[str, str], results: Dict[str, Any]) -> Dict[str, Any]:
    record = {
        "ts": results["ts"],
        "label": (label or "").strip(),
        "context": (context or "").strip(),
        "ratio": results["ratio"],
        "band": results["band"],
        "total_points": results["total_points"],
        "max_points": results["max_points"],
        "domain_report": results["domain_report"],
        "answers": answers
    }
    append_history(base, record)
    return record
