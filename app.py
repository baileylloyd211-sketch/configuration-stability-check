import streamlit as st
import json
from datetime import datetime

# -----------------------------
# BASIC APP SETUP
# -----------------------------
st.set_page_config(page_title="Configuration Stability Check", layout="centered")

if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.responses = []
    st.session_state.current_q = 0

# -----------------------------
# SAMPLE QUESTIONS (TEMP)
# Replace tomorrow with full pool
# -----------------------------
QUESTIONS = [
    {
        "id": "P1",
        "prompt": "When demands increase faster than available capacity, what happens first?",
        "options": [
            "The system reallocates effort internally",
            "Non-essential activity is deferred",
            "Output quality becomes uneven",
            "Short-term throughput is prioritized",
            "Coordination becomes harder",
        ],
    },
    {
        "id": "P2",
        "prompt": "When results are slow to appear, how does the system proceed?",
        "options": [
            "It continues based on prior assumptions",
            "It pauses to reassess direction",
            "It seeks informal signals",
            "It increases activity to compensate",
            "It narrows focus to fewer actions",
        ],
    },
    {
        "id": "P3",
        "prompt": "When effort doesn’t reliably translate into progress, what emerges?",
        "options": [
            "Process refinement",
            "Frustration without action",
            "Experimentation",
            "Reduced engagement",
            "Overextension",
        ],
    },
]

MAX_QUESTIONS = len(QUESTIONS)

# -----------------------------
# START SCREEN
# -----------------------------
if st.session_state.stage == "start":
    st.title("Configuration Stability Check")

    st.markdown(
        """
        This tool provides a baseline read on whether a system
        is likely to remain workable under continued conditions.

        It does **not** diagnose, judge, or prescribe actions.
        """
    )

    system_type = st.selectbox(
        "What system are you evaluating?",
        [
            "My current situation",
            "A team or organization",
            "An operational process",
            "An abstract system",
        ],
    )

    persistence = st.selectbox(
        "Are the conditions creating strain expected to persist?",
        [
            "Likely temporary",
            "Likely persistent",
            "Unclear",
        ],
    )

    if st.button("Start"):
        st.session_state.system_type = system_type
        st.session_state.persistence = persistence
        st.session_state.stage = "questions"
        st.experimental_rerun()

# -----------------------------
# QUESTION LOOP
# -----------------------------
elif st.session_state.stage == "questions":
    q = QUESTIONS[st.session_state.current_q]

    st.subheader(f"Question {st.session_state.current_q + 1}")
    st.write(q["prompt"])

    choice = st.radio(
        "Select the option closest to what typically happens:",
        q["options"],
        index=None,
    )

    if choice:
        if st.button("Continue"):
            st.session_state.responses.append(
                {
                    "question_id": q["id"],
                    "response": choice,
                }
            )
            st.session_state.current_q += 1

            if st.session_state.current_q >= MAX_QUESTIONS:
                st.session_state.stage = "summary"

            st.experimental_rerun()

# -----------------------------
# SUMMARY + DOWNLOAD
# -----------------------------
elif st.session_state.stage == "summary":
    st.title("Snapshot Summary")

    st.markdown(
        """
        This snapshot reflects how strain appears to concentrate
        under the conditions you described.
        """
    )

    st.write("**System evaluated:**", st.session_state.system_type)
    st.write("**Condition persistence:**", st.session_state.persistence)
    st.write("**Questions answered:**", len(st.session_state.responses))

    st.markdown(
        """
        **Interpretation (v1):**
        - This is a baseline orientation, not a conclusion.
        - Repeating this check after changes can reveal drift or relief.
        """
    )

    snapshot = {
        "timestamp": datetime.utcnow().isoformat(),
        "system_type": st.session_state.system_type,
        "persistence": st.session_state.persistence,
        "responses": st.session_state.responses,
    }

    snapshot_json = json.dumps(snapshot, indent=2)

    st.download_button(
        label="Save this snapshot",
        data=snapshot_json,
        file_name="configuration_snapshot.json",
        mime="application/json",
    )

    if st.button("Start over"):
        st.session_state.clear()
        st.experimental_rerun()
