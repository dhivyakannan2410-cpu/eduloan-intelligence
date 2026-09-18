import pandas as pd
import os

os.makedirs('data/excel', exist_ok=True)

# ============================================================
# SBI DATA
# ============================================================
sbi_data = [
    {"scheme_name": "SBI Scholar Loan (IIMs/IITs)", "interest_rate": 7.05, "rate_type": "Floating", "max_loan_amount": 5000000, "collateral_required": "No (up to 7.5L)", "processing_fee_percent": 0, "moratorium_months": 12, "best_for": "Top 10 IIMs & IITs", "study_destination": "India", "source_url": "https://www.fincash.com/l/loan/sbi-scholar-loan", "source_type": "Third-Party Aggregator"},
    {"scheme_name": "SBI Global Ed-Vantage (Abroad, Female)", "interest_rate": 8.65, "rate_type": "Floating", "max_loan_amount": 15000000, "collateral_required": "Yes", "processing_fee_percent": 0.5, "moratorium_months": 12, "best_for": "Abroad Studies (Female)", "study_destination": "Abroad", "source_url": "https://www.gyandhan.com/sbi-education-loan", "source_type": "Third-Party Aggregator"},
    {"scheme_name": "SBI Global Ed-Vantage (Abroad, Male)", "interest_rate": 9.15, "rate_type": "Floating", "max_loan_amount": 15000000, "collateral_required": "Yes", "processing_fee_percent": 0.5, "moratorium_months": 12, "best_for": "Abroad Studies (Male)", "study_destination": "Abroad", "source_url": "https://www.gyandhan.com/sbi-education-loan", "source_type": "Third-Party Aggregator"},
    {"scheme_name": "PM-Vidyalaxmi (Utkarsh)", "interest_rate": 6.90, "rate_type": "Floating", "max_loan_amount": 1000000, "collateral_required": "No", "processing_fee_percent": 0, "moratorium_months": 12, "best_for": "Meritorious Students (EWS)", "study_destination": "India", "source_url": "https://ndtv.bankbazaar.com/sbi-education-loan.html", "source_type": "Third-Party Aggregator"}
]

# ============================================================
# HDFC DATA
# ============================================================
hdfc_data = [
    {"scheme_name": "HDFC Education Loan (Domestic)", "interest_rate": 10.50, "rate_type": "Floating", "max_loan_amount": 7500000, "collateral_required": "No (up to 7.5L)", "processing_fee_percent": 0, "moratorium_months": 12, "best_for": "Domestic Students", "study_destination": "India", "source_url": "https://www.hdfc.bank.in/education-loan/interest-rates-and-charges", "source_type": "Official Bank Website"},
    {"scheme_name": "HDFC Education Loan (Abroad)", "interest_rate": 8.64, "rate_type": "Floating", "max_loan_amount": 15000000, "collateral_required": "Yes", "processing_fee_percent": 0.5, "moratorium_months": 12, "best_for": "Abroad Studies", "study_destination": "Abroad", "source_url": "https://www.propelld.com/blog/hdfc-education-loan", "source_type": "Third-Party Aggregator"}
]

# ============================================================
# ICICI DATA
# ============================================================
icici_data = [
    {"scheme_name": "ICICI Secured Loan (Domestic Premier)", "interest_rate": 8.50, "rate_type": "Floating", "max_loan_amount": 10000000, "collateral_required": "Yes", "processing_fee_percent": 1.5, "moratorium_months": 12, "best_for": "Select Domestic Institutes", "study_destination": "India", "source_url": "https://www.icicibank.com/personal-banking/loans/education-loan/interest-rates", "source_type": "Official Bank Website"},
    {"scheme_name": "ICICI Secured Loan (Abroad)", "interest_rate": 9.00, "rate_type": "Floating", "max_loan_amount": 30000000, "collateral_required": "Yes", "processing_fee_percent": 1.5, "moratorium_months": 12, "best_for": "Abroad Studies (Secured)", "study_destination": "Abroad", "source_url": "https://www.icicibank.com/personal-banking/loans/education-loan/interest-rates", "source_type": "Official Bank Website"},
    {"scheme_name": "ICICI Unsecured Loan (Abroad)", "interest_rate": 10.25, "rate_type": "Floating", "max_loan_amount": 5000000, "collateral_required": "No", "processing_fee_percent": 1.5, "moratorium_months": 12, "best_for": "Abroad Studies (No Collateral)", "study_destination": "Abroad", "source_url": "https://www.icicibank.com/personal-banking/loans/education-loan/interest-rates", "source_type": "Official Bank Website"}
]

# ============================================================
# AXIS DATA
# ============================================================
axis_data = [
    {"scheme_name": "Axis Education Loan (Domestic Secured)", "interest_rate": 7.45, "rate_type": "Floating", "max_loan_amount": 7500000, "collateral_required": "Yes", "processing_fee_percent": 2.0, "moratorium_months": 12, "best_for": "Secured Loans", "study_destination": "India", "source_url": "https://www.axis.bank.in/loans/education-loan/interest-rates-charges", "source_type": "Third-Party Aggregator (BankBazaar)"},
    {"scheme_name": "Axis Education Loan (Abroad Unsecured)", "interest_rate": 10.81, "rate_type": "Floating", "max_loan_amount": 7500000, "collateral_required": "No (up to 40L)", "processing_fee_percent": 2.0, "moratorium_months": 12, "best_for": "Abroad Studies", "study_destination": "Abroad", "source_url": "https://ndtv.in/business-news/education-loan-interest-rates-compared", "source_type": "News Article (NDTV)"}
]

# ============================================================
# BOB DATA
# ============================================================
bob_data = [
    {"scheme_name": "Baroda Scholar (Top IIMs/IITs)", "interest_rate": 6.85, "rate_type": "Floating", "max_loan_amount": 4000000, "collateral_required": "No (up to 7.5L)", "processing_fee_percent": 1.0, "moratorium_months": 12, "best_for": "Top 10 IIMs & IITs", "study_destination": "India", "source_url": "https://bankofbaroda.bank.in/loans/education-loan/baroda-education-loan-to-students-of-premier-institutions", "source_type": "Official Bank Website"},
    {"scheme_name": "Baroda Gyan (AA Category)", "interest_rate": 7.20, "rate_type": "Floating", "max_loan_amount": 3000000, "collateral_required": "No (up to 7.5L)", "processing_fee_percent": 1.0, "moratorium_months": 12, "best_for": "AA Category Institutions", "study_destination": "India", "source_url": "https://bankofbaroda.bank.in/loans/education-loan/baroda-education-loan-to-students-of-premier-institutions", "source_type": "Official Bank Website"},
    {"scheme_name": "Baroda Education Loan (General)", "interest_rate": 8.55, "rate_type": "Floating", "max_loan_amount": 15000000, "collateral_required": "Yes", "processing_fee_percent": 1.0, "moratorium_months": 12, "best_for": "General Students", "study_destination": "India", "source_url": "https://bankofbaroda.bank.in/loans/education-loan", "source_type": "Official Bank Website"}
]

# ============================================================
# CREATE EXCEL FILE FOR EACH BANK
# ============================================================
banks = {
    "SBI": ("Public Sector", sbi_data),
    "HDFC": ("Private Sector", hdfc_data),
    "ICICI": ("Private Sector", icici_data),
    "Axis": ("Private Sector", axis_data),
    "BOB": ("Public Sector", bob_data)
}

for bank_name, (bank_type, schemes) in banks.items():
    df = pd.DataFrame(schemes)
    df.insert(0, 'bank', bank_name)
    df.insert(1, 'bank_type', bank_type)
    df['date_collected'] = '2026-09-13'
    
    # Reorder columns
    df = df[['bank', 'bank_type', 'scheme_name', 'interest_rate', 'rate_type',
             'max_loan_amount', 'collateral_required', 'processing_fee_percent',
             'moratorium_months', 'best_for', 'study_destination',
             'source_url', 'source_type', 'date_collected']]
    
    output_file = f'data/excel/{bank_name}_education_loan.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Created: {output_file} ({len(df)} schemes)")

print()
print("All 5 Excel files created with source_type labeled!")
