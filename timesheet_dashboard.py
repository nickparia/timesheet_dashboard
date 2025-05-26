import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from io import StringIO

# Set page config
st.set_page_config(
    page_title="ACMI - Timesheet Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom color scheme - Professional navy and blue */
    :root {
        --primary-color: #1f2937;
        --secondary-color: #3b82f6;
        --accent-color: #10b981;
        --background-color: #f8fafc;
        --card-background: #ffffff;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --border-color: #e5e7eb;
    }
    
    /* Main title styling */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: var(--primary-color);
        text-align: center;
        margin: 2rem 0;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        border-bottom: 3px solid var(--secondary-color);
        padding-bottom: 1rem;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Metric cards styling */
    .metric-card {
        background: linear-gradient(135deg, var(--card-background) 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Alert boxes */
    .alert-box {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        border-left: 4px solid;
        font-weight: 500;
    }
    
    .alert-warning {
        background-color: #fef3c7;
        border-left-color: #f59e0b;
        color: #92400e;
    }
    
    .alert-success {
        background-color: #d1fae5;
        border-left-color: var(--accent-color);
        color: #065f46;
    }
    
    .alert-info {
        background-color: #dbeafe;
        border-left-color: var(--secondary-color);
        color: #1e40af;
    }
    
    /* Professional buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--secondary-color) 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--background-color);
    }
    
    /* Tab styling - More aggressive approach */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--background-color);
        padding: 1rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--card-background) !important;
        border-radius: 8px !important;
        border: 1px solid var(--border-color) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        color: #1f2937 !important;
        min-height: 45px !important;
    }
    
    .stTabs [data-baseweb="tab"] > div {
        color: #1f2937 !important;
    }
    
    .stTabs [data-baseweb="tab"] span {
        color: #1f2937 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f5f9 !important;
        border-color: var(--secondary-color) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--secondary-color) 0%, #2563eb 100%) !important;
        color: white !important;
        border-color: var(--secondary-color) !important;
    }
    
    .stTabs [aria-selected="true"] > div {
        color: white !important;
    }
    
    .stTabs [aria-selected="true"] span {
        color: white !important;
    }
    
    /* Header section */
    .header-section {
        background: linear-gradient(135deg, var(--primary-color) 0%, #374151 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Professional data tables */
    .dataframe {
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-success {
        background-color: #d1fae5;
        color: #065f46;
    }
    
    .status-warning {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    .status-error {
        background-color: #fee2e2;
        color: #991b1b;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-color);
        border-left: 4px solid var(--secondary-color);
        padding-left: 1rem;
        margin: 2rem 0 1rem 0;
    }
    
    /* Company branding */
    .company-logo {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--secondary-color) 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load and cache data
@st.cache_data
def load_data(uploaded_file=None):
    """Load and preprocess the timesheet data"""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        try:
            df = pd.read_csv('Detailweergaveuren (5).csv')
        except FileNotFoundError:
            return None
    
    # Convert date column to datetime
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d-%m-%Y')
    
    # Extract additional date features
    df['Year'] = df['Datum'].dt.year
    df['Month'] = df['Datum'].dt.month
    df['Month_Name'] = df['Datum'].dt.strftime('%B')
    df['Quarter'] = df['Datum'].dt.quarter
    df['Day_of_Week'] = df['Datum'].dt.day_name()
    df['Week'] = df['Datum'].dt.isocalendar().week
    df['Year_Week'] = df['Datum'].dt.strftime('%Y-W%U')
    
    # Clean numeric columns
    df['Aantal'] = pd.to_numeric(df['Aantal'], errors='coerce')
    df['Uurtarief'] = pd.to_numeric(df['Uurtarief'], errors='coerce')
    df['Totaal'] = pd.to_numeric(df['Totaal'], errors='coerce')
    
    # Fill missing values
    df = df.fillna({'Projectleider': 'Unassigned', 'Projectnummer': 'N/A'})
    
    # Add working day flags
    df['Is_Weekend'] = df['Day_of_Week'].isin(['Saturday', 'Sunday'])
    df['Is_Leave'] = df['Categorie'].str.contains('Leave|Absence', case=False, na=False)
    
    return df

# Data upload section
st.markdown("""
<div class="header-section">
    <div class="company-logo">ACMI</div>
    <div class="subtitle">Timesheet Analytics Platform</div>
    <p style="margin: 0; opacity: 0.9;">Advanced workforce analytics and compliance monitoring</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📁 Upload Timesheet Data", 
    type=['csv'],
    help="Upload your Detailweergaveuren CSV file to begin analysis"
)

# Load data
df = load_data(uploaded_file)

if df is None:
    st.markdown("""
    <div class="alert-box alert-info">
        <strong>🚀 Getting Started</strong><br>
        Please upload your timesheet CSV file to access the analytics platform.<br>
        <small>Expected format: CSV with columns including Medewerker, Datum, Aantal, Categorie, etc.</small>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

st.markdown("""
<div class="alert-box alert-success">
    <strong>✅ Data Successfully Loaded</strong><br>
    """ + f"{len(df):,} records processed and ready for analysis" + """
</div>
""", unsafe_allow_html=True)

# Helper functions for date calculations
def get_last_week_dates():
    today = datetime.now()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    return last_monday.date(), last_sunday.date()

def get_last_month_dates():
    today = datetime.now()
    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)
    return first_day_last_month.date(), last_day_last_month.date()

def get_last_quarter_dates():
    today = datetime.now()
    current_quarter = (today.month - 1) // 3 + 1
    if current_quarter == 1:
        last_quarter_start = datetime(today.year - 1, 10, 1)
        last_quarter_end = datetime(today.year - 1, 12, 31)
    else:
        quarter_start_month = (current_quarter - 2) * 3 + 1
        last_quarter_start = datetime(today.year, quarter_start_month, 1)
        last_quarter_end = datetime(today.year, quarter_start_month + 2, 1) - timedelta(days=1)
    return last_quarter_start.date(), last_quarter_end.date()

def get_last_year_dates():
    today = datetime.now()
    last_year = today.year - 1
    return datetime(last_year, 1, 1).date(), datetime(last_year, 12, 31).date()

# Sidebar filters
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem; margin-bottom: 1rem; background: linear-gradient(135deg, #1f2937 0%, #374151 100%); border-radius: 8px; color: white;">
    <h3 style="margin: 0; color: white;">🔍 Analytics Filters</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.9rem;">Customize your data view</p>
</div>
""", unsafe_allow_html=True)

# Date range filter
date_min = df['Datum'].min().date()
date_max = df['Datum'].max().date()
selected_date_range = st.sidebar.date_input(
    "Date Range",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

# Employee filter
employees = ['All'] + sorted(df['Medewerker'].unique().tolist())
selected_employees = st.sidebar.multiselect(
    "Employees",
    employees,
    default=['All']
)

# Project filter
projects = ['All'] + sorted(df['Project'].unique().tolist())
selected_projects = st.sidebar.multiselect(
    "Projects",
    projects,
    default=['All']
)

# Client filter
clients = ['All'] + sorted(df['Relatie'].unique().tolist())
selected_clients = st.sidebar.multiselect(
    "Clients",
    clients,
    default=['All']
)

# Category filter
categories = ['All'] + sorted(df['Categorie'].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Categories",
    categories,
    default=['All']
)

# Apply filters function
def apply_filters(dataframe):
    filtered_df = dataframe.copy()
    
    # Date filter
    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
        filtered_df = filtered_df[
            (filtered_df['Datum'].dt.date >= start_date) & 
            (filtered_df['Datum'].dt.date <= end_date)
        ]
    
    # Employee filter
    if 'All' not in selected_employees and selected_employees:
        filtered_df = filtered_df[filtered_df['Medewerker'].isin(selected_employees)]
    
    # Project filter
    if 'All' not in selected_projects and selected_projects:
        filtered_df = filtered_df[filtered_df['Project'].isin(selected_projects)]
    
    # Client filter
    if 'All' not in selected_clients and selected_clients:
        filtered_df = filtered_df[filtered_df['Relatie'].isin(selected_clients)]
    
    # Category filter
    if 'All' not in selected_categories and selected_categories:
        filtered_df = filtered_df[filtered_df['Categorie'].isin(selected_categories)]
    
    return filtered_df

# Apply filters
filtered_df = apply_filters(df)

# Display filtered data info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Current Selection")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Records", f"{len(filtered_df):,}")
    st.metric("Hours", f"{filtered_df['Aantal'].sum():.0f}")
with col2:
    st.metric("Revenue", f"€{filtered_df['Totaal'].sum()/1000:.0f}K")
    st.metric("Employees", len(filtered_df['Medewerker'].unique()))

# Main dashboard content
st.markdown("### 📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin: 0; color: #3b82f6;">⏰ Total Hours</h3>
        <h2 style="margin: 0.5rem 0 0 0; color: #1f2937;">""" + f"{filtered_df['Aantal'].sum():,.0f}" + """</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin: 0; color: #10b981;">💰 Total Revenue</h3>
        <h2 style="margin: 0.5rem 0 0 0; color: #1f2937;">€""" + f"{filtered_df['Totaal'].sum():,.0f}" + """</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin: 0; color: #f59e0b;">📊 Avg Rate</h3>
        <h2 style="margin: 0.5rem 0 0 0; color: #1f2937;">€""" + f"{filtered_df['Uurtarief'].mean():.0f}" + """/hr</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin: 0; color: #8b5cf6;">👥 Active Staff</h3>
        <h2 style="margin: 0.5rem 0 0 0; color: #1f2937;">""" + f"{len(filtered_df['Medewerker'].unique())}" + """</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Create tabs for different views
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Executive Dashboard", 
    "👥 Workforce Analytics", 
    "📋 Project Performance", 
    "💼 Client Portfolio", 
    "🔍 Advanced Analytics", 
    "📊 Data Export"
])

with tab1:
    st.markdown('<div class="section-header">Executive Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hours by category
        category_hours = filtered_df.groupby('Categorie')['Aantal'].sum().reset_index()
        fig1 = px.pie(category_hours, values='Aantal', names='Categorie', 
                     title="Hours Distribution by Category")
        st.plotly_chart(fig1, use_container_width=True)
        
        # Hours by month
        monthly_hours = filtered_df.groupby('Month_Name')['Aantal'].sum().reset_index()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_hours['Month_Name'] = pd.Categorical(monthly_hours['Month_Name'], 
                                                   categories=month_order, ordered=True)
        monthly_hours = monthly_hours.sort_values('Month_Name')
        
        fig2 = px.bar(monthly_hours, x='Month_Name', y='Aantal', 
                     title="Hours by Month")
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Revenue by category
        category_revenue = filtered_df.groupby('Categorie')['Totaal'].sum().reset_index()
        fig3 = px.pie(category_revenue, values='Totaal', names='Categorie', 
                     title="Revenue Distribution by Category")
        st.plotly_chart(fig3, use_container_width=True)
        
        # Daily hours trend
        daily_hours = filtered_df.groupby('Datum')['Aantal'].sum().reset_index()
        fig4 = px.line(daily_hours, x='Datum', y='Aantal', 
                      title="Daily Hours Trend")
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.markdown('<div class="section-header">Workforce Analytics</div>', unsafe_allow_html=True)
    
    # Quick access buttons
    st.markdown("#### 🚀 Quick Period Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📅 Last Week", key="last_week", use_container_width=True):
            st.session_state.time_period = "last_week"
    with col2:
        if st.button("📅 Last Month", key="last_month", use_container_width=True):
            st.session_state.time_period = "last_month"
    with col3:
        if st.button("📅 Last Quarter", key="last_quarter", use_container_width=True):
            st.session_state.time_period = "last_quarter"
    with col4:
        if st.button("📅 Last Year", key="last_year", use_container_width=True):
            st.session_state.time_period = "last_year"
    
    # Handle time period selection
    if 'time_period' not in st.session_state:
        st.session_state.time_period = None
    
    period_data = None
    period_name = ""
    
    if st.session_state.time_period == "last_week":
        start_date, end_date = get_last_week_dates()
        period_data = filtered_df[(filtered_df['Datum'].dt.date >= start_date) & (filtered_df['Datum'].dt.date <= end_date)]
        period_name = f"Last Week ({start_date} to {end_date})"
    elif st.session_state.time_period == "last_month":
        start_date, end_date = get_last_month_dates()
        period_data = filtered_df[(filtered_df['Datum'].dt.date >= start_date) & (filtered_df['Datum'].dt.date <= end_date)]
        period_name = f"Last Month ({start_date.strftime('%B %Y')})"
    elif st.session_state.time_period == "last_quarter":
        start_date, end_date = get_last_quarter_dates()
        period_data = filtered_df[(filtered_df['Datum'].dt.date >= start_date) & (filtered_df['Datum'].dt.date <= end_date)]
        period_name = f"Last Quarter ({start_date} to {end_date})"
    elif st.session_state.time_period == "last_year":
        start_date, end_date = get_last_year_dates()
        period_data = filtered_df[(filtered_df['Datum'].dt.date >= start_date) & (filtered_df['Datum'].dt.date <= end_date)]
        period_name = f"Last Year ({start_date.year})"
    
    if period_data is not None:
        st.markdown(f"#### 📊 Analysis for {period_name}")
        
        # Employee activity in selected period
        period_summary = period_data.groupby('Medewerker').agg({
            'Aantal': 'sum',
            'Totaal': 'sum',
            'Project': 'nunique',
            'Datum': ['min', 'max']
        }).round(2)
        
        period_summary.columns = ['Total Hours', 'Total Revenue', 'Projects Worked', 'First Entry', 'Last Entry']
        period_summary = period_summary.sort_values('Total Hours', ascending=False)
        
        st.dataframe(period_summary, use_container_width=True)
        
        # Visualization for the period
        if len(period_summary) > 0:
            fig_period = px.bar(
                x=period_summary.index[:15], 
                y=period_summary['Total Hours'][:15],
                title=f"Top 15 Employees by Hours - {period_name}",
                labels={'x': 'Employee', 'y': 'Hours'},
                color_discrete_sequence=['#3b82f6']
            )
            fig_period.update_layout(
                xaxis_tickangle=45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_family="Arial, sans-serif"
            )
            st.plotly_chart(fig_period, use_container_width=True)
    
    st.markdown("---")
    
    # Incomplete timesheet detection for last week
    st.markdown("#### ⚠️ Compliance Monitoring - Last Week")
    
    last_week_start, last_week_end = get_last_week_dates()
    last_week_data = filtered_df[
        (filtered_df['Datum'].dt.date >= last_week_start) & 
        (filtered_df['Datum'].dt.date <= last_week_end)
    ]
    
    # Calculate working days (Monday-Friday) in last week
    working_days_last_week = pd.date_range(start=last_week_start, end=last_week_end, freq='D')
    working_days_last_week = [d for d in working_days_last_week if d.weekday() < 5]  # Mon-Fri only
    expected_hours = len(working_days_last_week) * 8  # Assuming 8 hours per working day
    
    # Group by employee for last week
    last_week_employee_hours = last_week_data.groupby('Medewerker').agg({
        'Aantal': 'sum',
        'Is_Leave': 'any'  # Check if employee had any leave
    }).round(1)
    
    last_week_employee_hours.columns = ['Hours Logged', 'Had Leave']
    
    # Identify employees who didn't log full week and weren't on leave
    incomplete_timesheets = last_week_employee_hours[
        (last_week_employee_hours['Hours Logged'] < expected_hours) & 
        (last_week_employee_hours['Had Leave'] == False)
    ]
    
    if len(incomplete_timesheets) > 0:
        st.markdown(f"""
        <div class="alert-box alert-warning">
            <strong>⚠️ {len(incomplete_timesheets)} employees have incomplete timesheets for last week</strong><br>
            Expected: {expected_hours} hours ({len(working_days_last_week)} working days × 8 hours)
        </div>
        """, unsafe_allow_html=True)
        
        # Show incomplete timesheets
        incomplete_display = incomplete_timesheets.copy()
        incomplete_display['Hours Missing'] = expected_hours - incomplete_display['Hours Logged']
        incomplete_display = incomplete_display.sort_values('Hours Missing', ascending=False)
        
        st.dataframe(incomplete_display[['Hours Logged', 'Hours Missing']], use_container_width=True)
    else:
        st.markdown(f"""
        <div class="alert-box alert-success">
            <strong>✅ All employees have complete timesheets for last week!</strong><br>
            All active employees logged at least {expected_hours} hours or were on approved leave.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Overall employee summary
    st.markdown("#### 📊 Workforce Performance Summary")
    
    employee_summary = filtered_df.groupby('Medewerker').agg({
        'Aantal': 'sum',
        'Totaal': 'sum',
        'Uurtarief': 'mean',
        'Project': 'nunique'
    }).round(2)
    employee_summary.columns = ['Total Hours', 'Total Revenue', 'Avg Rate', 'Projects Count']
    employee_summary = employee_summary.sort_values('Total Hours', ascending=False)
    
    st.dataframe(employee_summary, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top employees by hours
        top_employees = employee_summary.head(10)
        fig5 = px.bar(top_employees, x=top_employees.index, y='Total Hours',
                     title="Top 10 Employees by Hours")
        fig5.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Employee rate distribution
        fig6 = px.histogram(filtered_df, x='Uurtarief', nbins=20,
                           title="Employee Rate Distribution")
        st.plotly_chart(fig6, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header">Project Performance Analytics</div>', unsafe_allow_html=True)
    
    # Project summary table
    project_summary = filtered_df.groupby('Project').agg({
        'Aantal': 'sum',
        'Totaal': 'sum',
        'Medewerker': 'nunique',
        'Uurtarief': 'mean'
    }).round(2)
    project_summary.columns = ['Total Hours', 'Total Revenue', 'Employee Count', 'Avg Rate']
    project_summary = project_summary.sort_values('Total Hours', ascending=False)
    
    st.dataframe(project_summary, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top projects by hours
        top_projects = project_summary.head(10)
        fig7 = px.bar(top_projects, x=top_projects.index, y='Total Hours',
                     title="Top 10 Projects by Hours")
        fig7.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig7, use_container_width=True)
    
    with col2:
        # Project revenue vs hours scatter
        fig8 = px.scatter(project_summary, x='Total Hours', y='Total Revenue',
                        hover_data=['Employee Count'], 
                        title="Project Revenue vs Hours")
        st.plotly_chart(fig8, use_container_width=True)

with tab4:
    st.markdown('<div class="section-header">Client Portfolio Analytics</div>', unsafe_allow_html=True)
    
    # Client summary table
    client_summary = filtered_df.groupby('Relatie').agg({
        'Aantal': 'sum',
        'Totaal': 'sum',
        'Project': 'nunique',
        'Medewerker': 'nunique'
    }).round(2)
    client_summary.columns = ['Total Hours', 'Total Revenue', 'Project Count', 'Employee Count']
    client_summary = client_summary.sort_values('Total Revenue', ascending=False)
    
    st.dataframe(client_summary, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top clients by revenue
        top_clients = client_summary.head(10)
        fig9 = px.bar(top_clients, x=top_clients.index, y='Total Revenue',
                     title="Top 10 Clients by Revenue")
        fig9.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        # Client hours distribution
        fig10 = px.pie(client_summary.head(8), values='Total Hours', 
                      names=client_summary.head(8).index,
                      title="Hours Distribution by Top Clients")
        st.plotly_chart(fig10, use_container_width=True)

with tab5:
    st.markdown('<div class="section-header">Advanced Data Analytics</div>', unsafe_allow_html=True)
    
    # Advanced filtering options
    st.markdown("#### Advanced Filtering Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_hours = st.number_input("Minimum Hours", min_value=0.0, value=0.0, step=0.5)
        max_hours = st.number_input("Maximum Hours", min_value=0.0, value=float(filtered_df['Aantal'].max()), step=0.5)
    
    with col2:
        min_rate = st.number_input("Minimum Rate (€)", min_value=0.0, value=0.0, step=5.0)
        max_rate = st.number_input("Maximum Rate (€)", min_value=0.0, value=float(filtered_df['Uurtarief'].max()), step=5.0)
    
    with col3:
        search_term = st.text_input("Search in Description/Project:")
        exclude_zero_hours = st.checkbox("Exclude Zero Hours", value=False)
    
    # Apply advanced filters
    advanced_filtered_df = filtered_df.copy()
    
    # Hours filter
    advanced_filtered_df = advanced_filtered_df[
        (advanced_filtered_df['Aantal'] >= min_hours) & 
        (advanced_filtered_df['Aantal'] <= max_hours)
    ]
    
    # Rate filter
    advanced_filtered_df = advanced_filtered_df[
        (advanced_filtered_df['Uurtarief'] >= min_rate) & 
        (advanced_filtered_df['Uurtarief'] <= max_rate)
    ]
    
    # Search filter
    if search_term:
        mask = (
            advanced_filtered_df['Project'].str.contains(search_term, case=False, na=False) |
            advanced_filtered_df['Toelichting'].str.contains(search_term, case=False, na=False) |
            advanced_filtered_df['Urensoort'].str.contains(search_term, case=False, na=False)
        )
        advanced_filtered_df = advanced_filtered_df[mask]
    
    # Zero hours filter
    if exclude_zero_hours:
        advanced_filtered_df = advanced_filtered_df[advanced_filtered_df['Aantal'] > 0]
    
    st.info(f"📊 Found {len(advanced_filtered_df)} records matching your criteria")
    
    # Display results
    display_columns = ['Medewerker', 'Datum', 'Project', 'Relatie', 'Categorie', 
                      'Urensoort', 'Aantal', 'Uurtarief', 'Totaal', 'Toelichting']
    
    if len(advanced_filtered_df) > 0:
        display_df = advanced_filtered_df[display_columns].copy()
        display_df['Datum'] = display_df['Datum'].dt.strftime('%d-%m-%Y')
        
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # Summary stats for filtered data
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Hours", f"{advanced_filtered_df['Aantal'].sum():.1f}")
        with col2:
            st.metric("Total Revenue", f"€{advanced_filtered_df['Totaal'].sum():,.2f}")
        with col3:
            st.metric("Avg Rate", f"€{advanced_filtered_df['Uurtarief'].mean():.2f}")
        with col4:
            st.metric("Employees", advanced_filtered_df['Medewerker'].nunique())
    
    # Download filtered data
    if st.button("📥 Download Filtered Data"):
        csv = advanced_filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f'filtered_timesheet_data_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
            mime='text/csv'
        )

with tab6:
    st.markdown('<div class="section-header">Data Export & Raw Analysis</div>', unsafe_allow_html=True)
    
    # Search and filter options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("Search in all columns:")
    
    with col2:
        show_all = st.checkbox("Show all columns", value=False)
    
    # Apply search filter
    display_df = filtered_df.copy()
    if search_term:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    # Select columns to display
    if not show_all:
        key_columns = ['Medewerker', 'Datum', 'Project', 'Relatie', 'Categorie', 
                      'Urensoort', 'Aantal', 'Uurtarief', 'Totaal']
        display_columns = [col for col in key_columns if col in display_df.columns]
        display_df = display_df[display_columns]
    
    # Format date for display
    if 'Datum' in display_df.columns:
        display_df = display_df.copy()
        display_df['Datum'] = display_df['Datum'].dt.strftime('%d-%m-%Y')
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name='filtered_timesheet_data.csv',
        mime='text/csv'
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem; background-color: #f8fafc; border-radius: 8px; margin-top: 2rem;'>
    <div style='font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;'>ACMI</div>
    <p style="margin: 0; font-weight: 500;">Timesheet Analytics Platform</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Advanced workforce intelligence • Real-time compliance monitoring • Strategic insights</p>
</div>
""", unsafe_allow_html=True)
