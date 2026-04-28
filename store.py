import csv
import os
from datetime import datetime

SCORES_FILE = "data/scores.csv"
FIELDNAMES = ["user_id", "score", "timestamp"]


def save_score(user_id: str, score: float) -> None:
    """
    Appends a participant's score to the scores CSV.
    Creates the file and header if it doesn't exist yet.
    Updates the score if the user_id already exists.

    Args:
        user_id: Unique identifier for the participant
        score:   Computed compatibility score (0-100)
    """
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)

    existing = load_scores()
    updated = False

    for row in existing:
        if row["user_id"] == user_id:
            row["score"] = score
            row["timestamp"] = datetime.now().isoformat()
            updated = True
            break

    if updated:
        # Rewrite entire file
        with open(SCORES_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(existing)
    else:
        # Append new row
        file_exists = os.path.exists(SCORES_FILE)
        with open(SCORES_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            writer.writerow(
                {
                    "user_id": user_id,
                    "score": score,
                    "timestamp": datetime.now().isoformat(),
                }
            )


def load_scores() -> list[dict]:
    """
    Loads all saved scores from the CSV.

    Returns:
        List of dicts with user_id, score, and timestamp keys.
        Returns an empty list if the file doesn't exist yet.
    """
    if not os.path.exists(SCORES_FILE):
        return []

    with open(SCORES_FILE, "r") as f:
        return list(csv.DictReader(f))


def add_participant_and_reassign(
    user_id: str, score: float, table_size: int = 4
) -> list[dict]:
    """
    Saves a participant's score and immediately recomputes all table assignments.

    Args:
        user_id:    Unique identifier for the participant
        score:      Computed compatibility score (0-100)
        table_size: Target seats per table

    Returns:
        Full updated table assignments for all participants
    """
    from matcher import assign_tables

    save_score(user_id, score)
    all_scores = load_scores()
    return assign_tables(all_scores, table_size=table_size)
