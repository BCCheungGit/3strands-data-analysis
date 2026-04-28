# 3Strands-Data-Analysis
Data analysis for [3Strands](https://threestrandssocial.online)

---

# Project Structure
```
3Strands-Data-Analyais/
├── config/
│   └── weights.json       # Question weights and scale ranges
│   └── survey_responses.xlsx       # Excel that contains the survey responses, used in batch mode 
├── data/
│   ├── scores.csv         # Auto-generated, persists all scores
├── results/
│   └── tables.xlsx        # Batch output of assigned tables for all respondents 
├── loader.py              # Reads and validates the Excel survey file
├── matcher.py             # Score calculation and table assignment logic
├── store.py               # Persists scores to CSV, triggers reassignment
├── output.py              # Terminal display and Excel export
└── main.py                # Entry point
```

---

# Setup
1. Clone the repository:
    ```bash
    git clone
    ```
2. Install dependencies:
    ```bash
    pip install pandas openpyxl numpy
    ```
3. Configure weights and scale ranges in `config/weights.json`.
4. Place the survey responses Excel file in `config/survey_responses.xlsx` (if using batch mode).

---

# Usage

## Live mode — one person at a time

FOR NOW: 
Edit the `user_id` and `responses` in `main.py` then run:
 
```bash
python main.py
```

- [ ] Future: add ui to input responses live, then calculate and display results immediately.
 
Each run saves the person's score and reprints updated table assignments.
 
## Batch mode — full Excel file at once
 
Your Excel file must have a `user_id` column and one column per question (named to match `weights.json`):
 
| user_id | q1_values_alignment | q2_communication_style | ... |
|---------|--------------------|-----------------------|-----|
| alice   | 5                  | 3                     | ... |
| bob     | 4                  | 4                     | ... |
 
Then run:
 
```bash
python main.py config/survey_responses.xlsx
```
 
---



