import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple


HISTORY_FILE = "history.jsonl"  # append-only; safest for logging


KILL_SWITCH_PLAYBOOK = {
    "capacity": [
        "Cut scope to the smallest shippable unit.",
        "Freeze new commitments for 24 hours.",
        "Protect 1–2 core tasks only."
    ],
    "feedback": [
        "Stop guessing. Create a single measurable test.",
        "Reduce to one feedback channel.",
        "If feedback is slow, shorten the loop (smaller experiments)."
    ],
    "coherence": [
        "Remove context switching: pick one thread and finish a chunk.",
        "Rewrite the goal in one sentence and delete any task that doesn’t serve it.",
        "If reactive, schedule one deliberate block."
    ],
    "control": [
        "Clarify constraints: write the top 3 constraints explicitly.",
        "Make one decision irreversible for today; defer the rest.",
        "Set a hard boundary for time/attention."
    ],
    "persistence": [
        "Lower pace to sustainable minimum.",
        "Plan only the next 6–12 hours (not the week).",
        "If endurance is hours, stop non-essential work immediately."
    ],
    "recovery": [
        "Mandatory recovery block (even 20–40 minutes).",
        "Reduce stimulants/spiral inputs; increase passive recovery.",
        "If severely deprived, do not attempt complex tasks."
    ],
    "error": [
        "Stop shipping new changes; stabilize and fix leaks.",
        "Introduce a checklist step before ‘done’.",
        "If rework dominates, reduce complexity and revert risky changes."
    ],
    "adaptation": [
        "Change one variable at a time (no shotgun changes).",
        "Prefer simplification over intensity.",
        "If you’re adding complexity, you’re probably losing—cut it."
    ]
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_questions(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path.name} (expected next to app.py)")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"{path.name} is not valid JSON: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("questions.json must be a JSON object")

    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("questions.json must contain non-empty 'items' list")

    for i, q in enumerate(items, start=1):
        for key in ("id", "type", "prompt", "choices", "weights"):
            if key not in q:
                raise ValueError(f"items[{i}] missing '{key}'")
        if q["type"] != "choice":
            raise ValueError(f"items[{i}] only supports type='choice' right now")
        if not isinstance(q["choices"], list) or not q["choices"]:
            raise ValueError(f"items[{i}] choices must be non-empty list")
        if not isinstance(q["weights"], dict) or not q["weights"]:
            raise ValueError(f"items[{i}] weights must be non-empty object")
        for c in q["choices"]:
            if c not in q["weights"]:
                raise ValueError(f"items[{i}] missing weight for choice: {c}")

    return data


def ask_choice(prompt: str, choices: List[str]) -> str:
    print(f"\n{prompt}")
    for idx, c in enumerate(choices, start=1):
        print(f"  {idx}) {c}")
    while True:
        raw = input("> ").strip()
        if raw.isdigit():
            n = int(raw)
            if 1 <= n <= len(choices):
                return choices[n - 1]
        if raw in choices:
            return raw
        print("Pick a number from the list (or type the option exactly).")


def band(total: int, max_total: int) -> Tuple[str, str]:
    if max_total <= 0:
        return ("UNKNOWN", "No scoring range.")
    ratio = total / max_total
    if ratio >= 0.70:
        return ("RED", "Overload likely. Reduce scope and protect core functions.")
    if ratio >= 0.45:
        return ("YELLOW", "Strain rising. Simplify and tighten the loop.")
    return ("GREEN", "Stable relative to current load.")


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
    """
    Simple, robust trend: compare last value to mean of previous runs.
    Also compute direction over last 3 points if available.
    """
    ratios = [h.get("ratio", 0) for h in history if isinstance(h.get("ratio"), (int, float))]
    if len(ratios) < 2:
        return {"status": "insufficient", "note": "Need at least 2 runs."}

    last = ratios[-1]
    prev = ratios[:-1]
    prev_mean = sum(prev) / len(prev) if prev else last

    delta_vs_mean = last - prev_mean

    # last 3 slope
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
    """
    Trigger kill-switch if:
      - band is RED, or
      - trend is rising AND last ratio >= 0.55, or
      - delta vs mean >= +0.10 (sharp spike)
    """
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

    # Pick top 2 worst domains by ratio
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


def main():
    base = Path(__file__).resolve().parent
    qpath = base / "questions.json"
    questions = load_questions(qpath)

    answers: Dict[str, str] = {}
    breakdown = []
    domain_totals: Dict[str, int] = {}
    domain_max: Dict[str, int] = {}

    total = 0
    max_total = 0

    for q in questions["items"]:
        ans = ask_choice(q["prompt"], q["choices"])
        pts = int(q["weights"][ans])
        d = q.get("domain", "general")

        answers[q["id"]] = ans
        breakdown.append({
            "id": q["id"],
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

    record = {
        "ts": now_iso(),
        "total_points": total,
        "max_points": max_total,
        "ratio": round(ratio, 3),
        "band": band_label,
        "domain_report": domain_report,
        "answers": answers
    }

    append_history(base, record)

    hist = read_history(base, limit=30)
    t = trend(hist)
    ks = kill_switch_plan(band_label, domain_report, t)

    # Write latest outputs
    (base / "answers.json").write_text(json.dumps(answers, indent=2), encoding="utf-8")
    (base / "results.json").write_text(json.dumps({
        **record,
        "band_note": band_note,
        "trend": t,
        "kill_switch": ks
    }, indent=2), encoding="utf-8")

    print("\n====================")
    print(f"TOTAL: {total}/{max_total}  ratio={round(ratio,3)}")
    print(f"BAND:  {band_label} — {band_note}")
    if t.get("status") == "ok":
        print(f"TREND: last={t['last_ratio']} prev_mean={t['prev_mean_ratio']} delta={t['delta_vs_mean']} pattern={t['last3_pattern']}")
    else:
        print("TREND: need more runs")
    print("====================\n")

    print("Worst domains (highest strain first):")
    for row in domain_report[:3]:
        print(f"- {row['domain']}: {row['points']}/{row['max_points']} (ratio {row['ratio']})")

    if ks["triggered"]:
        print("\nKILL SWITCH: TRIGGERED")
        for r in ks["reasons"]:
            print(f"- {r}")
        print("\nDo this now (focus domains):")
        for a in ks["focus_domains"]:
            print(f"\n[{a['domain']}] (ratio {a.get('ratio')})")
            for s in a["steps"]:
                print(f"  - {s}")
    else:
        print("\nKILL SWITCH: not triggered (yet).")

    print(f"\nLogged run → {HISTORY_FILE}")
    print("Saved: answers.json, results.json")


if __name__ == "__main__":
    main()
