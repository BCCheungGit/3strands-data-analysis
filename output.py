import os

import pandas as pd

from matcher import get_table_summary


def print_tables(assignments: list[dict]) -> None:
    """
    Prints a formatted table summary to the terminal.

    Args:
        assignments: Output of assign_tables() or add_participant_and_reassign()
    """
    if not assignments:
        print("No participants yet.")
        return

    summary = get_table_summary(assignments)

    print("\n" + "=" * 50)
    print(f"  TABLE ASSIGNMENTS  ({len(assignments)} participants)")
    print("=" * 50)

    for table in summary:
        print(f"\nTable {table['table']}  (avg score: {table['avg_score']:.1f})")
        print("-" * 40)
        for m in table["members"]:
            print(f"  {str(m['user_id']):20s}  score: {float(m['score']):.1f}")

    print("\n" + "=" * 50)


def export_tables(assignments: list[dict], path: str = "results/tables.xlsx") -> None:
    """
    Exports the current table assignments to an Excel file.

    Columns: table, user_id, score, timestamp
    Sorted by table number then score.

    Args:
        assignments: Output of assign_tables() or add_participant_and_reassign()
        path:        Output file path
    """
    if not assignments:
        print("Nothing to export — no participants yet.")
        return

    os.makedirs(os.path.dirname(path), exist_ok=True)

    df = pd.DataFrame(assignments)

    # Ensure consistent column order
    cols = ["table", "user_id", "email", "score", "timestamp"]
    cols = [c for c in cols if c in df.columns]
    df = df[cols].sort_values(["table", "score"])

    df.to_excel(path, index=False)
    print(f"Table assignments saved to {path}")


def export_from_batch(path: str, config: dict, table_size: int = 4) -> None:
    """
    Convenience function: loads a full Excel survey file, scores everyone,
    assigns tables, and exports results. Use this for batch/offline processing.

    Args:
        path:       Path to the survey Excel file
        config:     Loaded weights.json config dict
        table_size: Target seats per table
    """
    from loader import load_survey
    from matcher import assign_tables, compute_score

    df = load_survey(path, config)
    question_cols = list(config.keys())

    scored = []
    for _, row in df.iterrows():
        responses = {q: row[q] for q in question_cols}
        score = compute_score(responses, config)
        scored.append({"user_id": row["user_id"], "score": score})

    assignments = assign_tables(scored, table_size=table_size)
    print_tables(assignments)
    export_tables(assignments)
