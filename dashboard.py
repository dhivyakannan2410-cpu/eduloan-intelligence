import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EduLoan Intelligence", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .winner-card { background: linear-gradient(135deg, #10b981, #059669);
        color: white; padding: 1.5rem; border-radius: 12px; margin: 0.5rem 0; }
    .winner-card h2 { color: white; margin: 0; font-size: 1.6rem; }
    .winner-card h3 { color: #d1fae5; margin: 0.3rem 0; font-size: 1.05rem; }
    .metric-box { background: rgba(255,255,255,0.18); border-radius: 8px;
        padding: 0.6rem; text-align: center; }
    .metric-label { font-size: 0.7rem; opacity: 0.9; text-transform: uppercase; }
    .metric-value { font-size: 1.2rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 EduLoan Intelligence")
st.caption("Enter your amount → See the best bank, best scheme, and how much you save")

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    return pd.read_excel('data/cleaned/cleaned_all_banks.xlsx'), pd.read_excel('data/raw/historical_rates.xlsx')

df, hist = load_data()

def calculate_emi(principal, annual_rate, years):
    r = annual_rate / 12 / 100
    n = years * 12
    if r == 0: return principal / n
    return principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header("🎯 Your Loan Details")

loan_amount = st.sidebar.number_input(
    "💰 Loan Amount (₹)", min_value=10000, max_value=50000000,
    value=500000, step=50000, format="%d"
)

tenure_years = st.sidebar.selectbox(
    "📅 Tenure (Years)", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15], index=4
)

destination = st.sidebar.radio("🌍 Destination", ["All", "India", "Abroad"], horizontal=True)
collateral = st.sidebar.radio("🏠 Collateral", ["All", "Yes", "No"], horizontal=True)
bank_type_filter = st.sidebar.radio("🏦 Bank Type", ["All", "Public Sector", "Private Sector"], horizontal=True)

st.sidebar.divider()

# ⭐ CROSS-FILTER: Bank selector
all_banks_list = sorted(df['bank'].unique().tolist())
selected_banks = st.sidebar.multiselect(
    "🔍 Focus on Banks (Cross-Filter)",
    options=all_banks_list,
    default=all_banks_list,
    help="Select banks → all charts update to show only those banks"
)

st.sidebar.divider()
st.sidebar.caption("📌 Data: Official bank websites")

# ============================================================
# APPLY FILTERS
# ============================================================
f = df[df['max_loan_amount'] >= loan_amount].copy()

if destination != "All":
    f = f[f['study_destination'].str.contains(destination, case=False, na=False)]

if collateral != "All":
    if collateral == "No":
        f = f[f['collateral_needed'].str.lower().str.contains('no', na=False)]
    elif collateral == "Yes":
        f = f[~f['collateral_needed'].str.lower().str.contains('no', na=False)]

if bank_type_filter != "All":
    f = f[f['bank_type'] == bank_type_filter]

# ⭐ Apply cross-filter
f = f[f['bank'].isin(selected_banks)]

# ============================================================
# KPI SNAPSHOT + ACTIVE FILTERS
# ============================================================
st.subheader("📊 Market Snapshot")

active_banks = ', '.join(selected_banks) if len(selected_banks) < 5 else 'All 5 banks'
st.caption(f"🎯 Active filters: **₹{loan_amount:,}** | **{tenure_years} years** | Destination: **{destination}** | Collateral: **{collateral}** | Bank Type: **{bank_type_filter}** | Banks: **{active_banks}**")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Schemes Matched", len(f))
if not f.empty:
    c2.metric("Lowest Rate", f"{f['interest_rate'].min():.2f}%")
    c3.metric("Highest Rate", f"{f['interest_rate'].max():.2f}%")
    c4.metric("Market Average", f"{f['interest_rate'].mean():.2f}%")

# Exclusion panel
excluded = df[~df.index.isin(f.index)]
if len(excluded) > 0:
    with st.expander(f"🔍 Why {len(excluded)} schemes were excluded from your search"):
        reasons_list = []
        for _, row in excluded.iterrows():
            reasons = []
            if row['max_loan_amount'] < loan_amount:
                reasons.append(f"Max loan ₹{row['max_loan_amount']:,} < ₹{loan_amount:,}")
            if destination != "All" and destination.lower() not in str(row['study_destination']).lower():
                reasons.append(f"Only for {row['study_destination']} studies")
            if collateral == "No" and 'no' not in str(row['collateral_needed']).lower():
                reasons.append(f"Requires collateral")
            if collateral == "Yes" and 'no' in str(row['collateral_needed']).lower() and 'up to' not in str(row['collateral_needed']).lower():
                reasons.append(f"No collateral required")
            if bank_type_filter != "All" and row['bank_type'] != bank_type_filter:
                reasons.append(f"Only {row['bank_type']}")
            if row['bank'] not in selected_banks:
                reasons.append(f"Not in selected banks")
            reasons_list.append({
                'Bank': row['bank'], 'Scheme': row['scheme_name'],
                'Rate': row['interest_rate'], 'Max Loan': row['max_loan_amount'],
                'Reason': '; '.join(reasons) if reasons else 'Filtered out'
            })
        st.dataframe(
            pd.DataFrame(reasons_list).style.format({'Rate': '{:.2f}%', 'Max Loan': '₹{:,.0f}'}),
            width='stretch'
        )

st.divider()

if f.empty:
    st.warning("No schemes match. Try reducing the loan amount or changing filters.")
    st.stop()

# ============================================================
# BUILD COST TABLE
# ============================================================
cost_list = []
for _, row in f.iterrows():
    emi = calculate_emi(loan_amount, row['interest_rate'], tenure_years)
    months = tenure_years * 12
    interest = (emi * months) - loan_amount
    fee = loan_amount * row['processing_fee_percent'] / 100
    total = loan_amount + interest + fee
    cost_list.append({
        'Bank': row['bank'], 'Scheme': row['scheme_name'],
        'Rate': row['interest_rate'], 'EMI': round(emi),
        'Interest': round(interest), 'Fee': round(fee), 'Total': round(total),
        'Collateral': row['collateral_required'], 'Fee %': row['processing_fee_percent'],
        'Max Loan': row['max_loan_amount'], 'Bank Type': row['bank_type'],
        'Best For': row['best_for']
    })
cost_df = pd.DataFrame(cost_list).sort_values('Total').reset_index(drop=True)

best = cost_df.iloc[0]
worst = cost_df.iloc[-1]
savings = worst['Total'] - best['Total']

bank_best_cost = cost_df.groupby('Bank')['Total'].min().reset_index()
best_bank = bank_best_cost.sort_values('Total').iloc[0]['Bank']
worst_bank = bank_best_cost.sort_values('Total').iloc[-1]['Bank']

# ============================================================
# 1️⃣ BEST BANK & SCHEME
# ============================================================
st.subheader("🏆 Best for You")

st.markdown(f"""
<div class="winner-card">
    <p style="margin:0; font-size:0.8rem; opacity:0.9;">BEST FOR ₹{loan_amount:,} OVER {tenure_years} YEARS</p>
    <h2>🏆 {best['Bank']}</h2>
    <h3>📋 {best['Scheme']}</h3>
    <div style="display:flex; gap:0.8rem; margin-top:1rem; flex-wrap:wrap;">
        <div class="metric-box" style="flex:1;">
            <div class="metric-label">Rate</div>
            <div class="metric-value">{best['Rate']:.2f}%</div>
        </div>
        <div class="metric-box" style="flex:1;">
            <div class="metric-label">EMI</div>
            <div class="metric-value">₹{best['EMI']:,.0f}</div>
        </div>
        <div class="metric-box" style="flex:1;">
            <div class="metric-label">Total</div>
            <div class="metric-value">₹{best['Total']:,.0f}</div>
        </div>
        <div class="metric-box" style="flex:1;">
            <div class="metric-label">You Save</div>
            <div class="metric-value">₹{savings:,.0f}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top 3 banks
st.markdown("### 🏅 Top 3 Banks for You")
top3 = cost_df.drop_duplicates(subset='Bank').head(3).reset_index(drop=True)
cols = st.columns(len(top3))
for i, (_, row) in enumerate(top3.iterrows()):
    with cols[i]:
        medal = ['🥇', '🥈', '🥉'][i]
        st.success(f"{medal} **{row['Bank']}** — {row['Rate']:.2f}%\n\n{row['Scheme']}\n\nTotal: ₹{row['Total']:,.0f}")

with st.expander("❓ How do we identify the best bank for you?"):
    st.markdown(f"""
    **Step 1 — Filter eligible schemes:**
    - Only schemes that can cover **₹{loan_amount:,}**
    - Matching destination: **{destination}**
    - Matching collateral preference: **{collateral}**

    **Step 2 — Calculate total cost for each scheme:**
    - `EMI = P × r × (1+r)^n / ((1+r)^n - 1)`
    - `Total = Principal + Interest + Processing Fee`

    **Step 3 — Rank by lowest total cost**

    **Step 4 — Quantify savings:**
    - Choosing **{best['Bank']}** saves you **₹{savings:,.0f}** vs the worst option.
    """)

# ============================================================
# 2️⃣ COMPARISON WITH ALL OTHER BANKS
# ============================================================
st.subheader("💵 How You Compare with Other Banks")

compare_list = []
for bank in cost_df['Bank'].unique():
    bank_row = cost_df[cost_df['Bank'] == bank].sort_values('Total').iloc[0]
    diff = bank_row['Total'] - best['Total']
    if diff == 0:
        verdict = "🥇 BEST"
    elif diff <= savings * 0.3:
        verdict = f"🥈 Good (₹{diff:,.0f} more)"
    elif diff <= savings * 0.7:
        verdict = f"🥉 Okay (₹{diff:,.0f} more)"
    else:
        verdict = f"❌ Expensive (₹{diff:,.0f} more)"
    compare_list.append({
        'Bank': bank, 'Best Rate': bank_row['Rate'],
        'Monthly EMI': bank_row['EMI'], 'Extra Fee': bank_row['Fee'],
        'Total Cost': bank_row['Total'], 'Compared to Best': diff,
        'Verdict': verdict
    })
compare_df = pd.DataFrame(compare_list).sort_values('Compared to Best')

st.dataframe(
    compare_df.style.format({
        'Best Rate': '{:.2f}%', 'Monthly EMI': '₹{:,.0f}',
        'Extra Fee': '₹{:,.0f}', 'Total Cost': '₹{:,.0f}',
        'Compared to Best': '₹{:,.0f}'
    }),
    width='stretch',
    height=min(400, len(compare_df) * 38 + 40)
)

st.info(f"💡 **If you pick {worst['Bank']}, you lose ₹{savings:,.0f}** compared to {best['Bank']}")

st.divider()

# ============================================================
# 3️⃣ BANK RANKINGS
# ============================================================
st.subheader("📊 Bank Rankings")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### 🟢 Lowest Rate")
    lowest = cost_df.sort_values('Rate').iloc[0]
    st.success(f"**{lowest['Bank']}** — {lowest['Rate']:.2f}%\n\n{lowest['Scheme']}")
with col2:
    st.markdown("#### 🔴 Highest Rate")
    highest = cost_df.sort_values('Rate', ascending=False).iloc[0]
    st.error(f"**{highest['Bank']}** — {highest['Rate']:.2f}%\n\n{highest['Scheme']}")
with col3:
    st.markdown("#### 💸 Highest Extra Fee")
    fee_hi = cost_df.sort_values('Fee', ascending=False).iloc[0]
    st.warning(f"**{fee_hi['Bank']}** — ₹{fee_hi['Fee']:,.0f}\n\n{fee_hi['Fee %']:.2f}% processing fee")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 💰 Cheapest Total")
    st.success(f"**{best['Bank']}** — ₹{best['Total']:,.0f}\n\n{best['Scheme']}")
with col2:
    st.markdown("#### 💸 Most Expensive Total")
    st.error(f"**{worst['Bank']}** — ₹{worst['Total']:,.0f}\n\n{worst['Scheme']}")

st.divider()

# ============================================================
# 3.5 RATE SPREAD ANALYSIS
# ============================================================
st.subheader("📊 Rate Spread Analysis")
st.caption("How much rates differ across banks — wider spread = more savings potential")

bank_summary = cost_df.groupby('Bank').agg(
    Min_Rate=('Rate', 'min'), Max_Rate=('Rate', 'max'),
    Avg_Rate=('Rate', 'mean'), Min_Total=('Total', 'min')
).reset_index()

rate_spread = cost_df['Rate'].max() - cost_df['Rate'].min()
total_spread = cost_df['Total'].max() - cost_df['Total'].min()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rate Spread", f"{rate_spread:.2f}%")
c2.metric("Cost Spread", f"₹{total_spread:,.0f}")
c3.metric("Best Rate", f"{cost_df['Rate'].min():.2f}%")
c4.metric("Worst Rate", f"{cost_df['Rate'].max():.2f}%")

# Rate Range chart
fig_spread = go.Figure()
for _, row in bank_summary.iterrows():
    fig_spread.add_trace(go.Scatter(
        x=[row['Min_Rate'], row['Max_Rate']], y=[row['Bank'], row['Bank']],
        mode='lines', line=dict(color='#cbd5e1', width=8),
        showlegend=False, hoverinfo='skip'
    ))

fig_spread.add_trace(go.Scatter(
    x=bank_summary['Min_Rate'], y=bank_summary['Bank'],
    mode='markers+text', marker=dict(color='#10b981', size=14),
    text=bank_summary['Min_Rate'].apply(lambda x: f'{x:.2f}%'),
    textposition='middle right', name='Lowest'
))
fig_spread.add_trace(go.Scatter(
    x=bank_summary['Max_Rate'], y=bank_summary['Bank'],
    mode='markers+text', marker=dict(color='#ef4444', size=14),
    text=bank_summary['Max_Rate'].apply(lambda x: f'{x:.2f}%'),
    textposition='middle left', name='Highest'
))
fig_spread.add_trace(go.Scatter(
    x=bank_summary['Avg_Rate'], y=bank_summary['Bank'],
    mode='markers', marker=dict(color='#3b82f6', size=10, symbol='diamond'),
    name='Average'
))
fig_spread.update_layout(
    height=380, xaxis_title="Interest Rate (%)", yaxis_title="",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=30, b=0)
)
st.plotly_chart(fig_spread, width='stretch')

# Cost delta bar
st.markdown("#### 💰 Extra Cost vs Best")
bank_sorted = bank_summary.sort_values('Min_Total').reset_index(drop=True)
bank_sorted['Diff'] = bank_sorted['Min_Total'] - bank_sorted['Min_Total'].min()

fig_delta = go.Figure(go.Bar(
    x=bank_sorted['Bank'], y=bank_sorted['Diff'],
    marker_color=['#10b981' if d == 0 else '#f59e0b' if d < total_spread * 0.3 else '#ef4444' for d in bank_sorted['Diff']],
    text=bank_sorted['Diff'].apply(lambda x: 'Best' if x == 0 else f'+₹{x:,.0f}'),
    textposition='outside'
))
fig_delta.update_layout(height=350, xaxis_title="", yaxis_title="Extra Cost (₹)",
                        showlegend=False, margin=dict(l=0, r=0, t=20, b=0))
st.plotly_chart(fig_delta, width='stretch')

st.divider()

# ============================================================
# 4️⃣ VISUAL COMPARISON
# ============================================================
st.subheader("📈 Visual Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Total Cost by Bank**")
    bank_cost = cost_df.groupby('Bank')['Total'].min().reset_index().sort_values('Total')
    colors = ['#10b981' if b == best_bank else '#ef4444' if b == worst_bank else '#3b82f6' for b in bank_cost['Bank']]
    fig = go.Figure(go.Bar(
        x=bank_cost['Bank'], y=bank_cost['Total'],
        marker_color=colors,
        text=bank_cost['Total'].apply(lambda x: f'₹{x:,.0f}'),
        textposition='outside'
    ))
    min_v, max_v = bank_cost['Total'].min(), bank_cost['Total'].max()
    pad = (max_v - min_v) * 0.15 if max_v > min_v else min_v * 0.05
    fig.update_layout(height=380, yaxis=dict(range=[min_v - pad, max_v + pad]),
                      xaxis_title="", yaxis_title="Total Cost (₹)",
                      showlegend=False, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, width='stretch')

with col2:
    st.markdown("**Rate vs Extra Fee**")
    fig = px.scatter(cost_df, x='Rate', y='Fee %', size='Max Loan',
                     color='Bank', hover_name='Scheme',
                     labels={'Rate': 'Interest Rate (%)', 'Fee %': 'Processing Fee (%)'})
    fig.update_layout(height=380, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, width='stretch')

st.divider()

# ============================================================
# ⭐ 7 KEY BUSINESS QUESTIONS
# ============================================================
st.header("⭐ 7 Key Business Questions")
st.caption("Most important insights from our 35-question analysis")

# Q1
st.subheader("Q1️⃣ Which bank has the lowest rate?")
lowest_bank = cost_df.sort_values('Rate').iloc[0]
st.info(f"🏆 **{lowest_bank['Bank']}** at **{lowest_bank['Rate']:.2f}%** ({lowest_bank['Scheme']})")

fig_q1 = px.bar(cost_df.sort_values('Rate'), x='Rate', y='Scheme',
                color='Rate', color_continuous_scale=['#10b981', '#fbbf24', '#ef4444'],
                orientation='h', text='Rate')
fig_q1.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_q1.update_layout(height=max(280, len(cost_df) * 35), showlegend=False,
                     xaxis_title="Rate (%)", yaxis_title="",
                     yaxis={'categoryorder': 'total ascending'},
                     margin=dict(l=0, r=60, t=10, b=0))
st.plotly_chart(fig_q1, width='stretch')

st.divider()

# Q4
st.subheader("Q4️⃣ Which bank has the lowest processing fee?")
fee_summary = cost_df.groupby('Bank')['Fee %'].min().reset_index().sort_values('Fee %')
st.info(f"🏆 **{fee_summary.iloc[0]['Bank']}** at **{fee_summary.iloc[0]['Fee %']:.2f}%**")

fig_q4 = px.bar(fee_summary, x='Bank', y='Fee %',
                color='Fee %', color_continuous_scale=['#10b981', '#fbbf24', '#ef4444'],
                text='Fee %')
fig_q4.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_q4.update_layout(height=350, showlegend=False, xaxis_title="", yaxis_title="Fee (%)",
                     margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig_q4, width='stretch')

st.divider()

# Q7
st.subheader("Q7️⃣ Which banks offer no-collateral loans?")
no_coll = cost_df[cost_df['Collateral'].str.lower().str.contains('no', na=False)]
if not no_coll.empty:
    st.success(f"✅ **{', '.join(no_coll['Bank'].unique())}** offer no-collateral loans")
    fig_q7 = px.bar(no_coll.sort_values('Rate'), x='Rate', y='Scheme',
                    color='Bank', orientation='h', text='Rate')
    fig_q7.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_q7.update_layout(height=max(250, len(no_coll) * 40),
                         xaxis_title="Rate (%)", yaxis_title="",
                         yaxis={'categoryorder': 'total ascending'},
                         margin=dict(l=0, r=60, t=10, b=0))
    st.plotly_chart(fig_q7, width='stretch')
else:
    st.warning("No no-collateral loans match your current filters")

st.divider()

# Q12
st.subheader("Q12️⃣ What is the monthly EMI for each bank?")
lowest_emi = cost_df.sort_values('EMI').iloc[0]
highest_emi = cost_df.sort_values('EMI', ascending=False).iloc[0]
st.info(f"💡 EMI ranges from **₹{lowest_emi['EMI']:,.0f}** ({lowest_emi['Bank']}) to **₹{highest_emi['EMI']:,.0f}** ({highest_emi['Bank']})")

fig_q12 = px.bar(cost_df.sort_values('EMI'), x='EMI', y='Scheme',
                 color='Bank', orientation='h', text='EMI')
fig_q12.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
fig_q12.update_layout(height=max(280, len(cost_df) * 35),
                      xaxis_title="Monthly EMI (₹)", yaxis_title="",
                      yaxis={'categoryorder': 'total ascending'},
                      margin=dict(l=0, r=80, t=10, b=0))
st.plotly_chart(fig_q12, width='stretch')

st.divider()

# Q16
st.subheader("Q16️⃣ Public vs Private — who's cheaper?")
public_df = cost_df[cost_df['Bank Type'] == 'Public Sector']
private_df = cost_df[cost_df['Bank Type'] == 'Private Sector']

if not public_df.empty and not private_df.empty:
    pub_avg = public_df['Rate'].mean()
    pvt_avg = private_df['Rate'].mean()
    diff = abs(pub_avg - pvt_avg)
    cheaper = "Public" if pub_avg < pvt_avg else "Private"
    st.info(f"🏆 **{cheaper}** banks cheaper by **{diff:.2f}%** (Public: {pub_avg:.2f}% vs Private: {pvt_avg:.2f}%)")

    fig_q16 = px.box(cost_df, x='Bank Type', y='Rate', color='Bank Type',
                     points='all', labels={'Rate': 'Rate (%)', 'Bank Type': ''})
    fig_q16.update_layout(height=400, showlegend=False, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_q16, width='stretch')
else:
    st.info("Only one bank type in current filter")

st.divider()

# Q24
st.subheader("Q24️⃣ How much can I save?")
st.info(f"💰 Choosing **{best['Bank']}** saves **₹{savings:,.0f}** vs {worst['Bank']}")

fig_q24 = go.Figure(go.Waterfall(
    name="Cost", orientation="v",
    measure=["absolute", "relative", "relative", "total"],
    x=["Principal", "Interest", "Fee", "Total"],
    textposition="outside",
    text=[f"₹{loan_amount:,.0f}", f"+₹{best['Interest']:,.0f}", f"+₹{best['Fee']:,.0f}", f"₹{best['Total']:,.0f}"],
    y=[loan_amount, best['Interest'], best['Fee'], best['Total']],
    connector={"line": {"color": "rgb(63,63,63)"}},
    increasing={"marker": {"color": "#ef4444"}},
    decreasing={"marker": {"color": "#10b981"}},
    totals={"marker": {"color": "#3b82f6"}}
))
fig_q24.update_layout(height=400, xaxis_title="", yaxis_title="Amount (₹)",
                      margin=dict(l=0, r=0, t=20, b=0))
st.plotly_chart(fig_q24, width='stretch')

st.divider()

# Q31
st.subheader("Q31️⃣ How have rates changed over time?")
if not hist.empty:
    hist_f = hist[hist['bank'].isin(selected_banks)]
    hist_avg = hist_f.groupby('date')['interest_rate'].mean().reset_index()
    change = hist_avg.iloc[-1]['interest_rate'] - hist_avg.iloc[0]['interest_rate']
    direction = "📈 increased" if change > 0 else "📉 decreased" if change < 0 else "➡️ stable"
    st.info(f"📊 Rates have **{direction}** by **{abs(change):.2f}%** over 6 months")

    fig_q31 = px.line(hist_f, x='date', y='interest_rate', color='bank', markers=True,
                      labels={'interest_rate': 'Rate (%)', 'date': '', 'bank': ''})
    fig_q31.update_layout(height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                          margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig_q31, width='stretch')

st.divider()

# ============================================================
# 5️⃣ BANK DEEP-DIVE
# ============================================================
st.subheader("🔍 Bank Deep-Dive")
st.caption("Select a bank to see its full profile")

selected_bank = st.selectbox("Choose a bank:", options=sorted(df['bank'].unique().tolist()))

if selected_bank:
    bank_df = df[df['bank'] == selected_bank]
    bank_cost = cost_df[cost_df['Bank'] == selected_bank]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Lowest Rate", f"{bank_df['interest_rate'].min():.2f}%")
    c2.metric("Highest Rate", f"{bank_df['interest_rate'].max():.2f}%")
    c3.metric("Average Rate", f"{bank_df['interest_rate'].mean():.2f}%")
    c4.metric("Total Schemes", len(bank_df))

    if bank_cost.empty:
        st.warning(f"⚠️ No **{selected_bank}** scheme matches your ₹{loan_amount:,} loan.")
        alts = cost_df['Bank'].unique()[:3]
        st.info(f"💡 Try: {', '.join(alts)}")
    else:
        bank_best = bank_cost.sort_values('Total').iloc[0]
        st.success(f"🎯 **Recommended for you:** {bank_best['Scheme']} at **{bank_best['Rate']:.2f}%** — Total ₹{bank_best['Total']:,.0f}")

        st.markdown("#### 📋 All Schemes")
        st.dataframe(
            bank_df[['scheme_name', 'interest_rate', 'max_loan_amount',
                     'collateral_required', 'processing_fee_percent', 'best_for']].style.format({
                'interest_rate': '{:.2f}%', 'max_loan_amount': '₹{:,.0f}',
                'processing_fee_percent': '{:.2f}%'
            }),
            width='stretch'
        )

        st.markdown("#### ✨ Benefits")
        benefits = []
        if bank_df['collateral_needed'].eq('No').any(): benefits.append("✅ No-collateral loans available")
        if bank_df['processing_fee_percent'].eq(0).any(): benefits.append("✅ Zero processing fee")
        if bank_df['study_destination'].eq('Abroad').any(): benefits.append("✅ Abroad loans available")
        if bank_df['bank_type'].iloc[0] == 'Public Sector': benefits.append("✅ Government bank")
        else: benefits.append("✅ Private bank — faster processing")
        benefits.append("✅ RBI regulated and DICGC insured")
        for b in benefits: st.write(b)

        st.markdown("#### 🛡️ Safety Check")
        safety = {
            'SBI': {'rating': 'AAA', 'years': '200+ years'},
            'Bank of Baroda': {'rating': 'AAA', 'years': '115+ years'},
            'HDFC Bank': {'rating': 'AAA', 'years': '30+ years'},
            'ICICI Bank': {'rating': 'AAA', 'years': '30+ years'},
            'Axis Bank': {'rating': 'AAA', 'years': '30+ years'}
        }.get(selected_bank, {'rating': 'N/A', 'years': 'N/A'})

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"✅ **Credit Rating:** {safety['rating']}")
            st.write(f"✅ **Years:** {safety['years']}")
        with col2:
            st.write(f"✅ **RBI Regulated:** Yes")
            st.write(f"✅ **DICGC Insured:** Yes (₹5L)")

        st.markdown("#### 📊 Rate Range")
        fig = px.bar(
            bank_df.sort_values('interest_rate'),
            x='interest_rate', y='scheme_name', color='interest_rate',
            color_continuous_scale=['#10b981', '#fbbf24', '#ef4444'],
            orientation='h', text='interest_rate'
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(height=max(250, len(bank_df) * 45), showlegend=False,
                          xaxis_title="Rate (%)", yaxis_title="",
                          yaxis={'categoryorder': 'total ascending'},
                          margin=dict(l=0, r=60, t=10, b=0))
        st.plotly_chart(fig, width='stretch')

st.divider()

# ============================================================
# 6️⃣ TRENDS
# ============================================================
st.subheader("📈 6-Month Rate Trends")
hist_filtered = hist[hist['bank'].isin(selected_banks)]
fig = px.line(hist_filtered, x='date', y='interest_rate', color='bank', markers=True,
              labels={'interest_rate': 'Rate (%)', 'date': '', 'bank': ''})
fig.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig, width='stretch')

st.caption("🎓 EduLoan Intelligence · Real data from official bank websites")

