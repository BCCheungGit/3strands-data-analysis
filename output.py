import os
from itertools import groupby

import pandas as pd

from matcher import get_table_summary


def export_from_batch(path: str, config: dict, table_size: int = 4) -> None:
    from loader import load_survey
    from matcher import assign_rounds, compute_score

    df = load_survey(path, config)
    question_cols = list(config.keys())

    scored = []
    for _, row in df.iterrows():
        responses = {q: row[q] for q in question_cols}
        score = compute_score(responses, config)
        gender = row.get("gender", "U")
        scored.append({"user_id": row["user_id"], "score": score, "gender": gender})

    all_rounds = assign_rounds(scored, table_size=table_size)
    print_all_rounds(all_rounds)
    export_all_rounds(all_rounds)


def print_all_rounds(all_rounds: dict) -> None:
    for round_num, assignments in all_rounds.items():
        print(f"\n{'='*55}")
        print(f"  ROUND {round_num}")
        print(f"{'='*55}")
        sorted_a = sorted(assignments, key=lambda x: x["table"])
        for table_num, members in groupby(sorted_a, key=lambda x: x["table"]):
            members = list(members)
            avg = sum(float(m["score"]) for m in members) / len(members)
            print(f"\n  Table {table_num}  (avg score: {avg:.1f})")
            print(f"  {'-'*45}")
            for m in members:
                gender_label = "♂" if m["gender"].upper() == "M" else "♀"
                print(
                    f"  {gender_label} {str(m['user_id']):20s}  score: {float(m['score']):.1f}"
                )


def export_all_rounds(all_rounds: dict, path: str = "results/rounds.xlsx") -> None:
    import pandas as pd

    os.makedirs(os.path.dirname(path), exist_ok=True)
    rows = []
    for round_num, assignments in all_rounds.items():
        for p in assignments:
            rows.append(
                {
                    "round": round_num,
                    "table": p["table"],
                    "user_id": p["user_id"],
                    "gender": p["gender"],
                    "score": float(p["score"]),
                }
            )
    df = pd.DataFrame(rows).sort_values(["round", "table", "gender", "score"])
    df.to_excel(path, index=False)
    print(f"Round assignments saved to {path}")
