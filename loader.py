import pandas as pd


def load_survey(path: str, config: dict) -> pd.DataFrame:
    """
    Loads survey responses from an Excel file.

    Expects the file to have:
      - A 'timestamp' column with the submission time
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

    df.columns = df.columns.str.lower()

    if "user_id" not in df.columns:
        if "name" not in df.columns or "timestamp" not in df.columns:
            raise ValueError(
                "Spreadsheet must have either 'user_id' column or both 'name' and 'timestamp' columns."
            )
        # Formats the timestamp to be more compact and consistent, removing spaces and special characters
        # Then creates a user_id by combining the name and formatted timestamp, ensuring unique identifiers for each respondent
        df["user_id"] = (
            df["name"].astype(str).str.strip()
            + "_"
            + pd.to_datetime(df["timestamp"]).dt.strftime("%Y%m%d_%H%M%S")
        )

    identity_cols = ["user_id", "name", "age", "email"]
    question_cols = list(config.keys())
    required_cols = identity_cols + question_cols

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in spreadsheet: {missing}")
    df = pd.DataFrame(df[required_cols]).dropna()

    return df
