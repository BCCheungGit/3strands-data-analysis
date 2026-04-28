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


def assign_tables(scores: list[dict], table_size: int = 4) -> list[dict]:
    """
    Sorts all participants by score and assigns them to tables.

    People with the most similar scores sit together. If the last group
    has fewer than table_size people it is merged into the previous table.

    Args:
        scores:     List of dicts with at least 'user_id' and 'score' keys
        table_size: Target number of people per table (default 4)

    Returns:
        Same list with a 'table' key added to each entry
    """
    if not scores:
        return []

    sorted_scores = sorted(scores, key=lambda x: float(x["score"]))
    total = len(sorted_scores)

    assignments = []
    for i, person in enumerate(sorted_scores):
        table_num = (i // table_size) + 1
        assignments.append({**person, "table": table_num})

    # Fold remainder into the last full table if it's an incomplete group
    remainder = total % table_size
    if remainder > 0 and total >= table_size:
        last_full_table = total // table_size
        for p in assignments:
            if p["table"] == last_full_table + 1:
                p["table"] = last_full_table

    return assignments


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
