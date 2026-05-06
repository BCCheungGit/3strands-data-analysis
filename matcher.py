from itertools import groupby


def compute_score(responses: dict, config: dict) -> float:
    """
    Converts a person's Likert responses into a single 0-100 score.

    Each response is normalized to 0-1 using its own scale range before
    the weight is applied. This ensures questions with different numbers
    of options (e.g. 1-2 vs 1-7) are compared fairly.

    Args:
        responses: {"q1_values_alignment": 4, "q4_yes_no_question": 2, ...}
        config:    {"q1_values_alignment": {"weight": 3.0, "scale_min": 1, "scale_max": 5}, ...}

    Returns:
        Float score between 0.0 and 100.0
    """
    weighted_sum = 0.0
    total_weight = 0.0

    for q, value in responses.items():
        if q not in config:
            raise KeyError(f"Question '{q}' not found in config.")

        q_config = config[q]
        weight = q_config["weight"]
        scale_min = q_config["scale_min"]
        scale_max = q_config["scale_max"]

        if scale_max == scale_min:
            raise ValueError(
                f"Question '{q}' has scale_min == scale_max. Check weights.json."
            )

        # Normalize this response to 0-1 relative to its own scale
        normalized = (value - scale_min) / (scale_max - scale_min)

        # Clamp to [0, 1] in case of out-of-range input
        normalized = max(0.0, min(1.0, normalized))

        weighted_sum += normalized * weight
        total_weight += weight

    if total_weight == 0:
        raise ValueError("Total weight is zero. Check weights.json.")

    return round((weighted_sum / total_weight) * 100, 2)


def assign_rounds(
    scores: list[dict], table_size: int = 4, num_rounds: int = 4
) -> dict[int, list[dict]]:
    """
    Splits participants by gender, sorts each group by score,
    then rotates female assignments each round so people meet
    different partners while staying score-similar.

    Each table seats (table_size // 2) males + (table_size // 2) females.
    Returns: {round_num: [{"table": int, "user_id": ..., "gender": ..., "score": ...}]}
    """

    for i, entry in enumerate(scores):
        if "gender" not in entry:
            print(
                f"Error at index {i}: Missing 'gender' key. Available keys: {entry.keys()}"
            )
    males = sorted(
        [p for p in scores if p["gender"].upper() == "M"],
        key=lambda x: float(x["score"]),
    )
    females = sorted(
        [p for p in scores if p["gender"].upper() == "F"],
        key=lambda x: float(x["score"]),
    )

    if not males or not females:
        raise ValueError("Need at least one male and one female participant.")

    # Balance group sizes by trimming to the smaller group
    # (you can change this to keep extras in a waiting list instead)
    min_size = min(len(males), len(females))
    males = males[:min_size]
    females = females[:min_size]

    half = table_size // 2  # e.g. 2 males + 2 females per table
    all_rounds = {}

    for round_num in range(1, num_rounds + 1):
        # Rotate females by (round_num - 1) * half positions
        # so each round produces a different pairing
        rotation = ((round_num - 1) * half) % min_size
        rot_females = females[rotation:] + females[:rotation]

        # Interleave: [M1, M2, F1, F2, M3, M4, F3, F4, ...]
        # then chunk into tables
        combined = []
        for i in range(min_size):
            combined.append(males[i])
            combined.append(rot_females[i])

        # Group into tables of table_size
        assignments = []
        table_num = 1
        for i in range(0, len(combined), table_size):
            chunk = combined[i : i + table_size]
            # If last chunk is too small, merge into previous table
            if len(chunk) < table_size and assignments:
                for p in chunk:
                    assignments[-1]["members"] if False else None
                    assignments.append({**p, "table": table_num - 1})
            else:
                for p in chunk:
                    assignments.append({**p, "table": table_num})
                table_num += 1

        all_rounds[round_num] = assignments

    return all_rounds


def get_table_summary(assignments: list[dict]) -> list[dict]:
    """
    Returns a summary of each table: table number, members, and average score.

    Args:
        assignments: Output of assign_tables()

    Returns:
        List of dicts: {"table": int, "members": [...], "avg_score": float}
    """
    sorted_a = sorted(assignments, key=lambda x: x["table"])
    summary = []

    for table_num, members in groupby(sorted_a, key=lambda x: x["table"]):
        members = list(members)
        avg = sum(float(m["score"]) for m in members) / len(members)
        summary.append(
            {"table": table_num, "members": members, "avg_score": round(avg, 2)}
        )

    return summary
