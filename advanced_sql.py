import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///data/edu_loan.db')

def run(title, query, desc=""):
    print("\n" + "="*70)
    print(f"📊 {title}")
    if desc: print(f"   {desc}")
    print("-"*70)
    result = pd.read_sql(text(query), engine)
    print(result.to_string(index=False))
    print()

# ============================================================
# 1. WINDOW FUNCTION — RANK banks by average rate
# ============================================================
run("1. Bank Ranking by Average Rate (Window Function)",
    """
    SELECT 
        bank,
        ROUND(AVG(interest_rate), 2) AS avg_rate,
        RANK() OVER (ORDER BY AVG(interest_rate) ASC) AS rank
    FROM schemes
    GROUP BY bank
    ORDER BY rank;
    """,
    "Uses: RANK() OVER — window function")

# ============================================================
# 2. ROW_NUMBER — Top 2 cheapest schemes per bank
# ============================================================
run("2. Top 2 Cheapest Schemes per Bank (ROW_NUMBER)",
    """
    SELECT bank, scheme_name, interest_rate, rn
    FROM (
        SELECT 
            bank,
            scheme_name,
            interest_rate,
            ROW_NUMBER() OVER (PARTITION BY bank ORDER BY interest_rate ASC) AS rn
        FROM schemes
    )
    WHERE rn <= 2
    ORDER BY bank, rn;
    """,
    "Uses: ROW_NUMBER() OVER PARTITION BY")

# ============================================================
# 3. CTE — Common Table Expression for avg comparison
# ============================================================
run("3. Banks Below Market Average (CTE)",
    """
    WITH market_avg AS (
        SELECT AVG(interest_rate) AS avg_rate FROM schemes
    )
    SELECT 
        bank,
        scheme_name,
        interest_rate,
        ROUND((SELECT avg_rate FROM market_avg), 2) AS market_avg,
        ROUND(interest_rate - (SELECT avg_rate FROM market_avg), 2) AS diff
    FROM schemes
    WHERE interest_rate < (SELECT avg_rate FROM market_avg)
    ORDER BY interest_rate ASC;
    """,
    "Uses: WITH clause (CTE)")

# ============================================================
# 4. CASE WHEN — Rate categorization
# ============================================================
run("4. Rate Category Analysis (CASE WHEN)",
    """
    SELECT 
        bank,
        scheme_name,
        interest_rate,
        CASE 
            WHEN interest_rate < 7.5 THEN 'Excellent'
            WHEN interest_rate < 9 THEN 'Good'
            WHEN interest_rate < 11 THEN 'Moderate'
            ELSE 'High'
        END AS rate_category
    FROM schemes
    ORDER BY interest_rate ASC;
    """,
    "Uses: CASE WHEN conditional logic")

# ============================================================
# 5. HAVING — Banks with more than 2 schemes
# ============================================================
run("5. Banks with Multiple Schemes (HAVING)",
    """
    SELECT 
        bank,
        COUNT(*) AS total_schemes,
        ROUND(AVG(interest_rate), 2) AS avg_rate
    FROM schemes
    GROUP BY bank
    HAVING COUNT(*) >= 3
    ORDER BY total_schemes DESC;
    """,
    "Uses: HAVING clause")

# ============================================================
# 6. SUBQUERY — Schemes cheaper than HDFC average
# ============================================================
run("6. Schemes Cheaper than HDFC Average (Subquery)",
    """
    SELECT bank, scheme_name, interest_rate
    FROM schemes
    WHERE interest_rate < (
        SELECT AVG(interest_rate) FROM schemes WHERE bank = 'HDFC Bank'
    )
    ORDER BY interest_rate ASC;
    """,
    "Uses: Subquery in WHERE clause")

# ============================================================
# 7. SELF JOIN — Compare schemes within same bank
# ============================================================
run("7. Rate Spread Within Each Bank (Self Join)",
    """
    SELECT 
        a.bank,
        ROUND(MIN(a.interest_rate), 2) AS min_rate,
        ROUND(MAX(b.interest_rate), 2) AS max_rate,
        ROUND(MAX(b.interest_rate) - MIN(a.interest_rate), 2) AS spread
    FROM schemes a
    JOIN schemes b ON a.bank = b.bank
    GROUP BY a.bank
    ORDER BY spread DESC;
    """,
    "Uses: Self Join")

# ============================================================
# 8. UNION — Combine India and Abroad schemes
# ============================================================
run("8. India vs Abroad Scheme Comparison (UNION)",
    """
    SELECT bank, scheme_name, interest_rate, 'India' AS category
    FROM schemes WHERE study_destination = 'India'
    UNION
    SELECT bank, scheme_name, interest_rate, 'Abroad' AS category
    FROM schemes WHERE study_destination = 'Abroad'
    ORDER BY category, interest_rate ASC;
    """,
    "Uses: UNION to combine results")

# ============================================================
# 9. LAG — Rate change over time
# ============================================================
run("9. Month-over-Month Rate Change (LAG)",
    """
    SELECT 
        bank,
        date,
        interest_rate,
        LAG(interest_rate) OVER (PARTITION BY bank ORDER BY date) AS prev_rate,
        ROUND(interest_rate - LAG(interest_rate) OVER (PARTITION BY bank ORDER BY date), 3) AS change
    FROM historical_rates
    WHERE bank = 'SBI'
    ORDER BY date
    LIMIT 10;
    """,
    "Uses: LAG() window function")

# ============================================================
# 10. PERCENTAGE — Rate change percentage
# ============================================================
run("10. Rate Change Percentage Over 6 Months",
    """
    SELECT 
        bank,
        ROUND(MIN(interest_rate), 2) AS earliest,
        ROUND(MAX(interest_rate), 2) AS latest,
        ROUND((MAX(interest_rate) - MIN(interest_rate)) / MIN(interest_rate) * 100, 2) AS pct_change
    FROM historical_rates
    GROUP BY bank
    ORDER BY pct_change DESC;
    """,
    "Uses: Percentage calculation")

print("="*70)
print("✅ ALL ADVANCED SQL QUERIES EXECUTED")
print("="*70)
