# amazon_dashboard.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import subprocess
import sys

# Page configuration
st.set_page_config(
    page_title='Amazon India Analytics',
    page_icon='🛍️',
    layout='wide'
)

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Safe database query function
def safe_query(query):
    """Create a NEW connection for EVERY query"""
    try:
        conn = sqlite3.connect('amazon_india_analytics.db', check_same_thread=False)
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

# Load data function
def load_data():
    """Load data from database"""
    try:
        # Load sales data
        sales_data = safe_query("SELECT * FROM transactions LIMIT 50000")
        
        if sales_data.empty:
            st.error("No data found in database!")
            return False
        
        # Load product catalog if exists
        product_catalog = safe_query("SELECT * FROM products")
        
        st.session_state.sales_data = sales_data
        st.session_state.product_catalog = product_catalog if not product_catalog.empty else None
        st.session_state.data_loaded = True
        
        return True
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return False

# EDA Dashboard Launcher
def launch_eda_dashboard():
    """Launch the EDA dashboard"""
    try:
        # Check if EDA file exists
        if os.path.exists('amazon_eda_complete.py'):
            # Use subprocess to run the EDA dashboard
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", "amazon_eda_complete.py"])
            st.success("📊 EDA Dashboard launched in a new window!")
            st.info("Check your browser for the EDA dashboard with all 20 questions.")
        else:
            st.error("EDA dashboard file not found. Please ensure 'amazon_eda_complete.py' is in the project folder.")
    except Exception as e:
        st.error(f"Could not launch EDA dashboard: {e}")

# 30 Dashboards Launcher
def launch_30_dashboards():
    """Launch the 30 dashboards"""
    try:
        # Check if 30 dashboards file exists
        if os.path.exists('amazon_30_dashboards.py'):
            # Use subprocess to run the 30 dashboards
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", "amazon_30_dashboards.py"])
            st.success("📊 30 Dashboards launched in a new window!")
            st.info("Check your browser for the comprehensive 30-dashboard analytics suite.")
        else:
            st.error("30 Dashboards file not found. Please ensure 'amazon_30_dashboards.py' is in the project folder.")
    except Exception as e:
        st.error(f"Could not launch 30 Dashboards: {e}")

# Main Dashboard
def main_dashboard():
    """Main Amazon Analytics Dashboard"""
    st.title('🛍️ Amazon India Analytics Dashboard')
    
    # Sidebar
    st.sidebar.header('📊 Dashboard Navigation')
    
    # Main navigation
    page_option = st.sidebar.radio(
        "Go to:",
        ["Main Dashboard", "EDA Questions Analysis", "30 Comprehensive Dashboards"]
    )
    
    if page_option == "EDA Questions Analysis":
        st.sidebar.info("Launching comprehensive EDA with 20 questions...")
        launch_eda_dashboard()
        return
    
    if page_option == "30 Comprehensive Dashboards":
        st.sidebar.info("Launching comprehensive 30-dashboard analytics suite...")
        launch_30_dashboards()
        return
    
    # Load data button
    if st.sidebar.button('🔄 Load Data') or st.session_state.data_loaded:
        if not st.session_state.data_loaded:
            with st.spinner('Loading data from database...'):
                if load_data():
                    st.sidebar.success('Data loaded successfully!')
        else:
            st.sidebar.info('Data already loaded!')
    
    # Quick stats in sidebar
    if st.session_state.data_loaded:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📈 Quick Stats")
        
        df = st.session_state.sales_data
        total_orders = len(df)
        total_revenue = df['final_amount_inr'].sum()
        unique_customers = df['customer_id'].nunique() if 'customer_id' in df.columns else 0
        
        st.sidebar.markdown(f"""
        - 📊 Orders: {total_orders:,}
        - 💰 Revenue: ₹{total_revenue:,.0f}
        - 👥 Customers: {unique_customers:,}
        """)
    
    # Advanced Analytics Section
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Advanced Analytics")
    
    st.sidebar.markdown("""
    ### 📊 Choose Your Analytics Level:
    
    **🔍 EDA Questions (20 Questions)**
    - Revenue trends & growth
    - Seasonal patterns  
    - Category performance
    - Customer insights
    - Operations analysis
    
    **📈 Comprehensive Dashboards (30 Dashboards)**
    - Executive dashboards
    - Revenue analytics
    - Customer analytics
    - Product & inventory
    - Operations & logistics
    - Advanced analytics
    """)
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("📊 Launch EDA", use_container_width=True):
            launch_eda_dashboard()
    
    with col2:
        if st.button("🚀 30 Dashboards", use_container_width=True, type="primary"):
            launch_30_dashboards()
    
    # Main dashboard content
    if st.session_state.data_loaded and st.session_state.sales_data is not None:
        df = st.session_state.sales_data
        
        # Display key metrics
        st.subheader('📈 Business Overview')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_orders = len(df)
            st.metric('Total Orders', f"{total_orders:,}")
        
        with col2:
            total_revenue = df['final_amount_inr'].sum()
            st.metric('Total Revenue', f"₹{total_revenue:,.2f}")
        
        with col3:
            avg_rating = df['customer_rating'].mean() if 'customer_rating' in df.columns else 0
            st.metric('Average Rating', f"{avg_rating:.1f} ⭐")
        
        with col4:
            unique_customers = df['customer_id'].nunique() if 'customer_id' in df.columns else 0
            st.metric('Unique Customers', f"{unique_customers:,}")

        # Analytics Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "💰 Revenue Analytics", 
            "📊 Sales Performance", 
            "🏪 Category Analysis",
            "📋 Data Explorer"
        ])

        with tab1:
            st.subheader("Revenue Analytics")
            
            # Monthly revenue trend
            if 'order_date' in df.columns:
                df['order_date'] = pd.to_datetime(df['order_date'])
                df['month'] = df['order_date'].dt.to_period('M').astype(str)
                
                monthly_data = df.groupby('month').agg({
                    'final_amount_inr': 'sum',
                    'order_id': 'count'
                }).reset_index()
                
                fig = px.line(monthly_data, x='month', y='final_amount_inr', 
                             title='Monthly Revenue Trend')
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Sales Performance")
            
            if 'category' in df.columns:
                category_sales = df.groupby('category').agg({
                    'final_amount_inr': 'sum',
                    'order_id': 'count'
                }).reset_index()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(category_sales.nlargest(10, 'final_amount_inr'), 
                                x='category', y='final_amount_inr',
                                title='Top 10 Categories by Revenue')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.pie(category_sales.nlargest(8, 'final_amount_inr'), 
                                values='final_amount_inr', names='category',
                                title='Revenue Share - Top 8 Categories')
                    st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.subheader("Category Analysis")
            
            if 'category' in df.columns:
                category_stats = df['category'].value_counts().reset_index()
                category_stats.columns = ['category', 'count']
                
                fig = px.pie(category_stats.head(8), values='count', names='category',
                            title='Orders by Category')
                st.plotly_chart(fig, use_container_width=True)

        with tab4:
            st.subheader("Data Explorer")
            
            # Table explorer
            table_option = st.selectbox(
                'Select Table to Explore:',
                ['transactions', 'products', 'customers', 'time_dimension']
            )
            
            if table_option:
                sample_data = safe_query(f"SELECT * FROM {table_option} LIMIT 100")
                st.write(f"**Sample Data from {table_option}:**")
                st.dataframe(sample_data)
                
                # Table statistics
                st.write("**Table Statistics:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Rows displayed: {len(sample_data)}")
                    st.write(f"Total columns: {len(sample_data.columns)}")
                with col2:
                    st.write(f"Memory usage: {sample_data.memory_usage(deep=True).sum() / 1024:.1f} KB")

    else:
        # Welcome page when no data is loaded
        st.info("👆 Click 'Load Data' in the sidebar to start analyzing!")
        
        st.markdown("""
        ### 🎯 Amazon India Analytics Platform
        
        This platform provides comprehensive analytics for Amazon India data from 2015-2025.
        
        **📊 Available Features:**
        - **Main Dashboard**: Business overview and key metrics
        - **Revenue Analytics**: Trends and performance analysis
        - **Sales Performance**: Category and product insights
        - **Data Explorer**: Raw data access and exploration
        
        **🔍 Advanced Analytics Options:**
        
        **📊 EDA Questions Analysis (20 Questions)**
        Comprehensive exploratory data analysis including:
        - Customer segmentation (RFM)
        - Geographic analysis
        - Festival impact studies
        - Pricing strategies
        - Delivery performance
        
        **🚀 30 Comprehensive Dashboards**
        Complete business intelligence suite with:
        - Executive dashboards (Q1-Q5)
        - Revenue analytics (Q6-Q10)  
        - Customer analytics (Q11-Q15)
        - Product & inventory (Q16-Q20)
        - Operations & logistics (Q21-Q25)
        - Advanced analytics (Q26-Q30)
        
        **📈 Data Scope:**
        - 1,023,248 transactions
        - 345,730 unique customers  
        - 2,004 products
        - ₹69.78 Billion total revenue
        - 2015-2025 time period
        """)
        
        # Quick setup guide
        with st.expander("🚀 Quick Setup Guide"):
            st.markdown("""
            1. **Ensure database exists**: Run `data_cleaning_pipeline.py` first
            2. **Load data**: Click 'Load Data' in sidebar
            3. **Explore analytics**: Use the tabs above
            4. **Advanced EDA**: Click 'Launch EDA Dashboard' for 20 comprehensive questions
            5. **Full Analytics**: Click '30 Dashboards' for complete business intelligence
            
            **File Requirements:**
            - `amazon_india_analytics.db` (database file)
            - `amazon_eda_complete.py` (for EDA dashboard)
            - `amazon_30_dashboards.py` (for 30 dashboards)
            """)

    # Footer
    st.markdown("---")
    st.markdown("### 🛍️ Amazon India Analytics Dashboard")
    st.markdown("Complete Business Intelligence Platform | Data: 2015-2025")

# Run the appropriate dashboard based on navigation
if st.session_state.current_page == "main":
    main_dashboard()
else:
    # If somehow we're not on main page, show main dashboard
    main_dashboard()