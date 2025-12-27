import streamlit as st
st.write("CHECKPOINT 1: streamlit imported")import engine
st.write("CHECKPOINT 2: engine imported")from pathlib import Path
st.write("CHECKPOINT 3: pathlib ok")base = Path(__file__).resolve().parent
questions_path = base / "questions.json"
st.write("CHECKPOINT 4: path set", str(questions_path))questions = engine.load_questions(questions_path)
st.write("CHECKPOINT 5: questions loaded", len(questions["items"]))import json
from pathlib import Path
import streamlit as st

import engine


st.set_page_config(page_title="Capacity & Strain Test", page_icon="🧭", layout="centered")

base = Path(__file__).resolve().parent
questions_path = base / "questions.json"

st.title("Capacity & Strain Test")
st.caption("Higher score = worse (more strain). Take this repeatedly over days to see trend + early failure signals.")

try:
    questions = engine.load_questions(questions_path)
except Exception as e:
    st.error(f"questions.json problem: {e}")
    st.stop()

with st.expander("What this is (read once)", expanded=False):
    st.write(
        "- This is a **strain instrument**: higher = closer to overload.\n"
        "- The point is **trend**, not one run.\n"
        "- If it triggers a kill-switch, it tells you what to cut first."
    )

st.subheader("Take the test")

answers = {}
for q in questions["items"]:
    qid = q["id"]
    answers[qid] = st.radio(q["prompt"], q["choices"], key=qid)

col1, col2 = st.columns(2)
with col1:
    label = st.text_input("Optional label (name/initials)", value="", placeholder="e.g., Lloyd / TestUser")
with col2:
    context = st.text_input("Optional context note", value="", placeholder="e.g., after work / morning / stressed")

if st.button("Submit run", type="primary"):
    results = engine.compute_results(questions, answers)
    record = engine.save_run(base, label, context, answers, results)

    hist = engine.read_history(base, limit=30)
    t = engine.trend(hist)
    ks = engine.kill_switch_plan(results["band"], results["domain_report"], t)

    st.success("Run saved.")

    st.subheader("Result")
    if results["band"] == "GREEN":
        st.success(f"{results['band']} — {results['band_note']}")
    elif results["band"] == "YELLOW":
        st.warning(f"{results['band']} — {results['band_note']}")
    else:
        st.error(f"{results['band']} — {results['band_note']}")

    st.metric("Total", f"{results['total_points']}/{results['max_points']}")
    st.metric("Ratio", results["ratio"])

    st.subheader("Domain strain (highest first)")
    st.dataframe(results["domain_report"], use_container_width=True)

    st.subheader("Trend")
    if t.get("status") == "ok":
        st.write(f"Last ratio: **{t['last_ratio']}**")
        st.write(f"Baseline mean (prior): **{t['prev_mean_ratio']}**")
        st.write(f"Delta vs baseline: **{t['delta_vs_mean']}**")
        st.write(f"Last-3 pattern: **{t['last3_pattern']}**")
    else:
        st.info(t.get("note", "Need more runs."))

    st.subheader("Kill switch")
    if ks["triggered"]:
        st.error("TRIGGERED")
        for r in ks["reasons"]:
            st.write(f"- {r}")
        for a in ks["focus_domains"]:
            st.markdown(f"**{a['domain']}** (ratio {a.get('ratio')})")
            for s in a["steps"]:
                st.write(f"• {s}")
    else:
        st.success("Not triggered (yet).")

    st.divider()
    st.subheader("Latest raw record")
    st.code(json.dumps(record, indent=2), language="json")

st.divider()
st.subheader("Recent history (last 10)")
hist = engine.read_history(base, limit=10)
if hist:
    st.dataframe(list(reversed(hist)), use_container_width=True)
else:
    st.info("No history yet. Submit your first run.")
