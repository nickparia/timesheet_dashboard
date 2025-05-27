import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from io import StringIO
import re

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
    
    /* Tab styling */
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
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f5f9 !important;
        border-color: var(--secondary-color) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--secondary-color) 0%, #2563eb 100%) !important;
        color: white !important;
        border-color: var(--secondary-color) !important;
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

# Secure Chatbot Class
class SecureTimesheetChatbot:
    def __init__(self, df):
        self.df = df
        self.conversation_history = []
    
    def analyze_query(self, user_question):
        """Analyze user question using pattern matching - no API key needed"""
        
        question = user_question.lower().strip()
        
        # Employee-related queries
        if self._contains_patterns(question, ['who worked', 'top employee', 'most hours', 'best performer']):
            return self._get_top_employees(question)
        
        # Project-related queries  
        elif self._contains_patterns(question, ['project', 'which project', 'top project']):
            return self._get_project_insights(question)
        
        # Time period queries
        elif self._contains_patterns(question, ['last week', 'last month', 'this month', 'last quarter']):
            return self._get_time_period_analysis(question)
        
        # Compliance queries
        elif self._contains_patterns(question, ['compliance', 'missing', 'incomplete', 'not submitted']):
            return self._check_compliance_issues()
        
        # Total/summary queries
        elif self._contains_patterns(question, ['total', 'sum', 'how much', 'how many']):
            return self._get_totals(question)
        
        # Revenue queries
        elif self._contains_patterns(question, ['revenue', 'money', 'billing', 'cost']):
            return self._get_revenue_insights(question)
        
        # Trend queries
        elif self._contains_patterns(question, ['trend', 'pattern', 'increase', 'decrease', 'growth']):
            return self._analyze_trends()
        
        # Client queries
        elif self._contains_patterns(question, ['client', 'customer', 'relatie']):
            return self._get_client_insights()
        
        # Comparison queries
        elif self._contains_patterns(question, ['compare', 'vs', 'versus', 'difference']):
            return self._compare_periods()
        
        # Help/general queries
        else:
            return self._get_help_response()
    
    def _contains_patterns(self, text, patterns):
        """Check if text contains any of the specified patterns"""
        return any(pattern in text for pattern in patterns)
    
    def _get_top_employees(self, question):
        """Get top performing employees"""
        emp_hours = self.df.groupby('Medewerker')['Aantal'].sum().sort_values(ascending=False)
        top_3 = emp_hours.head(3)
        
        response = "🏆 **Top Performing Employees:**\n\n"
        for i, (emp, hours) in enumerate(top_3.items(), 1):
            response += f"{i}. **{emp}**: {hours:.0f} hours\n"
        
        if len(top_3) > 0:
            avg_hours = emp_hours.mean()
            top_performance = (top_3.iloc[0] / avg_hours * 100 - 100)
            response += f"\n💡 The top performer logged {top_3.iloc[0]:.0f} hours, which is {top_performance:.0f}% above average."
        
        return response
    
    def _get_project_insights(self, question):
        """Get project-related insights"""
        proj_hours = self.df.groupby('Project')['Aantal'].sum().sort_values(ascending=False)
        proj_revenue = self.df.groupby('Project')['Totaal'].sum().sort_values(ascending=False)
        
        response = "📋 **Project Insights:**\n\n"
        response += "**Top Projects by Hours:**\n"
        for i, (proj, hours) in enumerate(proj_hours.head(3).items(), 1):
            revenue = proj_revenue.get(proj, 0)
            response += f"{i}. **{proj}**: {hours:.0f} hours (€{revenue:,.0f} revenue)\n"
        
        response += f"\n📊 Total of {len(proj_hours)} active projects in your data."
        return response
    
    def _get_time_period_analysis(self, question):
        """Analyze specific time periods"""
        # Get the date range from the data instead of using current date
        data_start = self.df['Datum'].min()
        data_end = self.df['Datum'].max()
        
        if 'last week' in question:
            # Get last 7 days from the data
            start_date = data_end - timedelta(days=7)
            period_data = self.df[self.df['Datum'] >= start_date]
            period_name = "last week of data"
        elif 'last month' in question:
            # Get last 30 days from the data
            start_date = data_end - timedelta(days=30)
            period_data = self.df[self.df['Datum'] >= start_date]
            period_name = "last 30 days of data"
        else:
            # Default to last month
            start_date = data_end - timedelta(days=30)
            period_data = self.df[self.df['Datum'] >= start_date]
            period_name = "recent period"
        
        if len(period_data) == 0:
            return f"❓ No data found for {period_name}."
        
        total_hours = period_data['Aantal'].sum()
        total_revenue = period_data['Totaal'].sum()
        active_employees = period_data['Medewerker'].nunique()
        
        response = f"📅 **Analysis for {period_name}:**\n\n"
        response += f"⏰ **Total Hours**: {total_hours:.0f}\n"
        response += f"💰 **Revenue**: €{total_revenue:,.0f}\n"
        response += f"👥 **Active Employees**: {active_employees}\n"
        
        # Top performer for the period
        if len(period_data) > 0:
            emp_hours = period_data.groupby('Medewerker')['Aantal'].sum()
            if len(emp_hours) > 0:
                top_emp = emp_hours.idxmax()
                top_hours = emp_hours.max()
                response += f"🏆 **Top Performer**: {top_emp} ({top_hours:.0f} hours)"
        
        return response
    
    def _check_compliance_issues(self):
        """Check for compliance issues"""
        # Use the last week of available data instead of current date
        data_end = self.df['Datum'].max()
        last_week_start = data_end - timedelta(days=7)
        recent_data = self.df[self.df['Datum'] >= last_week_start]
        
        if len(recent_data) == 0:
            return "ℹ️ Unable to check recent compliance - insufficient recent data."
        
        # Calculate weekly hours per employee
        weekly_hours = recent_data.groupby('Medewerker')['Aantal'].sum()
        expected_hours = 35  # Assuming 35-hour work week
        
        incomplete = weekly_hours[weekly_hours < expected_hours]
        
        response = "⚠️ **Compliance Check (Last Week of Data):**\n\n"
        
        if len(incomplete) > 0:
            response += f"**{len(incomplete)} employees** have potentially incomplete timesheets:\n\n"
            for emp, hours in incomplete.head(5).items():
                missing = expected_hours - hours
                response += f"• **{emp}**: {hours:.0f} hours (missing {missing:.0f})\n"
            
            if len(incomplete) > 5:
                response += f"• ... and {len(incomplete)-5} more\n"
        else:
            response += "✅ All employees appear to have complete timesheets!"
        
        response += f"\n📊 Based on {expected_hours}-hour work week assumption."
        return response
    
    def _get_totals(self, question):
        """Get total summaries"""
        total_hours = self.df['Aantal'].sum()
        total_revenue = self.df['Totaal'].sum()
        total_employees = self.df['Medewerker'].nunique()
        total_projects = self.df['Project'].nunique()
        date_range = f"{self.df['Datum'].min().strftime('%Y-%m-%d')} to {self.df['Datum'].max().strftime('%Y-%m-%d')}"
        
        response = "📊 **Complete Summary:**\n\n"
        response += f"⏰ **Total Hours**: {total_hours:,.0f}\n"
        response += f"💰 **Total Revenue**: €{total_revenue:,.0f}\n"
        response += f"👥 **Employees**: {total_employees}\n"
        response += f"📋 **Projects**: {total_projects}\n"
        response += f"📅 **Period**: {date_range}\n"
        response += f"💵 **Average Rate**: €{self.df['Uurtarief'].mean():.0f}/hour"
        
        return response
    
    def _get_revenue_insights(self, question):
        """Get revenue-related insights"""
        revenue_by_category = self.df.groupby('Categorie')['Totaal'].sum().sort_values(ascending=False)
        revenue_by_client = self.df.groupby('Relatie')['Totaal'].sum().sort_values(ascending=False)
        
        response = "💰 **Revenue Insights:**\n\n"
        response += "**By Category:**\n"
        total_revenue = revenue_by_category.sum()
        for cat, rev in revenue_by_category.head(3).items():
            pct = (rev / total_revenue * 100) if total_revenue > 0 else 0
            response += f"• **{cat}**: €{rev:,.0f} ({pct:.0f}%)\n"
        
        response += "\n**Top Clients:**\n"
        for client, rev in revenue_by_client.head(3).items():
            response += f"• **{client}**: €{rev:,.0f}\n"
        
        avg_rate = self.df['Uurtarief'].mean()
        response += f"\n📈 **Average Rate**: €{avg_rate:.0f}/hour"
        
        return response
    
    def _analyze_trends(self):
        """Analyze trends in the data"""
        monthly_hours = self.df.groupby('Month_Name')['Aantal'].sum()
        
        if len(monthly_hours) < 2:
            return "📈 Need more time periods to analyze trends."
        
        peak_month = monthly_hours.idxmax()
        peak_hours = monthly_hours.max()
        low_month = monthly_hours.idxmin()
        low_hours = monthly_hours.min()
        
        response = "📈 **Trend Analysis:**\n\n"
        response += f"🔝 **Peak Month**: {peak_month} ({peak_hours:.0f} hours)\n"
        response += f"📉 **Lowest Month**: {low_month} ({low_hours:.0f} hours)\n"
        
        avg_hours = monthly_hours.mean()
        variance = ((peak_hours - low_hours) / avg_hours * 100) if avg_hours > 0 else 0
        response += f"📊 **Variation**: {variance:.0f}% difference between peak and low\n"
        
        # Simple trend detection
        if len(monthly_hours) >= 6:
            recent_avg = monthly_hours.tail(3).mean()
            earlier_avg = monthly_hours.head(3).mean()
            
            if recent_avg > earlier_avg * 1.1:
                response += "📈 **Trend**: Increasing activity in recent months"
            elif recent_avg < earlier_avg * 0.9:
                response += "📉 **Trend**: Decreasing activity in recent months"
            else:
                response += "➡️ **Trend**: Relatively stable activity levels"
        
        return response
    
    def _get_client_insights(self):
        """Get client-related insights"""
        client_hours = self.df.groupby('Relatie')['Aantal'].sum().sort_values(ascending=False)
        client_revenue = self.df.groupby('Relatie')['Totaal'].sum().sort_values(ascending=False)
        
        response = "🏢 **Client Insights:**\n\n"
        response += "**Top Clients by Hours:**\n"
        for i, (client, hours) in enumerate(client_hours.head(3).items(), 1):
            revenue = client_revenue.get(client, 0)
            response += f"{i}. **{client}**: {hours:.0f} hours (€{revenue:,.0f})\n"
        
        response += f"\n📊 Working with {len(client_hours)} total clients"
        return response
    
    def _compare_periods(self):
        """Compare different time periods"""
        # Compare first half vs second half of data
        data_sorted = self.df.sort_values('Datum')
        mid_point = len(data_sorted) // 2
        
        if mid_point == 0:
            return "📊 Need more data to compare periods."
        
        first_half = data_sorted.iloc[:mid_point]
        second_half = data_sorted.iloc[mid_point:]
        
        first_hours = first_half['Aantal'].sum()
        second_hours = second_half['Aantal'].sum()
        
        response = "⚖️ **Period Comparison:**\n\n"
        response += f"**First Half**: {first_hours:.0f} hours\n"
        response += f"**Second Half**: {second_hours:.0f} hours\n"
        
        if first_hours > 0:
            change = ((second_hours - first_hours) / first_hours * 100)
            
            if change > 5:
                response += f"📈 **Change**: +{change:.0f}% increase in activity"
            elif change < -5:
                response += f"📉 **Change**: {change:.0f}% decrease in activity"
            else:
                response += f"➡️ **Change**: Relatively stable ({change:+.0f}%)"
        
        return response
    
    def _get_help_response(self):
        """Provide help and suggestions"""
        return """🤖 **ACMI Analytics Assistant Help**

I can help you analyze your timesheet data! Try asking questions like:

**👥 People & Performance:**
• "Who worked the most hours?"
• "Show me top employees"
• "Who are the best performers?"

**📋 Projects & Work:**
• "Which projects have the most hours?"
• "Show me project insights"
• "What are our biggest projects?"

**📅 Time Periods:**
• "What happened last week?"
• "Show me last month's data"
• "Analyze last quarter"

**⚠️ Compliance & Issues:**
• "Check compliance issues"
• "Who has incomplete timesheets?"
• "Show missing entries"

**💰 Revenue & Business:**
• "What's our total revenue?"
• "Show me revenue by client"
• "Revenue trends"

**📈 Trends & Patterns:**
• "Analyze trends"
• "Compare time periods"
• "What are the patterns?"

Just ask in natural language - I'll do my best to help! 🚀"""

# Load and cache data
@st.cache_data
def load_data(uploaded_file=None):
    """Load and preprocess the timesheet data"""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        # Try to read from the documents folder
        try:
            df = pd.read_csv('Detailweergaveuren 5.csv')
        except FileNotFoundError:
            try:
                df = pd.read_csv('Detailweergaveuren (5).csv')
            except FileNotFoundError:
                return None
    
    # Convert date column to datetime - FIXED: Handle DD-MM-YYYY format correctly
    try:
        df['Datum'] = pd.to_datetime(df['Datum'], format='%d-%m-%Y', errors='coerce')
    except:
        # Fallback for different date formats
        df['Datum'] = pd.to_datetime(df['Datum'], infer_datetime_format=True, errors='coerce')
    
    # Remove rows with invalid dates
    df = df.dropna(subset=['Datum'])
    
    # Extract additional date features
    df['Year'] = df['Datum'].dt.year
    df['Month'] = df['Datum'].dt.month
    df['Month_Name'] = df['Datum'].dt.strftime('%B')
    df['Quarter'] = df['Datum'].dt.quarter
    df['Day_of_Week'] = df['Datum'].dt.day_name()
    df['Week'] = df['Datum'].dt.isocalendar().week
    df['Year_Week'] = df['Datum'].dt.strftime('%Y-W%U')
    
    # Clean numeric columns - FIXED: Handle null values properly
    df['Aantal'] = pd.to_numeric(df['Aantal'], errors='coerce').fillna(0)
    df['Uurtarief'] = pd.to_numeric(df['Uurtarief'], errors='coerce').fillna(0)
    df['Totaal'] = pd.to_numeric(df['Totaal'], errors='coerce').fillna(0)
    
    # Fill missing values
    df = df.fillna({
        'Projectleider': 'Unassigned', 
        'Projectnummer': 'N/A',
        'Relatie': 'Unknown Client',
        'Project': 'Unknown Project',
        'Categorie': 'Other'
    })
    
    # Add working day flags
    df['Is_Weekend'] = df['Day_of_Week'].isin(['Saturday', 'Sunday'])
    df['Is_Leave'] = df['Categorie'].str.contains('Leave|Absence|Verlof', case=False, na=False)
    
    return df

# Helper functions for date calculations - FIXED: Use data dates instead of current date
def get_date_range_from_data(df, days_back):
    """Get date range based on the data's end date"""
    data_end = df['Datum'].max()
    start_date = data_end - timedelta(days=days_back)
    return start_date.date(), data_end.date()

def get_last_week_dates(df):
    return get_date_range_from_data(df, 7)

def get_last_month_dates(df):
    return get_date_range_from_data(df, 30)

def get_last_quarter_dates(df):
    return get_date_range_from_data(df, 90)

def get_last_year_dates(df):
    return get_date_range_from_data(df, 365)

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

records_count = len(df)
st.markdown(f"""
<div class="alert-box alert-success">
    <strong>✅ Data Successfully Loaded</strong><br>
    {records_count:,} records processed and ready for analysis
</div>
""", unsafe_allow_html=True)

# FIXED: Add data quality check
if records_count == 0:
    st.error("No valid records found in the uploaded file. Please check your data format.")
    st.stop()

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
    records_count = len(filtered_df)
    hours_sum = filtered_df['Aantal'].sum()
    st.metric("Records", f"{records_count:,}")
    st.metric("Hours", f"{hours_sum:.0f}")
with col2:
    revenue_sum = filtered_df['Totaal'].sum()
    employees_count = len(filtered_df['Medewerker'].unique())
    st.metric("Revenue", f"€{revenue_sum/1000:.0f}K")
    st.metric("Employees", employees_count)

# Main dashboard content
st.markdown("### 📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_hours = filtered_df['Aantal'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: #3b82f6;">⏰ Total Hours</h3>
        <h2 style="margin: 0.5rem 0 0 0; color: #1f2937;">{total_hours:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_revenue = filtered_df['Totaal'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: #10b981;">💰 Total Revenue</h3>
        <h2 style="margin: 0.5rem 0 0 0; color: #1f2937;">€{total_revenue:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_rate = filtered_df['Uurtarief'].mean() if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: #f59e0b;">📊 Avg Rate</h3>
        <h2 style="margin: 0.5rem 0 0 0; color: #1f2937;">€{avg_rate:.0f}/hr</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    active_staff = len(filtered_df['Medewerker'].unique()) if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: #8b5cf6;">👥 Active Staff</h3>
        <h2 style="margin: 0.5rem 0 0 0; color: #1f2937;">{active_staff}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Add secure chatbot interface
def add_secure_chatbot_interface(df):
    """Add secure chatbot interface (no API key required)"""
    
    st.markdown("### 🤖 ACMI Analytics Assistant")
    st.markdown("Ask questions about your timesheet data in natural language - **No API key required, fully secure!**")
    
    # Initialize chatbot
    if 'secure_chatbot' not in st.session_state:
        st.session_state.secure_chatbot = SecureTimesheetChatbot(df)
    
    # Chat history
    if 'secure_chat_history' not in st.session_state:
        st.session_state.secure_chat_history = []
    
    # Chat interface
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_question = st.text_input(
            "💬 Ask me anything about your timesheet data:",
            placeholder="e.g., 'Who worked the most hours?' or 'Check compliance issues'",
            key="secure_chat_input"
        )
    
    with col2:
        ask_clicked = st.button("Ask 🚀", key="secure_ask_button", use_container_width=True)
    
    # Process question
    if ask_clicked and user_question:
        # Get response from chatbot
        with st.spinner("Analyzing your data..."):
            response = st.session_state.secure_chatbot.analyze_query(user_question)
        
        # Add to chat history
        st.session_state.secure_chat_history.append({
            "question": user_question,
            "response": response,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        # Clear input by rerunning
        st.rerun()
    
    # Display most recent response prominently
    if st.session_state.secure_chat_history:
        latest = st.session_state.secure_chat_history[-1]
        st.markdown("#### 💡 Latest Response:")
        formatted_response = latest['response'].replace('\n', '<br>')
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6; margin: 1rem 0;">
            <strong style="color: #1e40af;">You asked:</strong> {latest['question']}<br><br>
            <div style="color: #374151; line-height: 1.6;">
                {formatted_response}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick action buttons
    st.markdown("#### ⚡ Quick Insights")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏆 Top Performers", key="secure_quick_top", use_container_width=True):
            response = st.session_state.secure_chatbot._get_top_employees("top employees")
            st.session_state.secure_chat_history.append({
                "question": "Quick: Show top performers",
                "response": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
    
    with col2:
        if st.button("⚠️ Compliance Check", key="secure_quick_compliance", use_container_width=True):
            response = st.session_state.secure_chatbot._check_compliance_issues()
            st.session_state.secure_chat_history.append({
                "question": "Quick: Check compliance",
                "response": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
    
    with col3:
        if st.button("📈 Trend Analysis", key="secure_quick_trends", use_container_width=True):
            response = st.session_state.secure_chatbot._analyze_trends()
            st.session_state.secure_chat_history.append({
                "question": "Quick: Analyze trends",
                "response": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
    
    with col4:
        if st.button("💰 Revenue Insights", key="secure_quick_revenue", use_container_width=True):
            response = st.session_state.secure_chatbot._get_revenue_insights("revenue insights")
            st.session_state.secure_chat_history.append({
                "question": "Quick: Show revenue insights", 
                "response": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
    
    # Show conversation history
    if len(st.session_state.secure_chat_history) > 1:
        with st.expander("💬 View Conversation History", expanded=False):
            for i, chat in enumerate(reversed(st.session_state.secure_chat_history[:-1])):
                truncated_response = chat['response'][:200] + '...' if len(chat['response']) > 200 else chat['response']
                st.markdown(f"""
                <div style="background-color: #f8fafc; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 3px solid #6b7280;">
                    <small style="color: #6b7280;">#{len(st.session_state.secure_chat_history)-i-1} • {chat['timestamp']}</small><br>
                    <strong>Q:</strong> {chat['question']}<br>
                    <strong>A:</strong> {truncated_response}
                </div>
                """, unsafe_allow_html=True)
    
    # Add privacy notice
    st.markdown("""
    <div style="background-color: #f0fdf4; padding: 1rem; border-radius: 8px; border: 1px solid #bbf7d0; margin-top: 1rem;">
        <small>🔒 <strong>Privacy & Security:</strong> This chatbot analyzes your data locally without sending any information to external APIs. 
        No API keys required, completely secure and private.</small>
    </div>
    """, unsafe_allow_html=True)

# Add the chatbot interface
add_secure_chatbot_interface(filtered_df)

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
    
    # Main overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Hours by category chart
        if len(filtered_df) > 0:
            category_hours = filtered_df.groupby('Categorie')['Aantal'].sum().reset_index()
            category_hours = category_hours.sort_values('Aantal', ascending=False)
            
            if len(category_hours) > 0:
                fig1 = px.pie(category_hours, values='Aantal', names='Categorie', 
                             title="Hours Distribution by Category")
                fig1.update_traces(
                    hovertemplate='<b>%{label}</b><br>Hours: %{value}<br>Percentage: %{percent}<extra></extra>',
                    textinfo='label+percent'
                )
                st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Hours by month chart
        if len(filtered_df) > 0:
            monthly_hours = filtered_df.groupby('Month_Name')['Aantal'].sum().reset_index()
            month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
            monthly_hours['Month_Name'] = pd.Categorical(monthly_hours['Month_Name'], 
                                                       categories=month_order, ordered=True)
            monthly_hours = monthly_hours.sort_values('Month_Name')
            
            if len(monthly_hours) > 0:
                fig2 = px.bar(monthly_hours, x='Month_Name', y='Aantal', 
                             title="Hours by Month",
                             color_discrete_sequence=['#3b82f6'])
                fig2.update_traces(
                    hovertemplate='<b>%{x}</b><br>Hours: %{y}<extra></extra>'
                )
                fig2.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig2, use_container_width=True)

    # Additional overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by category
        if len(filtered_df) > 0:
            category_revenue = filtered_df.groupby('Categorie')['Totaal'].sum().reset_index()
            if len(category_revenue) > 0:
                fig3 = px.pie(category_revenue, values='Totaal', names='Categorie', 
                             title="Revenue Distribution by Category")
                fig3.update_traces(
                    hovertemplate='<b>%{label}</b><br>Revenue: €%{value:,.0f}<br>Percentage: %{percent}<extra></extra>',
                    textinfo='label+percent'
                )
                st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Daily hours trend
        if len(filtered_df) > 0:
            daily_hours = filtered_df.groupby('Datum')['Aantal'].sum().reset_index()
            if len(daily_hours) > 0:
                fig4 = px.line(daily_hours, x='Datum', y='Aantal', 
                              title="Daily Hours Trend")
                fig4.update_traces(
                    hovertemplate='<b>%{x}</b><br>Hours: %{y}<extra></extra>',
                    line=dict(color='#10b981', width=3)
                )
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
    
    if st.session_state.time_period == "last_week" and len(filtered_df) > 0:
        start_date, end_date = get_last_week_dates(filtered_df)
        period_data = filtered_df[(filtered_df['Datum'].dt.date >= start_date) & (filtered_df['Datum'].dt.date <= end_date)]
        period_name = f"Last Week ({start_date} to {end_date})"
    elif st.session_state.time_period == "last_month" and len(filtered_df) > 0:
        start_date, end_date = get_last_month_dates(filtered_df)
        period_data = filtered_df[(filtered_df['Datum'].dt.date >= start_date) & (filtered_df['Datum'].dt.date <= end_date)]
        period_name = f"Last Month ({start_date.strftime('%B %Y')})"
    elif st.session_state.time_period == "last_quarter" and len(filtered_df) > 0:
        start_date, end_date = get_last_quarter_dates(filtered_df)
        period_data = filtered_df[(filtered_df['Datum'].dt.date >= start_date) & (filtered_df['Datum'].dt.date <= end_date)]
        period_name = f"Last Quarter ({start_date} to {end_date})"
    elif st.session_state.time_period == "last_year" and len(filtered_df) > 0:
        start_date, end_date = get_last_year_dates(filtered_df)
        period_data = filtered_df[(filtered_df['Datum'].dt.date >= start_date) & (filtered_df['Datum'].dt.date <= end_date)]
        period_name = f"Last Year ({start_date.year})"
    
    if period_data is not None:
        st.markdown(f"#### 📊 Analysis for {period_name}")
        
        if len(period_data) > 0:
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
        else:
            st.info(f"No data available for {period_name}")
    
    st.markdown("---")
    
    # Overall employee summary
    if len(filtered_df) > 0:
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
            if len(top_employees) > 0:
                fig5 = px.bar(top_employees, x=top_employees.index, y='Total Hours',
                             title="Top 10 Employees by Hours")
                fig5.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            # Employee rate distribution
            if len(filtered_df) > 0:
                fig6 = px.histogram(filtered_df, x='Uurtarief', nbins=20,
                                   title="Employee Rate Distribution")
                st.plotly_chart(fig6, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header">Project Performance Analytics</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
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
            if len(top_projects) > 0:
                fig7 = px.bar(top_projects, x=top_projects.index, y='Total Hours',
                             title="Top 10 Projects by Hours")
                fig7.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig7, use_container_width=True)
        
        with col2:
            # Project revenue vs hours scatter
            if len(project_summary) > 0:
                fig8 = px.scatter(project_summary, x='Total Hours', y='Total Revenue',
                                hover_data=['Employee Count'], 
                                title="Project Revenue vs Hours")
                st.plotly_chart(fig8, use_container_width=True)

with tab4:
    st.markdown('<div class="section-header">Client Portfolio Analytics</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
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
            if len(top_clients) > 0:
                fig9 = px.bar(top_clients, x=top_clients.index, y='Total Revenue',
                             title="Top 10 Clients by Revenue")
                fig9.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig9, use_container_width=True)
        
        with col2:
            # Client hours distribution
            if len(client_summary) >= 8:
                top_8_clients = client_summary.head(8)
                fig10 = px.pie(top_8_clients, values='Total Hours', 
                              names=top_8_clients.index,
                              title="Hours Distribution by Top Clients")
                st.plotly_chart(fig10, use_container_width=True)

with tab5:
    st.markdown('<div class="section-header">Advanced Data Analytics</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
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
    
    if len(filtered_df) > 0:
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
