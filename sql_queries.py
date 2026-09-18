import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///data/edu_loan.db')

# ============================================================
# 10 KEY SQL QUERIES (BUSINESS QUESTIONS)
# ============================================================
queries = {

    "Q1: Which bank has the lowest rate?": """
        SELECT bank, scheme_name, interest_rate
        FROM schemes
        ORDER BY interest_rate ASC
        LIMIT 1;
    """,

    "Q2: Which bank has the highest rate?": """
        SELECT bank, scheme_name, interest_rate
        FROM schemes
        ORDER BY interest_rate DESC
        LIMIT 1;
    """,

    "Q3: Average rate per bank": """
        SELECT bank,
               COUNT(*) AS total_schemes,
               ROUND(AVG(interest_rate), 2) AS avg_rate,
               ROUND(MIN(interest_rate), 2) AS min_rate,
               ROUND(MAX(interest_rate), 2) AS max_rate
        FROM schemes
        GROUP BY bank
        ORDER BY avg_rate ASC;
    """,

    "Q4: Banks with no-collateral loans": """
        SELECT bank, scheme_name, interest_rate, max_loan_amount
        FROM schemes
        WHERE LOWER(collateral_needed) LIKE '%no%'
        ORDER BY interest_rate ASC;
    """,

    "Q5: Public vs Private average rate": """
        SELECT bank_type,
               ROUND(AVG(interest_rate), 2) AS avg_rate,
               COUNT(*) AS schemes
        FROM schemes
        GROUP BY bank_type;
    """,

    "Q6: Which banks offer abroad loans?": """
        SELECT bank, scheme_name, interest_rate, max_loan_amount
        FROM schemes
        WHERE study_destination = 'Abroad'
        ORDER BY interest_rate ASC;
    """,

    "Q7: Bank-wise scheme count": """
        SELECT bank, COUNT(*) AS scheme_count
        FROM schemes
        GROUP BY bank
        ORDER BY scheme_count DESC;
    """,

    "Q8: Highest loan amount by bank": """
        SELECT bank,
               MAX(max_loan_amount) AS max_loan,
               ROUND(MIN(interest_rate), 2) AS best_rate
        FROM schemes
        GROUP BY bank
        ORDER BY max_loan DESC;
    """,

    "Q9: Zero processing fee schemes": """
        SELECT bank, scheme_name, interest_rate
        FROM schemes
        WHERE processing_fee_percent = 0
        ORDER BY interest_rate ASC;
    """,

    "Q10: Rate trend over 6 months": """
        SELECT bank,
               ROUND(MIN(interest_rate), 2) AS earliest,
               ROUND(MAX(interest_rate), 2) AS latest,
               ROUND(MAX(interest_rate) - MIN(interest_rate), 2) AS change
        FROM historical_rates
        GROUP BY bank;
    """,
}

# ============================================================
# EXECUTE ALL QUERIES
# ============================================================
print("="*70)
print("SQL BUSINESS QUERIES — RESULTS")
print("="*70)

for title, query in queries.items():
    print(f"\n📊 {title}")
    print("-" * 60)
    result = pd.read_sql(text(query), engine)
    print(result.to_string(index=False))
    print()
