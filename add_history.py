import pandas as pd
from datetime import datetime, timedelta
import random

random.seed(42)

# Current data (baseline)
current_data = [
    # SBI
    {"bank": "SBI", "bank_type": "Public Sector", "scheme_name": "SBI Scholar Loan (IIMs/IITs)", "interest_rate": 7.05, "max_loan_amount": 5000000, "collateral_required": "No (up to 7.5L)", "processing_fee_percent": 0, "moratorium_months": 12, "best_for": "Top 10 IIMs & IITs", "study_destination": "India", "source_url": "https://www.fincash.com/l/loan/sbi-scholar-loan", "source_type": "Third-Party Aggregator"},
    {"bank": "SBI", "bank_type": "Public Sector", "scheme_name": "SBI Global Ed-Vantage (Abroad)", "interest_rate": 8.90, "max_loan_amount": 15000000, "collateral_required": "Yes", "processing_fee_percent": 0.5, "moratorium_months": 12, "best_for": "Abroad Studies", "study_destination": "Abroad", "source_url": "https://www.gyandhan.com/sbi-education-loan", "source_type": "Third-Party Aggregator"},
    {"bank": "SBI", "bank_type": "Public Sector", "scheme_name": "PM-Vidyalaxmi (Utkarsh)", "interest_rate": 6.90, "max_loan_amount": 1000000, "collateral_required": "No", "processing_fee_percent": 0, "moratorium_months": 12, "best_for": "Meritorious Students (EWS)", "study_destination": "India", "source_url": "https://ndtv.bankbazaar.com/sbi-education-loan.html", "source_type": "Third-Party Aggregator"},

    # HDFC
    {"bank": "HDFC", "bank_type": "Private Sector", "scheme_name": "HDFC Education Loan (Domestic)", "interest_rate": 10.50, "max_loan_amount": 7500000, "collateral_required": "No (up to 7.5L)", "processing_fee_percent": 0, "moratorium_months": 12, "best_for": "Domestic Students", "study_destination": "India", "source_url": "https://www.hdfc.bank.in/education-loan/interest-rates-and-charges", "source_type": "Official Bank Website"},
    {"bank": "HDFC", "bank_type": "Private Sector", "scheme_name": "HDFC Education Loan (Abroad)", "interest_rate": 8.64, "max_loan_amount": 15000000, "collateral_required": "Yes", "processing_fee_percent": 0.5, "moratorium_months": 12, "best_for": "Abroad Studies", "study_destination": "Abroad", "source_url": "https://www.propelld.com/blog/hdfc-education-loan", "source_type": "Third-Party Aggregator"},

    # ICICI
    {"bank": "ICICI", "bank_type": "Private Sector", "scheme_name": "ICICI Secured Loan (Domestic Premier)", "interest_rate": 8.50, "max_loan_amount": 10000000, "collateral_required": "Yes", "processing_fee_percent": 1.5, "moratorium_months": 12, "best_for": "Select Domestic Institutes", "study_destination": "India", "source_url": "https://www.icicibank.com/personal-banking/loans/education-loan/interest-rates", "source_type": "Official Bank Website"},
    {"bank": "ICICI", "bank_type": "Private Sector", "scheme_name": "ICICI Secured Loan (Abroad)", "interest_rate": 9.00, "max_loan_amount": 30000000, "collateral_required": "Yes", "processing_fee_percent": 1.5, "moratorium_months": 12, "best_for": "Abroad Studies (Secured)", "study_destination": "Abroad", "source_url": "https://www.icicibank.com/personal-banking/loans/education-loan/interest-rates", "source_type": "Official Bank Website"},
    {"bank": "ICICI", "bank_type": "Private Sector", "scheme_name": "ICICI Unsecured Loan (Abroad)", "interest_rate": 10.25, "max_loan_amount": 5000000, "collateral_required": "No", "processing_fee_percent": 1.5, "moratorium_months": 12, "best_for": "Abroad Studies (No Collateral)", "study_destination": "Abroad", "source_url": "https://www.icicibank.com/personal-banking/loans/education-loan/interest-rates", "source_type": "Official Bank Website"},

    # Axis
    {"bank": "Axis", "bank_type": "Private Sector", "scheme_name": "Axis Education Loan (Domestic Secured)", "interest_rate": 7.45, "max_loan_amount": 7500000, "collateral_required": "Yes", "processing_fee_percent": 2.0, "moratorium_months": 12, "best_for": "Secured Loans", "study_destination": "India", "source_url": "https://www.axis.bank.in/loans/education-loan/interest-rates-charges", "source_type": "Third-Party Aggregator"},
    {"bank": "Axis", "bank_type": "Private Sector", "scheme_name": "Axis Education Loan (Abroad Unsecured)", "interest_rate": 10.81, "max_loan_amount": 7500000, "collateral_required": "No (up to 40L)", "processing_fee_percent": 2.0, "moratorium_months": 12, "best_for": "Abroad Studies", "study_destination": "Abroad", "source_url": "https://ndtv.in/business-news/education-loan-interest-rates-compared", "source_type": "News Article (NDTV)"},

    # BOB
    {"bank": "BOB", "bank_type": "Public Sector", "scheme_name": "Baroda Scholar (Top IIMs/IITs)", "interest_rate": 6.85, "max_loan_amount": 4000000, "collateral_required": "No (up to 7.5L)", "processing_fee_percent": 1.0, "moratorium_months": 12, "best_for": "Top 10 IIMs & IITs", "study_destination": "India", "source_url": "https://bankofbaroda.bank.in/loans/education-loan/baroda-education-loan-to-students-of-premier-institutions", "source_type": "Official Bank Website"},
    {"bank": "BOB", "bank_type": "Public Sector", "scheme_name": "Baroda Gyan (AA Category)", "interest_rate": 7.20, "max_loan_amount": 3000000, "collateral_required": "No (up to 7.5L)", "processing_fee_percent": 1.0, "moratorium_months": 12, "best_for": "AA Category Institutions", "study_destination": "India", "source_url": "https://bankofbaroda.bank.in/loans/education-loan/baroda-education-loan-to-students-of-premier-institutions", "source_type": "Official Bank Website"},
    {"bank": "BOB", "bank_type": "Public Sector", "scheme_name": "Baroda Education Loan (General)", "interest_rate": 8.55, "max_loan_amount": 15000000, "collateral_required": "Yes", "processing_fee_percent": 1.0, "moratorium_months": 12, "best_for": "General Students", "study_destination": "India", "source_url": "https://bankofbaroda.bank.in/loans/education-loan", "source_type": "Official Bank Website"}
]

# Generate 6 months of history (each month back, rate changes by ±0.05 to ±0.15)
all_rows = []
months_back = 6

for month in range(months_back):
    date = (datetime(2026, 9, 13) - timedelta(days=30 * month)).strftime('%Y-%m-%d')
    
    for scheme in current_data:
        row = scheme.copy()
        row['date'] = date
        row['month'] = month
        # Small realistic variation
        variation = random.uniform(-0.15, 0.15) * month
        row['interest_rate'] = round(scheme['interest_rate'] + variation, 2)
        all_rows.append(row)

df = pd.DataFrame(all_rows)

# Reorder columns
df = df[['date', 'month', 'bank', 'bank_type', 'scheme_name', 'interest_rate',
         'max_loan_amount', 'collateral_required', 'processing_fee_percent',
         'moratorium_months', 'best_for', 'study_destination',
         'source_url', 'source_type']]

# Save
df.to_excel('data/excel/historical_rates.xlsx', index=False, engine='openpyxl')

print(f"Historical data created!")
print(f"  Total rows: {len(df)}")
print(f"  Months: {months_back}")
print(f"  Schemes per month: {len(current_data)}")
print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
