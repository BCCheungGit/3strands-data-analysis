# Contains the core logic for matching the users
# Uses weighted Cosine Similarity distance matcher.
# Each person becomes a numerical vector of their Likert responses, and
# pathwise similarity scores are calculated between the users, each dimension
# scaled by its importance in weight.

from itertools import combinations

import numpy as np


# Element-wise multiplication between a person's Likert responses and importance weights.
# This allows us to represent each person as a weighted vector and perform linear algebra
# operations on their responses.
def weighted_vector(row: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return row * weights


# measures the angle between two vectors, giving a similarity score between 0 and 1.
# A score of 1 means the vectors are identical, while a score of 0 means completely orthogonal.
# TODO: consider using a different distance metric, such as Euclidean distance or Manhattan distance.
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return (
        float(np.dot(a, b) / denom) if denom else 0.0
    )  # guard against division by zero


# Takes in the user data and importance weights, computes the weighted vectors for each user,
# and calculates the cosine similarity between all pairs of users. The results are returned
# as a dictionary mapping each user ID (maybe name) to a list of their top N most similar matches,
# along with their similarity scores.
def compute_matches(df, weights: dict, top_n: int = 5) -> dict:
    weight_vec = np.array(list(weights.values()))
    question_cols = list(weights.keys())
    vectors = {
        row["user_id"]: weighted_vector(
            row[question_cols].values.astype(float), weight_vec
        )
        for _, row in df.iterrows()
    }
    ids = list(vectors.keys())
    scores = []
    for a, b in combinations(ids, 2):
        score = cosine_similarity(vectors[a], vectors[b])
        scores.append({"person_a": a, "person_b": b, "similarity": score})
    results = {}
    for id in ids:
        person_scores = [
            s for s in scores if s["person_a"] == id or s["person_b"] == id
        ]
        person_scores.sort(key=lambda x: x["score"], reverse=True)
        results[id] = person_scores[:top_n]
    return results


# This function takes the output of compute_matches and filters it to include only mutual matches.
def mutual_matches(matches: dict) -> list[dict]:
    seen = set()
    mutual = []
    for person, top in matches.items():
        for match in top:
            other = (
                match["person_b"] if match["person_a"] == person else match["person_a"]
            )
            pair = tuple(sorted((person, other)))
            if pair not in seen:
                other_tops = [
                    (
                        match2["person_b"]
                        if match2["person_a"] == other
                        else match2["person_a"]
                    )
                    for match2 in matches[other]
                ]
                if person in other_tops:
                    mutual.append(
                        {
                            "person_a": pair[0],
                            "person_b": pair[1],
                            "score": match["score"],
                        }
                    )
                    seen.add(pair)
    return mutual
