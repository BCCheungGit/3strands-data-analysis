import pandas as pd


def load_survey(path: str, config: dict) -> pd.DataFrame:
    """
    Loads survey responses from an Excel file.

    Expects the file to have:
      - A 'user_id' column identifying each respondent
      - A 'name' column identifying each respondent by name
      - An 'age' column identifying each respondent's age
      - One column per question, named to match the keys in config

    Args:
        path:   Path to the .xlsx file
        config: Nested dict from weights.json, keyed by question name

    Returns:
        DataFrame with user_id + question columns, nulls dropped
    """
    df = pd.read_excel(path)

    identity_cols = ["user_id", "name", "age"]
    question_cols = list(config.keys())
    required_cols = identity_cols + question_cols

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in spreadsheet: {missing}")
    df = pd.DataFrame(df[required_cols]).dropna()

    return df
