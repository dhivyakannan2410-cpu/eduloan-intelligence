# 🎓 EduLoan Intelligence

Data Analyst Project — Education Loan Rate Comparison Dashboard for 5 major Indian banks.

## 📊 Project Overview

- **5 Banks:** SBI, HDFC, ICICI, Axis, BOB
- **14 Schemes** analyzed
- **35 Business Questions** answered
- **6-Month Historical** trends
- **Cross-filtering** interactive dashboard

## 🎯 What This Project Does

This dashboard helps students:
- Compare education loan rates from 5 major Indian banks
- Find the **best bank + best scheme** for their loan amount
- Calculate **EMI, total interest, and processing fees**
- See **savings** compared to other banks
- View **6-month rate trends**

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| **Language** | Python 3.13 |
| **Data** | Pandas, NumPy |
| **Database** | SQLite, SQLAlchemy |
| **Visualization** | Plotly |
| **Dashboard** | Streamlit |
| **SQL Skills** | Window Functions, CTEs, Subqueries, Joins |

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install streamlit pandas plotly openpyxl sqlalchemy

# 2. Setup SQL database
python setup_sql.py

# 3. Run dashboard
python -m streamlit run dashboard.py
