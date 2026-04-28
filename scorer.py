# Contains the logic for giving users a weighted score rather than directly matching them to a specific table.


# This function computes a weighted score based on user responses and predefined weights for each question.
def compute_score(responses: dict, weights: dict, scale_max: int = 5) -> float:
    weighted_sum = sum(
        responses[question] * weights[question] for question in responses
    )
    max_possible = sum(scale_max * weights for weights in weights.values())
    return round((weighted_sum / max_possible) * 100, 2)
