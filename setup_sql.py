import pandas as pd
from sqlalchemy import create_engine, text

# ============================================================
# 1. LOAD EXCEL DATA
# ============================================================
print("Loading Excel data...")
df = pd.read_excel('data/cleaned/cleaned_all_banks.xlsx')
hist = pd.read_excel('data/raw/historical_rates.xlsx')

# ============================================================
# 2. CREATE SQLITE DATABASE
# ============================================================
engine = create_engine('sqlite:///data/edu_loan.db')
print("SQLite database created: data/edu_loan.db")

# ============================================================
# 3. LOAD DATA INTO SQL TABLES
# ============================================================
df.to_sql('schemes', engine, if_exists='replace', index=False)
hist.to_sql('historical_rates', engine, if_exists='replace', index=False)

print(f"Loaded {len(df)} rows into 'schemes' table")
print(f"Loaded {len(hist)} rows into 'historical_rates' table")

# ============================================================
# 4. VERIFY WITH SQL QUERIES
# ============================================================
print("\n" + "="*60)
print("VERIFICATION QUERIES")
print("="*60)

with engine.connect() as conn:
    # Count banks
    result = conn.execute(text("SELECT COUNT(DISTINCT bank) FROM schemes"))
    print(f"\n1. Total banks: {result.fetchone()[0]}")

    # Count schemes
    result = conn.execute(text("SELECT COUNT(*) FROM schemes"))
    print(f"2. Total schemes: {result.fetchone()[0]}")

    # Average rate
    result = conn.execute(text("SELECT AVG(interest_rate) FROM schemes"))
    print(f"3. Average rate: {result.fetchone()[0]:.2f}%")

    # Lowest rate
    result = conn.execute(text("SELECT MIN(interest_rate) FROM schemes"))
    print(f"4. Lowest rate: {result.fetchone()[0]:.2f}%")

print("\n" + "="*60)
print("SQL SETUP COMPLETE!")
print("="*60)
