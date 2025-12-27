
import streamlit as st
from pathlib import Path
import json
import engine

st.set_page_config(page_title="Capacity & Strain Test", layout="centered")

base = Path(__file__).resolve().parent
questions_path = base / "questions.json"

st.title("Capacity & Strain Test")

questions = engine.load_questions(questions_path)

answers = {}
for q in questions["items"]:
    answers[q["id"]] = st.radio(q["prompt"], q["choices"], key=q["id"])

if st.button("Submit"):
    results = engine.compute_results(questions, answers)
    st.write(results)
