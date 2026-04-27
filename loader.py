import pandas as pd


def load_survey(path: str, weights: dict) -> pd.DataFrame:
    df = pd.read_excel(path)
    question_cols = list(weights.keys())
    df = pd.DataFrame(df[["user_id"] + question_cols].dropna())
    return df
