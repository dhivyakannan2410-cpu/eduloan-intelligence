import pandas as pd
import os

print("=" * 60)
print("DATA CLEANING PIPELINE")
print("=" * 60)

# ============================================================
# 1. LOAD ALL RAW FILES
# ============================================================
print("\n[1/6] Loading raw Excel files...")

files = {
    'SBI': 'data/raw/SBI_education_loan.xlsx',
    'HDFC': 'data/raw/HDFC_education_loan.xlsx',
    'ICICI': 'data/raw/ICICI_education_loan.xlsx',
    'Axis': 'data/raw/Axis_education_loan.xlsx',
    'BOB': 'data/raw/BOB_education_loan.xlsx'
}

dfs = []
for bank, path in files.items():
    df = pd.read_excel(path)
    dfs.append(df)
    print(f"  Loaded {bank}: {len(df)} schemes")

combined = pd.concat(dfs, ignore_index=True)
print(f"\n  Total schemes: {len(combined)}")

# ============================================================
# 2. CLEAN
# ============================================================
print("\n[2/6] Cleaning data...")

text_cols = ['bank', 'bank_type', 'scheme_name', 'rate_type',
             'collateral_required', 'best_for', 'study_destination',
             'source_url', 'source_type']
for col in text_cols:
    if col in combined.columns:
        combined[col] = combined[col].astype(str).str.strip()

bank_mapping = {
    'SBI': 'SBI', 'State Bank of India': 'SBI',
    'HDFC': 'HDFC Bank', 'HDFC Bank': 'HDFC Bank',
    'ICICI': 'ICICI Bank', 'ICICI Bank': 'ICICI Bank',
    'Axis': 'Axis Bank', 'Axis Bank': 'Axis Bank',
    'BOB': 'Bank of Baroda', 'Bank of Baroda': 'Bank of Baroda'
}
combined['bank'] = combined['bank'].map(bank_mapping).fillna(combined['bank'])

dest_mapping = {'india': 'India', 'India': 'India', 'abroad': 'Abroad', 'Abroad': 'Abroad'}
combined['study_destination'] = combined['study_destination'].map(dest_mapping).fillna(combined['study_destination'])

numeric_cols = ['interest_rate', 'max_loan_amount', 'processing_fee_percent', 'moratorium_months']
for col in numeric_cols:
    combined[col] = pd.to_numeric(combined[col], errors='coerce')

combined['processing_fee_percent'] = combined['processing_fee_percent'].fillna(0)
combined['moratorium_months'] = combined['moratorium_months'].fillna(12)
combined = combined.dropna(subset=['bank', 'scheme_name', 'interest_rate'])

combined = combined.drop_duplicates(subset=['bank', 'scheme_name'], keep='first')

# ============================================================
# 3. ADD DERIVED COLUMNS
# ============================================================
print("\n[3/6] Adding derived columns...")

combined['total_cost_percent'] = combined['interest_rate'] + combined['processing_fee_percent']

def rate_category(rate):
    if rate < 7.5: return 'Excellent (<7.5%)'
    elif rate < 9: return 'Good (7.5-9%)'
    elif rate < 11: return 'Moderate (9-11%)'
    else: return 'High (>11%)'

combined['rate_category'] = combined['interest_rate'].apply(rate_category)
combined['collateral_needed'] = combined['collateral_required'].apply(
    lambda x: 'No' if 'no' in str(x).lower() else 'Yes')
combined['is_official'] = combined['source_type'].apply(
    lambda x: 'Yes' if 'Official' in str(x) else 'No')

# ============================================================
# 4. SAVE CLEANED FILES
# ============================================================
print("\n[4/6] Saving cleaned files...")

os.makedirs('data/cleaned', exist_ok=True)

combined.to_excel('data/cleaned/cleaned_all_banks.xlsx', index=False)
combined.to_csv('data/cleaned/cleaned_all_banks.csv', index=False)
print("  Saved: data/cleaned/cleaned_all_banks.xlsx")
print("  Saved: data/cleaned/cleaned_all_banks.csv")

for bank_name in combined['bank'].unique():
    bank_df = combined[combined['bank'] == bank_name]
    safe_name = bank_name.replace(' ', '_')
    bank_df.to_excel(f'data/cleaned/{safe_name}_cleaned.xlsx', index=False)
    print(f"  Saved: data/cleaned/{safe_name}_cleaned.xlsx")

# ============================================================
# 5. SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("CLEANING COMPLETE")
print("=" * 60)
print(f"  Total schemes: {len(combined)}")
print(f"  Banks: {combined['bank'].nunique()}")
print(f"  Rate range: {combined['interest_rate'].min():.2f}% - {combined['interest_rate'].max():.2f}%")
print("=" * 60)
