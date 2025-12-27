{
  "version": 1,
  "title": "Capacity & Strain (Higher = Worse)",
  "items": [
    {
      "id": "Q1",
      "type": "choice",
      "domain": "capacity",
      "construct": "load_vs_capacity",
      "prompt": "When demands increase faster than available capacity, what happens first?",
      "choices": [
        "Effort is redistributed internally",
        "Non-essential activity is deferred",
        "Output quality becomes uneven",
        "Short-term throughput is prioritized",
        "Coordination becomes harder"
      ],
      "weights": {
        "Effort is redistributed internally": 2,
        "Non-essential activity is deferred": 3,
        "Output quality becomes uneven": 4,
        "Short-term throughput is prioritized": 4,
        "Coordination becomes harder": 5
      }
    },
    {
      "id": "Q2",
      "type": "choice",
      "domain": "feedback",
      "construct": "feedback_latency",
      "prompt": "When results are slow to appear, how does the system proceed?",
      "choices": [
        "It continues based on prior assumptions",
        "It pauses to reassess direction",
        "It seeks informal signals",
        "It increases activity to compensate",
        "It narrows focus to fewer actions"
      ],
      "weights": {
        "It continues based on prior assumptions": 3,
        "It pauses to reassess direction": 2,
        "It seeks informal signals": 2,
        "It increases activity to compensate": 4,
        "It narrows focus to fewer actions": 3
      }
    },
    {
      "id": "Q3",
      "type": "choice",
      "domain": "coherence",
      "construct": "effort_to_progress",
      "prompt": "When effort does not reliably translate into progress, what emerges?",
      "choices": [
        "Process refinement",
        "Frustration without action",
        "Experimentation",
        "Reduced engagement",
        "Overextension"
      ],
      "weights": {
        "Process refinement": 2,
        "Frustration without action": 4,
        "Experimentation": 2,
        "Reduced engagement": 5,
        "Overextension": 4
      }
    },
    {
      "id": "Q4",
      "type": "choice",
      "domain": "control",
      "construct": "constraint_clarity",
      "prompt": "When constraints are unclear, what tends to change first?",
      "choices": [
        "Decision speed",
        "Confidence in choices",
        "Internal coordination",
        "Willingness to commit",
        "Attention distribution"
      ],
      "weights": {
        "Decision speed": 3,
        "Confidence in choices": 4,
        "Internal coordination": 5,
        "Willingness to commit": 4,
        "Attention distribution": 3
      }
    },
    {
      "id": "Q5",
      "type": "choice",
      "domain": "persistence",
      "construct": "sustained_strain",
      "prompt": "When strain persists without a clear endpoint, what shifts first?",
      "choices": [
        "Energy allocation",
        "Error tolerance",
        "Planning horizon",
        "Communication clarity",
        "Internal alignment"
      ],
      "weights": {
        "Energy allocation": 4,
        "Error tolerance": 3,
        "Planning horizon": 5,
        "Communication clarity": 4,
        "Internal alignment": 5
      }
    },
    {
      "id": "Q6",
      "type": "choice",
      "domain": "adaptation",
      "construct": "failed_correction",
      "prompt": "When corrective actions do not produce relief, what follows?",
      "choices": [
        "New strategies are tested",
        "Existing methods are intensified",
        "Scope is reduced",
        "Doubt increases",
        "Stability degrades"
      ],
      "weights": {
        "New strategies are tested": 2,
        "Existing methods are intensified": 4,
        "Scope is reduced": 3,
        "Doubt increases": 5,
        "Stability degrades": 5
      }
    },
    {
      "id": "Q7",
      "type": "choice",
      "domain": "recovery",
      "construct": "capacity_recovery",
      "prompt": "When recovery time shortens repeatedly, what changes?",
      "choices": [
        "Throughput",
        "Precision",
        "Risk tolerance",
        "Adaptability",
        "Sustainability"
      ],
      "weights": {
        "Throughput": 3,
        "Precision": 4,
        "Risk tolerance": 3,
        "Adaptability": 2,
        "Sustainability": 5
      }
    },
    {
      "id": "Q8",
      "type": "choice",
      "domain": "error",
      "construct": "error_accumulation",
      "prompt": "When errors accumulate faster than they can be resolved, what emerges?",
      "choices": [
        "Workarounds",
        "Process breakdown",
        "Blame shifting",
        "Increased oversight",
        "System fatigue"
      ],
      "weights": {
        "Workarounds": 3,
        "Process breakdown": 5,
        "Blame shifting": 4,
        "Increased oversight": 3,
        "System fatigue": 5
      }
    },

    {
      "id": "Q9",
      "type": "choice",
      "domain": "capacity",
      "construct": "buffer_margin",
      "prompt": "When an unexpected task arrives, what happens to the current plan?",
      "choices": [
        "Plan absorbs it with no changes",
        "Minor reshuffle and continue",
        "A key task gets delayed",
        "Multiple tasks slip at once",
        "Everything becomes reactive"
      ],
      "weights": {
        "Plan absorbs it with no changes": 1,
        "Minor reshuffle and continue": 2,
        "A key task gets delayed": 3,
        "Multiple tasks slip at once": 4,
        "Everything becomes reactive": 5
      }
    },
    {
      "id": "Q10",
      "type": "choice",
      "domain": "control",
      "construct": "decision_friction",
      "prompt": "When you need to decide fast, what blocks you first?",
      "choices": [
        "Nothing — decisions are clean",
        "Missing one key detail",
        "Too many competing priorities",
        "Second-guessing / doubt",
        "Fear of downstream consequences"
      ],
      "weights": {
        "Nothing — decisions are clean": 1,
        "Missing one key detail": 2,
        "Too many competing priorities": 4,
        "Second-guessing / doubt": 4,
        "Fear of downstream consequences": 5
      }
    },
    {
      "id": "Q11",
      "type": "choice",
      "domain": "feedback",
      "construct": "signal_quality",
      "prompt": "What is the quality of feedback you’re getting from the environment right now?",
      "choices": [
        "Clear and fast",
        "Clear but slow",
        "Mixed signals",
        "Mostly noise",
        "No feedback / blind"
      ],
      "weights": {
        "Clear and fast": 1,
        "Clear but slow": 2,
        "Mixed signals": 3,
        "Mostly noise": 4,
        "No feedback / blind": 5
      }
    },
    {
      "id": "Q12",
      "type": "choice",
      "domain": "coherence",
      "construct": "goal_alignment",
      "prompt": "How aligned are your actions with the stated goal right now?",
      "choices": [
        "Directly aligned",
        "Mostly aligned",
        "Half aligned / half distraction",
        "Mostly reactive",
        "Not aligned at all"
      ],
      "weights": {
        "Directly aligned": 1,
        "Mostly aligned": 2,
        "Half aligned / half distraction": 3,
        "Mostly reactive": 4,
        "Not aligned at all": 5
      }
    },
    {
      "id": "Q13",
      "type": "choice",
      "domain": "persistence",
      "construct": "endurance_curve",
      "prompt": "If nothing changes, how long can you sustain the current pace before something breaks?",
      "choices": [
        "Weeks+",
        "Several days",
        "1–2 days",
        "Hours",
        "Already breaking"
      ],
      "weights": {
        "Weeks+": 1,
        "Several days": 2,
        "1–2 days": 3,
        "Hours": 4,
        "Already breaking": 5
      }
    },
    {
      "id": "Q14",
      "type": "choice",
      "domain": "recovery",
      "construct": "sleep_quality",
      "prompt": "What is your recovery quality (sleep/rest) over the last 48 hours?",
      "choices": [
        "Restorative",
        "Okay",
        "Light / fragmented",
        "Poor",
        "Severely deprived"
      ],
      "weights": {
        "Restorative": 1,
        "Okay": 2,
        "Light / fragmented": 3,
        "Poor": 4,
        "Severely deprived": 5
      }
    },
    {
      "id": "Q15",
      "type": "choice",
      "domain": "error",
      "construct": "mistake_rate",
      "prompt": "Compared to normal, your mistake rate is…",
      "choices": [
        "Lower than normal",
        "Normal",
        "Slightly higher",
        "High",
        "Unmanageable"
      ],
      "weights": {
        "Lower than normal": 1,
        "Normal": 2,
        "Slightly higher": 3,
        "High": 4,
        "Unmanageable": 5
      }
    },
    {
      "id": "Q16",
      "type": "choice",
      "domain": "adaptation",
      "construct": "strategy_shift",
      "prompt": "When something fails, what is your typical next move?",
      "choices": [
        "Simplify and re-try",
        "Change one variable",
        "Add more effort",
        "Add more complexity",
        "Freeze / avoid"
      ],
      "weights": {
        "Simplify and re-try": 1,
        "Change one variable": 2,
        "Add more effort": 3,
        "Add more complexity": 4,
        "Freeze / avoid": 5
      }
    },
    {
      "id": "Q17",
      "type": "choice",
      "domain": "control",
      "construct": "boundary_integrity",
      "prompt": "How well are your boundaries holding (time, attention, obligations)?",
      "choices": [
        "Strong",
        "Mostly holding",
        "Leaking",
        "Collapsed",
        "No boundaries"
      ],
      "weights": {
        "Strong": 1,
        "Mostly holding": 2,
        "Leaking": 3,
        "Collapsed": 4,
        "No boundaries": 5
      }
    },
    {
      "id": "Q18",
      "type": "choice",
      "domain": "feedback",
      "construct": "external_validation",
      "prompt": "When you seek input, what do you get most often?",
      "choices": [
        "Actionable guidance",
        "Encouragement but no clarity",
        "Conflicting advice",
        "Dismissal / ridicule",
        "Silence"
      ],
      "weights": {
        "Actionable guidance": 1,
        "Encouragement but no clarity": 2,
        "Conflicting advice": 3,
        "Dismissal / ridicule": 4,
        "Silence": 4
      }
    },
    {
      "id": "Q19",
      "type": "choice",
      "domain": "coherence",
      "construct": "context_switching",
      "prompt": "How much context switching are you doing today?",
      "choices": [
        "Almost none",
        "Some",
        "A lot",
        "Constant",
        "Uncontrolled"
      ],
      "weights": {
        "Almost none": 1,
        "Some": 2,
        "A lot": 3,
        "Constant": 4,
        "Uncontrolled": 5
      }
    },
    {
      "id": "Q20",
      "type": "choice",
      "domain": "capacity",
      "construct": "resource_availability",
      "prompt": "Right now, do you have the resources needed to execute (tools/time/money/access)?",
      "choices": [
        "Yes, sufficient",
        "Mostly",
        "Barely",
        "No, constrained",
        "No, blocked"
      ],
      "weights": {
        "Yes, sufficient": 1,
        "Mostly": 2,
        "Barely": 3,
        "No, constrained": 4,
        "No, blocked": 5
      }
    },
    {
      "id": "Q21",
      "type": "choice",
      "domain": "persistence",
      "construct": "motivation_stability",
      "prompt": "What best describes your motivational state right now?",
      "choices": [
        "Steady",
        "Wobbly but present",
        "Driven by urgency only",
        "Mostly depleted",
        "Numb / detached"
      ],
      "weights": {
        "Steady": 1,
        "Wobbly but present": 2,
        "Driven by urgency only": 3,
        "Mostly depleted": 4,
        "Numb / detached": 5
      }
    },
    {
      "id": "Q22",
      "type": "choice",
      "domain": "recovery",
      "construct": "reset_access",
      "prompt": "If you needed to reset for 2–4 hours, could you?",
      "choices": [
        "Yes, easily",
        "Yes, with planning",
        "Maybe, with cost",
        "Unlikely",
        "No"
      ],
      "weights": {
        "Yes, easily": 1,
        "Yes, with planning": 2,
        "Maybe, with cost": 3,
        "Unlikely": 4,
        "No": 5
      }
    },
    {
      "id": "Q23",
      "type": "choice",
      "domain": "error",
      "construct": "rework_pressure",
      "prompt": "How much of today’s work is rework (fixing, redoing, repairing)?",
      "choices": [
        "Almost none",
        "Some",
        "A lot",
        "Most of it",
        "All of it"
      ],
      "weights": {
        "Almost none": 1,
        "Some": 2,
        "A lot": 3,
        "Most of it": 4,
        "All of it": 5
      }
    },
    {
      "id": "Q24",
      "type": "choice",
      "domain": "adaptation",
      "construct": "learning_loop",
      "prompt": "Are you learning fast enough to keep up with the situation?",
      "choices": [
        "Yes",
        "Mostly",
        "Unclear",
        "No, falling behind",
        "No, losing ground"
      ],
      "weights": {
        "Yes": 1,
        "Mostly": 2,
        "Unclear": 3,
        "No, falling behind": 4,
        "No, losing ground": 5
      }
    }
  ]
}
