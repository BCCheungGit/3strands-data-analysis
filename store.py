import csv
import os
from datetime import datetime

from matcher import assign_tables

SCORES_FILE = "data/scores.csv"


# Save the user's score to a CSV file with a timestamp
def save_score(user_id: str, score: float):
    file_exists = os.path.exists(SCORES_FILE)
    with open(SCORES_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "score", "timestamp"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "user_id": user_id,
                "score": score,
                "timestamp": datetime.now().isoformat(),
            }
        )


# Load all scores from the CSV file and return them as a list of dictionaries
def load_scores() -> list[dict]:
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


# This function adds a new participant's score, loads all scores, and reassigns tables based on the updated scores.
def add_participant_and_reassign(user_id: str, score: float) -> list[dict]:
    save_score(user_id, score)
    all_scores = load_scores()
    return assign_tables(all_scores)
