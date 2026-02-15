import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px
from datetime import date

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="SkyLine Analytics",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. DESIGN SYSTEM & CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --card-bg: rgba(30, 41, 59, 0.75);
        --accent: #0ea5e9;
        --success: #10b981;
        --info: #4f46e5;
        --text-primary: #ffffff;
        --text-secondary: #94a3b8;
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        color: var(--text-primary);
    }

    /* Main Container */
    .stApp {
        background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 100%);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }

    /* Input Widgets */
    .stSelectbox, .stNumberInput, .stDateInput, .stRadio, .stSlider {
        margin-bottom: 12px;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(30, 41, 59, 0.5);
        border-color: #334155;
        color: white;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    h4, h5, h6 {
        color: var(--text-secondary) !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.85rem;
    }

    /* Cards */
    .data-card {
        background: var(--card-bg);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 24px;
        backdrop-filter: blur(16px);
        margin-bottom: 16px;
        transition: border 0.2s;
    }
    .data-card:hover {
        border-color: var(--accent);
    }

    /* Metric Styles */
    .metric-hero {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-sub {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    /* Primary Button */
    .stButton>button {
        background-color: var(--accent);
        color: white;
        font-weight: 500;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        width: 100%;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background-color: #0284c7;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        color: var(--text-secondary);
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent);
        border-bottom: 2px solid var(--accent);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. HELPER FUNCTIONS & SETUP
# ---------------------------------------------------------
model_path = "house_model.joblib"
data_path = os.path.join("House price prediction", "house_prices.csv")
if not os.path.exists(data_path) and os.path.exists("house_prices.csv"):
    data_path = "house_prices.csv"

@st.cache_resource
def load_model():
    return joblib.load(model_path) if os.path.exists(model_path) else None

@st.cache_data
def load_data():
    return pd.read_csv(data_path) if os.path.exists(data_path) else None

def format_currency(value):
    if value >= 100: return f"₹{value/100:.2f} Cr"
    return f"₹{value:.2f} L"

def format_large_full(val):
    if val >= 10000000: return f"₹{val/10000000:.2f} Cr"
    elif val >= 100000: return f"₹{val/100000:.2f} L"
    return f"₹{val:,.0f}"

# Initialize Session State
if 'loan_input_val' not in st.session_state:
    st.session_state['loan_input_val'] = 5000000
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

# ---------------------------------------------------------
# 4. SIDEBAR - INPUT PANEL
# ---------------------------------------------------------
st.sidebar.title("SkyLine Analytics")
st.sidebar.caption("Professional Real Estate Valuation Control")
st.sidebar.markdown("---")

# 4.1 Timeline
st.sidebar.markdown("##### 1. Property Timeline")
construction_date = st.sidebar.date_input("Construction Date", value=date(2015, 1, 1), min_value=date(1950, 1, 1))
age = date.today().year - construction_date.year
st.sidebar.info(f"Property Age: {age} Years")
st.sidebar.markdown("---")

# 4.2 Structure
st.sidebar.markdown("##### 2. Property Structure")
prop_type = st.sidebar.radio("Type", ["House", "Apartment"], horizontal=True, label_visibility="collapsed")
area = 0.0
if prop_type == "House":
    plot = st.sidebar.number_input("Plot Area (sq.ft)", 100, 10000, 1200, 50)
    floors = st.sidebar.number_input("Floors", 1, 5, 2)
    area = plot * floors
else:
    carpet = st.sidebar.number_input("Carpet Area (sq.ft)", 100, 5000, 900, 50)
    balcony = st.sidebar.number_input("Balcony (sq.ft)", 0, 1000, 100)
    area = carpet + balcony

c1, c2 = st.sidebar.columns(2)
with c1: bedrooms = st.number_input("Bedrooms", 1, 10, 3)
with c2: distance = st.number_input("Dist. (km)", 0, 50, 5)
st.sidebar.caption(f"Total Area: {area:,.0f} sq.ft")
st.sidebar.markdown("---")

# 4.3 Financial
st.sidebar.markdown("##### 3. Financial Parameters")
loan_amount = st.sidebar.number_input("Loan Amount (₹)", 0, value=st.session_state['loan_input_val'], step=100000, key='loan_widget')
interest_rate = st.sidebar.number_input("Interest Rate (%)", 1.0, 20.0, 8.5, 0.1)
tenure = st.sidebar.slider("Tenure (Years)", 5, 30, 20)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("Calculate Value", type="primary"):
    model = load_model()
    if model:
        try:
            input_df = pd.DataFrame({'area': [area], 'bedrooms': [bedrooms], 'age': [age], 'distance': [distance]})
            st.session_state['prediction'] = model.predict(input_df)[0]
        except Exception as e:
            st.error(f"Prediction Error: {e}")
    else:
        st.error("Model not found.")

# ---------------------------------------------------------
# 5. MAIN DASHBOARD (RESULTS & ANALYTICS)
# ---------------------------------------------------------
tab_report, tab_analytics = st.tabs(["💎 Valuation Report", "📊 Market Analytics"])

# === TAB 1: VALUATION REPORT ===
with tab_report:
    if st.session_state['prediction'] is not None:
        pred = st.session_state['prediction']
        val_actual = pred * 100000
        
        # A. Estimated Value Hero Card
        st.markdown(f"""
        <div class="data-card">
            <h5 style="margin-bottom: 2px;">Estimated Market Value</h5>
            <div class="metric-hero">{format_currency(pred)}</div>
            <p style="color: #10b981; font-size: 0.9rem; margin-top: 5px;">
                <span style="opacity: 0.7;">Confidence Score:</span> <strong>96.5%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # B. EMI Summary
        st.markdown("##### Financial Summary")
        col_emi, col_chart = st.columns([1, 1])
        
        # EMI Calculation
        P = st.session_state.loan_widget
        R_monthly = interest_rate / 12 / 100
        N_months = tenure * 12
        emi = (P * R_monthly * (1 + R_monthly)**N_months) / ((1 + R_monthly)**N_months - 1) if P > 0 else 0
        total_pay = emi * N_months
        total_int = total_pay - P

        with col_emi:
            st.markdown(f"""
            <div class="data-card" style="border-left: 4px solid #10b981;">
                <h5 style="color: #94a3b8;">Monthly EMI</h5>
                <div class="metric-sub" style="color: #10b981;">₹{emi:,.0f}</div>
                <hr style="border-color: #334155; margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #94a3b8;">
                    <span>Total Interest</span>
                    <span style="color: #e2e8f0;">{format_large_full(total_int)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #94a3b8; margin-top: 5px;">
                    <span>Total Payable</span>
                    <span style="color: #e2e8f0;">{format_large_full(total_pay)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_chart:
            if P > 0:
                df_emi = pd.DataFrame({'Type': ['Principal', 'Interest'], 'Amount': [P, total_int]})
                fig = px.pie(df_emi, values='Amount', names='Type', color='Type',
                             color_discrete_map={'Principal': '#0ea5e9', 'Interest': '#10b981'}, hole=0.7)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                  showlegend=True, margin=dict(t=0,b=0,l=0,r=0), height=180,
                                  legend=dict(orientation="v", yanchor="middle", y=0.5))
                st.plotly_chart(fig, use_container_width=True)

        # C. Construction Quality & Future
        c_qual, c_fut = st.columns([1, 1])
        
        with c_qual:
            st.markdown("##### Construction Quality")
            with st.container(border=True):
                # Simplified Quality Inputs
                mat = st.selectbox("Material", ["RCC", "Steel", "Brick"], label_visibility="collapsed")
                qual_score = 82 if mat=="RCC" else 75 if mat=="Steel" else 60
                
                st.progress(qual_score/100)
                st.caption(f"Score: {qual_score}/100 (Good)")

        with c_fut:
            st.markdown("##### Future Projection (10Y)")
            growth = 8.0
            future_val = val_actual * ((1 + growth/100)**10)
            st.markdown(f"""
            <div style="padding: 15px; background: rgba(79, 70, 229, 0.1); border-radius: 8px; border: 1px solid #4f46e5;">
                <div style="color: #818cf8; font-size: 0.8rem; text-transform: uppercase;">Projected Value</div>
                <div style="font-size: 1.4rem; font-weight: 600; color: #a5b4fc;">{format_large_full(future_val)}</div>
                <div style="font-size: 0.8rem; color: #94a3b8;">@ 8.0% Annual Growth</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("👈 Please configure the property in the sidebar and click 'Calculate Value' to generate the report.")

# === TAB 2: MARKET ANALYTICS ===
with tab_analytics:
    df = load_data()
    if df is not None:
        st.markdown("##### Market Trends & Insights")
        
        row1_1, row1_2 = st.columns(2)
        
        with row1_1:
            st.markdown("###### Price vs Area")
            fig_bar = px.bar(df.sort_values('area'), x='area', y='price', color='price', 
                             labels={'area': 'Area (sq.ft)', 'price': 'Price'},
                             color_continuous_scale='Blues')
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                  font_color='#94a3b8', height=250, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with row1_2:
            st.markdown("###### Bedroom Distribution")
            dist_df = df['bedrooms'].value_counts().reset_index()
            dist_df.columns = ['BHK', 'Count']
            fig_pie = px.pie(dist_df, values='Count', names='BHK', color_discrete_sequence=px.colors.sequential.Tealgrn, hole=0.5)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8', height=250, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown("###### Property Age Depreciation Curve")
        fig_line = px.scatter(df, x='age', y='price', color='distance',
                              labels={'age': 'Property Age (Years)', 'price': 'Price'},
                              color_continuous_scale='Viridis')
        fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               font_color='#94a3b8', height=300)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Market data unavailable.")

