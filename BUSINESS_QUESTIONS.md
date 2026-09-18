# EduLoan Intelligence — Business Questions & Formulas

**Project:** Education Loan Rate Intelligence Dashboard
**Data Source:** Real data from 5 major Indian banks (SBI, HDFC, ICICI, Axis, BOB)
**Total Schemes:** 14 | **Banks:** 5 | **Historical Data:** 6 months
**Last Updated:** 2026-09-13

---

## Project Overview

| Metric | Value |
|--------|-------|
| Total Business Questions | 35 |
| Categories | 7 |
| Banks Analyzed | 5 |
| Schemes Analyzed | 14 
| Historical Data | 6 months (78 rows) |
| Data Quality | 100% |
| Source Traceability | 100% (hyperlinked) |

---

## Category 1: Cost Analysis (Q1-Q5)

### Q1: Which bank offers the lowest interest rate?

**Formula:** MIN(interest_rate)

**Expected Answer:** Bank of Baroda — Baroda Scholar at 6.85%

**Visual:** Ranked Bar Chart (sorted ascending)

**Business Value:** Identifies the cheapest option for cost-conscious students

---

### Q2: Which bank has the lowest total cost (rate + fee)?

**Formula:** MIN(interest_rate + processing_fee_percent)

**Expected Answer:** SBI — PM-Vidyalaxmi at 6.90% (0% processing fee)

**Visual:** Scatter Plot (Rate vs Fee)

**Business Value:** Reveals true cost, not just advertised rate

---

### Q3: How much extra will I pay if I choose a higher-rate bank?

**Formula:**
Extra Cost = (Higher Rate - Lower Rate) × Loan Amount × Tenure

**Example (Rs 10,00,000 over 5 years):**
- Best (6.85%): Rs 1,84,000 interest
- Worst (10.81%): Rs 2,97,000 interest
- Extra Cost: Rs 1,13,000

**Visual:** Cost Comparison Bar Chart

**Business Value:** Quantifies the cost of a wrong decision

---

### Q4: Which bank has the lowest processing fee?

**Formula:** MIN(processing_fee_percent)

**Expected Answer:** SBI, HDFC at 0% for select schemes

**Visual:** Bar Chart

**Business Value:** Upfront cost matters for students

---

### Q5: Is a lower rate always better?

**Formula:**
Total Cost = Interest + Processing Fee

**Expected Answer:** No — fees can erase rate advantage

**Visual:** Scatter Plot + Verdict Card

**Business Value:** Teaches total cost thinking

---

## Category 2: Eligibility Analysis (Q6-Q10)

### Q6: Which bank gives the highest loan amount?

**Formula:** MAX(max_loan_amount)

**Expected Answer:** ICICI Bank — Secured Loan (Abroad) at Rs 3,00,00,000

**Visual:** Bar Chart

**Business Value:** Critical for abroad education

---

### Q7: Which banks offer no-collateral loans?

**Formula:** FILTER(collateral_needed = "No")

**Expected Answer:** SBI, BOB, HDFC, ICICI (select schemes)

**Visual:** Filtered Table

**Business Value:** Accessibility for middle-class families

---

### Q8: What is the minimum loan amount each bank offers?

**Formula:** MIN(max_loan_amount) GROUP BY bank

**Visual:** Bar Chart

**Business Value:** Helps students with small needs

---

### Q9: Which bank has the most flexible eligibility?

**Formula:** COUNT(schemes WHERE collateral_needed = "No") GROUP BY bank

**Expected Answer:** SBI (3 schemes without collateral)

**Visual:** Comparison Table

**Business Value:** Shows which bank is most accessible

---

### Q10: Which banks don't require a co-applicant?

**Formula:** FILTER(co_applicant_required = "No")

**Expected Answer:** None — All banks require a co-applicant

**Visual:** Info Card

**Business Value:** Reality check for students

---

## Category 3: Repayment Analysis (Q11-Q15)

### Q11: Which bank offers the longest moratorium?

**Formula:** MAX(moratorium_months)

**Expected Answer:** All banks offer 12 months (standard)

**Visual:** Bar Chart

**Business Value:** Cash flow planning after graduation

---

### Q12: What is the monthly EMI for each bank?

**Formula:**
EMI = P × r × (1+r)^n / ((1+r)^n - 1)

Where:
  P = Principal (loan amount)
  r = Monthly interest rate = Annual Rate / 12 / 100
  n = Tenure in months

**Example (Rs 10,00,000 over 5 years):**
- SBI (7.05%): EMI = Rs 19,818
- HDFC (10.50%): EMI = Rs 21,494

**Visual:** EMI Calculator

**Business Value:** Monthly burden assessment

---

### Q13: Which bank offers the most flexible repayment?

**Formula:** FILTER(schemes WHERE moratorium_months > 12)

**Expected Answer:** All standard at 12 months

**Visual:** Comparison Table

**Business Value:** Real-world flexibility check

---

### Q14: How much interest will I pay in total?

**Formula:**
Total Interest = (EMI × n) - P

**Example (Rs 10,00,000 over 5 years):**
- SBI (7.05%): Rs 1,89,080 interest
- HDFC (10.50%): Rs 2,89,640 interest

**Visual:** Stacked Bar Chart

**Business Value:** True cost of borrowing

---

### Q15: Which bank offers prepayment without penalty?

**Formula:** FILTER(prepayment_penalty = "No")

**Expected Answer:** Most floating-rate loans (SBI, BOB)

**Visual:** Info Card

**Business Value:** Long-term savings potential

---

## Category 4: Comparison Analysis (Q16-Q20)

### Q16: Public vs Private — who is cheaper?

**Formula:**
Public Avg = AVERAGE(interest_rate WHERE bank_type = "Public Sector")
Private Avg = AVERAGE(interest_rate WHERE bank_type = "Private Sector")

**Expected Answer:** Public banks are 1.06% cheaper on average

**Visual:** Box Plot

**Business Value:** Trust vs cost trade-off

---

### Q17: Domestic vs Abroad — which costs more?

**Formula:**
Domestic Avg = AVERAGE(rate WHERE destination = "India")
Abroad Avg = AVERAGE(rate WHERE destination = "Abroad")

**Expected Answer:** Abroad loans cost ~1.5% more

**Visual:** Grouped Bar Chart

**Business Value:** Currency and risk premium

---

### Q18: Which bank is best for IIM/IIT students?

**Formula:** FILTER(best_for CONTAINS "IIM" OR "IIT")

**Expected Answer:** BOB Baroda Scholar at 6.85%

**Visual:** Filtered Verdict Card

**Business Value:** Elite institute advantage

---

### Q19: Which bank is best for middle-class families?

**Formula:** FILTER(collateral_needed = "No" AND interest_rate < 9)

**Expected Answer:** SBI PM-Vidyalaxmi at 6.90% (no collateral)

**Visual:** Filtered Verdict Card

**Business Value:** Accessibility analysis

---

### Q20: Which bank is consistently best across all metrics?

**Formula:**
Score = COUNT(metrics WHERE bank is best)

**Expected Answer:** BOB (wins 12 of 20 questions)

**Visual:** Score Card

**Business Value:** Overall winner identification

---

## Category 5: Loan Cost Calculator (Q21-Q25)

### Q21: How much interest for MY exact amount?

**Formula:**
Interest = (EMI × n) - P

**Visual:** Dynamic Table

**Business Value:** Personalized cost estimate

---

### Q22: What is the monthly EMI for my amount?

**Formula:** EMI = P × r × (1+r)^n / ((1+r)^n - 1)

**Visual:** EMI Table

**Business Value:** Monthly planning

---

### Q23: What is the total cost including fees?

**Formula:**
Total Cost = P + Interest + (P × processing_fee_percent / 100)

**Visual:** Bar Chart

**Business Value:** Full repayment understanding

---

### Q24: How much can I save by choosing the best bank?

**Formula:**
Savings = Worst Total Cost - Best Total Cost

**Example (Rs 12,000 over 5 years):**
- Best (BOB): Rs 14,570
- Worst (Axis): Rs 16,240
- Savings: Rs 1,670

**Visual:** Verdict Card

**Business Value:** Quantified decision impact

---

### Q25: Which bank is cheapest for MY amount?

**Formula:** MIN(Total Cost)

**Visual:** Dynamic Recommendation Card

**Business Value:** Personalized verdict

---

## Category 6: Bank Deep-Dive (Q26-Q30)

### Q26: What are all the interest rates this bank offers?

**Formula:** MIN, MAX, AVERAGE(interest_rate WHERE bank = selected)

**Visual:** KPI Cards + Bar Chart

**Business Value:** Complete rate picture

---

### Q27: Is this bank safe?

**Formula:** Check:
- Bank Type (Public/Private)
- RBI Regulated (Yes/No)
- DICGC Insured (Yes/No)
- Credit Rating (AAA/AA/A)
- Years in Operation

**Visual:** Safety Panel

**Business Value:** Trust verification

---

### Q28: What schemes does this bank offer?

**Formula:** FILTER(bank = selected)

**Visual:** Scheme Table

**Business Value:** Complete options list

---

### Q29: Which scheme is best for me?

**Formula:** MIN(interest_rate WHERE bank = selected AND meets_user_criteria)

**Visual:** Verdict Card

**Business Value:** Personalized advice

---

### Q30: What are the risks with this bank?

**Visual:** Risk Panel

**Business Value:** Transparency about downsides

---

## Category 7: Advanced Analysis (Q31-Q35)

### Q31: How have rates changed over time?

**Formula:**
Rate Change = Current Rate - Previous Rate

**Data Source:** historical_rates.xlsx (6 months)

**Visual:** Line Chart

**Business Value:** Trend analysis

---

### Q32: Which bank has the most stable rates?

**Formula:**
Volatility = STANDARD_DEVIATION(interest_rate)

**Visual:** Volatility Chart

**Business Value:** Predictability assessment

---

### Q33: What is the best day/month to apply?

**Formula:** MIN(interest_rate) BY date

**Visual:** Daily Best Rate Chart

**Business Value:** Timing optimization

---

### Q34: How does my rate compare to market average?

**Formula:**
Market Average = AVERAGE(interest_rate)
Difference = User Rate - Market Average

**Visual:** Gauge Chart

**Business Value:** Benchmark comparison

---

### Q35: What is the break-even point for prepayment?

**Formula:**
Break-even Months = Processing Fee / Monthly Savings

**Visual:** Calculator

**Business Value:** Prepayment strategy

---

## Key Formulas Summary

| Formula | Use Case |
|---------|----------|
| EMI = P × r × (1+r)^n / ((1+r)^n - 1) | Monthly payment |
| Total Interest = (EMI × n) - P | Interest cost |
| Total Cost = P + Interest + Fee | Full repayment |
| Savings = Worst - Best | Comparative savings |
| Volatility = STDDEV(rate) | Rate stability |
| Extra Cost = (Rate Diff) × P × Tenure | Wrong choice impact |
| Break-even = Fee / Monthly Savings | Prepayment timing |

---

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Questions Answered | 35 | Planned |
| Charts Created | 15+ | Planned |
| Banks Compared | 5 | Ready |
| Schemes Analyzed | 14 | Ready |
| Data Quality | 100% | Done |
| Source Traceability | 100% | Done |

---

## Project Impact

This dashboard helps students answer 35 real business questions about education loans — from finding the lowest rate (BOB at 6.85%) to calculating exact EMI for their loan amount — reducing decision time from hours to seconds.

---

## Best Rates Found

| Rank | Bank | Scheme | Rate |
|------|------|--------|------|
| 1 | Bank of Baroda | Baroda Scholar (IIMs/IITs) | 6.85% |
| 2 | SBI | PM-Vidyalaxmi (Utkarsh) | 6.90% |
| 3 | SBI | SBI Scholar Loan | 7.05% |
| 4 | Bank of Baroda | Baroda Gyan (AA) | 7.20% |
| 5 | Axis Bank | Axis Domestic Secured | 7.45% |
| 6 | ICICI Bank | ICICI Secured Domestic | 8.50% |
| 7 | HDFC Bank | HDFC Education Loan | 10.50% |

---

End of Document
