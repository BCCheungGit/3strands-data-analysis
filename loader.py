import pandas as pd


def load_survey(path: str, config: dict) -> pd.DataFrame:
    """
    Loads survey responses from an Excel file.

    Expects the file to have:
      - A 'user_id' column identifying each respondent
      - One column per question, named to match the keys in config

    Args:
        path:   Path to the .xlsx file
        config: Nested dict from weights.json, keyed by question name

    Returns:
        DataFrame with user_id + question columns, nulls dropped
    """
    df = pd.read_excel(path)

    question_cols = list(config.keys())
    missing = [c for c in ["user_id"] + question_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in spreadsheet: {missing}")

    df = pd.DataFrame(df[["user_id"] + question_cols]).dropna()
    return df
