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

Format of excel file:
 
| Timestamp        | Name        | Age | Email               |  q1_values_alignment | q2_communication_style | ... |
|------------------|-------------|-----|---------------------|----------------------|------------------------|-----|
|1/16/2026 17:18:14| alice chen  |25   | alicechen@gmail.com | 5                    | 3                      | ... |
|1/16/2026 17:23:14| bob wong    |30   | bobwong@gmail.com   | 4                    | 4                      | ... |
 
Then run:
 
```bash
python main.py config/survey_responses.xlsx
```
 
---

## How scoring works
 
1. Each response is normalized to 0–1 using its own scale: `(value - scale_min) / (scale_max - scale_min)`
2. The normalized value is multiplied by the question's weight
3. The weighted sum is divided by the total weight and scaled to 0–100
This means questions with more weight pull the final score more, and different scale lengths don't skew results.

Most of the scoring logic can be found in `matcher.py`, and the weights/scales are defined in `config/weights.json`.

---
 
## How table assignment works
 
1. All participants are sorted by score
2. Groups of 4 (or your chosen `table_size`) are taken in order — so the most similar scores sit together
3. If the last group is incomplete, those people are merged into the previous table
4. Every time a new person submits, all assignments are recomputed
Table assignments should be considered provisional until registration closes.

