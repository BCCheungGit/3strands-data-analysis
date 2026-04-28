"""
3strands-data-analysis / main.py
------------------------
Two ways to use this script:

  1. LIVE MODE (default)
     Simulates a single person submitting the survey.
     Scores them, saves to data/scores.csv, and recomputes table assignments.
     Will be used when people are filling in the survey one at a time.

  2. BATCH MODE
     Pass the path to a completed Excel survey file as a command-line argument.
     Scores everyone at once and assigns tables.

     python main.py data/survey_responses.xlsx
"""

import json
import sys

from matcher import compute_score
from output import export_from_batch, export_tables, print_tables
from store import add_participant_and_reassign


def load_config(path: str = "config/weights.json") -> dict:
    with open(path) as f:
        return json.load(f)


# ── BATCH MODE ────────────────────────────────────────────────────────────────
if len(sys.argv) > 1:
    survey_path = sys.argv[1]
    config = load_config()
    print(f"Batch mode: processing {survey_path}")
    export_from_batch(survey_path, config, table_size=4)
    sys.exit(0)


# ── LIVE MODE ─────────────────────────────────────────────────────────────────
config = load_config()

# Replace these with real input from your survey form / CLI prompt
user_id = "alice"
responses = {
    "q1_values_alignment": 5,
    "q2_communication_style": 3,
    "q3_lifestyle_pace": 4,
    "q4_yes_no_question": 2,
    "q5_humor": 4,
}

# 1. Compute score
score = compute_score(responses, config)
print(f"\n{user_id}'s compatibility score: {score}/100")

# 2. Save and get updated table assignments
assignments = add_participant_and_reassign(user_id, score, table_size=4)

# 3. Show and export
print_tables(assignments)
export_tables(assignments)
