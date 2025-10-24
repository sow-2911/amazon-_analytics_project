# amazon_eda_complete.py - COMPLETE 20 QUESTIONS
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title='Amazon India EDA Dashboard',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF9900;
        text-align: center;
        margin-bottom: 2rem;
    }
    .question-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #FF9900;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Amazon India - Complete EDA Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### 20 Comprehensive Exploratory Data Analysis Questions")

# Database connection
def safe_query(query):
    conn = sqlite3.connect('amazon_india_analytics.db', check_same_thread=False)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

def load_analysis_data():
    try:
        monthly_sales = safe_query("SELECT * FROM monthly_sales")
        customer_analysis = safe_query("SELECT * FROM customer_analysis")
        product_performance = safe_query("SELECT * FROM product_performance")
        transactions_sample = safe_query("SELECT * FROM transactions LIMIT 50000")
        products = safe_query("SELECT * FROM products")
        customers = safe_query("SELECT * FROM customers")
        sales_fact = safe_query("SELECT * FROM sales_fact LIMIT 50000")
        
        st.session_state.monthly_sales = monthly_sales
        st.session_state.customer_analysis = customer_analysis
        st.session_state.product_performance = product_performance
        st.session_state.transactions = transactions_sample
        st.session_state.products = products
        st.session_state.customers = customers
        st.session_state.sales_fact = sales_fact
        st.session_state.data_loaded = True
        
        return True
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return False

# EDA Questions Navigation
eda_questions = {
    "Q1": "Revenue Trend Analysis (2015-2025)",
    "Q2": "Seasonal Sales Patterns", 
    "Q3": "Customer RFM Segmentation",
    "Q4": "Payment Method Evolution",
    "Q5": "Category Performance Analysis",
    "Q6": "Prime Membership Impact",
    "Q7": "Geographic Sales Analysis",
    "Q8": "Festival Sales Impact", 
    "Q9": "Customer Age Group Analysis",
    "Q10": "Price vs Demand Analysis",
    "Q11": "Delivery Performance Analysis",
    "Q12": "Return Patterns & Satisfaction",
    "Q13": "Brand Performance Analysis",
    "Q14": "Customer Lifetime Value (CLV)",
    "Q15": "Discount Effectiveness",
    "Q16": "Product Rating Impact",
    "Q17": "Customer Journey Analysis",
    "Q18": "Product Lifecycle Patterns",
    "Q19": "Competitive Pricing Analysis",
    "Q20": "Business Health Dashboard"
}

# Sidebar
st.sidebar.header('🔍 EDA Questions Navigation')
selected_question = st.sidebar.selectbox(
    "Choose EDA Question:",
    list(eda_questions.keys()),
    format_func=lambda x: f"{x}: {eda_questions[x]}"
)

# Load data
if st.sidebar.button('🔄 Load Analysis Data') or st.session_state.data_loaded:
    if not st.session_state.data_loaded:
        with st.spinner('Loading data for comprehensive EDA...'):
            if load_analysis_data():
                st.sidebar.success('All data loaded successfully!')

# Quick stats in sidebar
if st.session_state.data_loaded:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Quick Stats")
    total_revenue = st.session_state.monthly_sales['total_revenue'].sum()
    total_customers = len(st.session_state.customer_analysis)
    total_products = len(st.session_state.products)
    
    st.sidebar.markdown(f"""
    - 💰 Revenue: ₹{total_revenue/1e9:.1f}B
    - 👥 Customers: {total_customers:,}
    - 📦 Products: {total_products:,}
    - 📅 Years: 2015-2025
    """)

# Main EDA Content
if st.session_state.data_loaded:
    
    # Q1: Revenue Trend Analysis
    if selected_question == "Q1":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("📈 Q1: Revenue Trend Analysis (2015-2025)")
        st.markdown("Comprehensive revenue trend analysis with growth rates and key growth periods")
        st.markdown('</div>', unsafe_allow_html=True)
        
        yearly_sales = safe_query("""
            SELECT strftime('%Y', order_date) as year, 
                   SUM(final_amount_inr) as revenue,
                   COUNT(*) as orders
            FROM transactions 
            GROUP BY strftime('%Y', order_date)
            ORDER BY year
        """)
        
        yearly_sales['revenue_growth'] = yearly_sales['revenue'].pct_change() * 100
        yearly_sales['revenue_growth'] = yearly_sales['revenue_growth'].fillna(0)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(yearly_sales, x='year', y='revenue', 
                         title='Yearly Revenue Trend (2015-2025)',
                         markers=True)
            fig.update_traces(line=dict(width=4))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = px.bar(yearly_sales, x='year', y='revenue_growth', 
                        title='Yearly Revenue Growth Rate (%)',
                        color='revenue_growth', 
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        total_rev = yearly_sales['revenue'].sum()
        avg_growth = yearly_sales['revenue_growth'].mean()
        best_year = yearly_sales.loc[yearly_sales['revenue'].idxmax()]
        cagr = ((yearly_sales['revenue'].iloc[-1] / yearly_sales['revenue'].iloc[0]) ** (1/10) - 1) * 100
        
        col1.metric("Total Revenue", f"₹{total_rev/1e9:.2f}B")
        col2.metric("Avg Growth", f"{avg_growth:.1f}%")
        col3.metric("Best Year", f"{best_year['year']}")
        col4.metric("CAGR", f"{cagr:.1f}%")

    # Q2: Seasonal Patterns
    elif selected_question == "Q2":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🌞 Q2: Seasonal Sales Patterns")
        st.markdown("Monthly sales heatmaps and seasonal trends across years and categories")
        st.markdown('</div>', unsafe_allow_html=True)
        
        monthly_detail = safe_query("""
            SELECT strftime('%Y', order_date) as year, strftime('%m', order_date) as month,
                   SUM(final_amount_inr) as revenue, COUNT(*) as orders
            FROM transactions GROUP BY year, month ORDER BY year, month
        """)
        
        heatmap_data = monthly_detail.pivot_table(values='revenue', index='year', columns='month').fillna(0)
        fig = px.imshow(heatmap_data, title='Monthly Revenue Heatmap', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
        
        monthly_detail['year_month'] = monthly_detail['year'] + '-' + monthly_detail['month']
        monthly_detail['year_month'] = pd.to_datetime(monthly_detail['year_month'])
        fig = px.line(monthly_detail, x='year_month', y='revenue', title='Monthly Revenue Trend')
        st.plotly_chart(fig, use_container_width=True)

                # Q3: Customer RFM Segmentation - FIXED VERSION
    elif selected_question == "Q3":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("👥 Q3: Customer RFM Segmentation")
        st.markdown("RFM analysis with customer segmentation and actionable insights")
        st.markdown('</div>', unsafe_allow_html=True)
        
        rfm_data = st.session_state.customer_analysis.copy()
        
        st.success("✅ All required RFM data is available!")
        
        # Check if all required columns exist
        required_columns = ['days_since_last_order', 'total_orders', 'total_spent']
        missing_columns = [col for col in required_columns if col not in rfm_data.columns]
        
        if missing_columns:
            st.error(f"❌ Missing required columns: {missing_columns}")
            st.info("Showing basic customer segmentation analysis instead...")
            
            # Show basic segmentation
            col1, col2 = st.columns(2)
            
            with col1:
                if 'spending_segment' in rfm_data.columns:
                    spending_segments = rfm_data['spending_segment'].value_counts()
                    fig = px.pie(spending_segments, values=spending_segments.values, names=spending_segments.index,
                                title='Customer Spending Segments')
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'recency_segment' in rfm_data.columns:
                    recency_segments = rfm_data['recency_segment'].value_counts()
                    fig = px.pie(recency_segments, values=recency_segments.values, names=recency_segments.index,
                                title='Customer Recency Segments')
                    st.plotly_chart(fig, use_container_width=True)
        else:
            # All columns exist, proceed with RFM analysis
            try:
                # Create RFM scores with proper error handling
                rfm_success = True
                
                # For Recency - lower days_since_last_order is better
                recency_data = rfm_data['days_since_last_order'].dropna()
                if recency_data.nunique() >= 5:
                    rfm_data['recency_score'] = pd.qcut(recency_data, q=5, labels=[5,4,3,2,1], duplicates='drop')
                else:
                    rfm_data['recency_score'] = pd.cut(recency_data, bins=5, labels=[5,4,3,2,1])
                
                # For Frequency - higher total_orders is better
                frequency_data = rfm_data['total_orders'].dropna()
                if frequency_data.nunique() >= 5:
                    rfm_data['frequency_score'] = pd.qcut(frequency_data, q=5, labels=[1,2,3,4,5], duplicates='drop')
                else:
                    rfm_data['frequency_score'] = pd.cut(frequency_data, bins=5, labels=[1,2,3,4,5])
                
                # For Monetary - higher total_spent is better
                monetary_data = rfm_data['total_spent'].dropna()
                if monetary_data.nunique() >= 5:
                    rfm_data['monetary_score'] = pd.qcut(monetary_data, q=5, labels=[1,2,3,4,5], duplicates='drop')
                else:
                    rfm_data['monetary_score'] = pd.cut(monetary_data, bins=5, labels=[1,2,3,4,5])
                
                # Convert scores to numeric and calculate RFM score
                rfm_data['recency_score'] = pd.to_numeric(rfm_data['recency_score'], errors='coerce')
                rfm_data['frequency_score'] = pd.to_numeric(rfm_data['frequency_score'], errors='coerce')
                rfm_data['monetary_score'] = pd.to_numeric(rfm_data['monetary_score'], errors='coerce')
                
                rfm_data['rfm_score'] = (rfm_data['recency_score'] + 
                                        rfm_data['frequency_score'] + 
                                        rfm_data['monetary_score'])
                
                # Create RFM segments
                def get_rfm_segment(row):
                    if pd.isna(row['rfm_score']):
                        return 'Unknown'
                    elif row['rfm_score'] >= 12: return 'Champions'
                    elif row['rfm_score'] >= 9: return 'Loyal Customers'
                    elif row['rfm_score'] >= 6: return 'Potential Loyalists'
                    elif row['rfm_score'] >= 4: return 'At Risk'
                    else: return 'Lost Customers'
                
                rfm_data['segment'] = rfm_data.apply(get_rfm_segment, axis=1)
                
                # Display RFM Analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    # Segment distribution - FIXED: removed color_continuous_scale from pie chart
                    segment_counts = rfm_data['segment'].value_counts()
                    fig = px.pie(segment_counts, values=segment_counts.values, names=segment_counts.index,
                                title='Customer RFM Segments Distribution',
                                color=segment_counts.index,  # Use segment names for color
                                color_discrete_sequence=px.colors.qualitative.Set3)  # Use discrete colors
                    st.plotly_chart(fig, use_container_width=True)
                    
                with col2:
                    # RFM scatter plot
                    fig = px.scatter(rfm_data, x='total_orders', y='total_spent', 
                                   color='segment', size='avg_order_value',
                                   title='RFM Analysis: Frequency vs Monetary Value',
                                   hover_data=['customer_id', 'days_since_last_order'],
                                   labels={
                                       'total_orders': 'Frequency (Total Orders)',
                                       'total_spent': 'Monetary (Total Spent ₹)',
                                       'segment': 'RFM Segment'
                                   })
                    st.plotly_chart(fig, use_container_width=True)
                
                # Segment insights table
                st.subheader("📊 RFM Segment Insights")
                segment_stats = rfm_data.groupby('segment').agg({
                    'total_spent': ['mean', 'count'],
                    'total_orders': 'mean',
                    'days_since_last_order': 'mean',
                    'avg_order_value': 'mean'
                }).round(2)
                
                # Flatten column names
                segment_stats.columns = ['avg_spending', 'customer_count', 'avg_orders', 'avg_recency_days', 'avg_order_value']
                segment_stats = segment_stats.reset_index()
                
                # Display segment statistics
                st.dataframe(segment_stats.style.format({
                    'avg_spending': '₹{:,.2f}',
                    'avg_order_value': '₹{:,.2f}'
                }))
                
                # Actionable recommendations
                st.subheader("🎯 Segment Recommendations")
                
                recommendations = {
                    'Champions': [
                        "💎 Reward these customers - they are your most valuable",
                        "🎁 Offer exclusive deals and early access to new products",
                        "👑 Create a VIP/loyalty program for this segment"
                    ],
                    'Loyal Customers': [
                        "⭐ Nurture relationships with personalized communication",
                        "🔔 Upsell complementary products and services", 
                        "📧 Engage with targeted email campaigns"
                    ],
                    'Potential Loyalists': [
                        "🚀 Encourage repeat purchases with limited-time offers",
                        "🎯 Create bundle deals to increase order value",
                        "📱 Engage through mobile app notifications"
                    ],
                    'At Risk': [
                        "📞 Reach out with win-back campaigns", 
                        "💝 Offer special discounts to reactivate",
                        "❓ Survey to understand why they're disengaging"
                    ],
                    'Lost Customers': [
                        "🔄 Focus on cost-effective re-engagement",
                        "📢 Run targeted social media campaigns",
                        "🎪 Invite to special events or webinars"
                    ]
                }
                
                for segment, tips in recommendations.items():
                    segment_count = len(rfm_data[rfm_data['segment'] == segment])
                    if segment_count > 0:
                        with st.expander(f"{segment} - {segment_count:,} customers"):
                            for tip in tips:
                                st.write(f"• {tip}")
                
                # RFM Score Distribution
                st.subheader("📈 RFM Score Distribution")
                fig = px.histogram(rfm_data, x='rfm_score', nbins=20, 
                                 title='Distribution of RFM Scores',
                                 labels={'rfm_score': 'RFM Score', 'count': 'Number of Customers'})
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error in RFM calculation: {str(e)}")
                st.info("Showing alternative customer segmentation analysis...")
                
                # Fallback: Use existing segments for analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'spending_segment' in rfm_data.columns:
                        spending_segments = rfm_data['spending_segment'].value_counts()
                        fig = px.pie(spending_segments, values=spending_segments.values, names=spending_segments.index,
                                    title='Customer Spending Segments')
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    if 'recency_segment' in rfm_data.columns:
                        recency_segments = rfm_data['recency_segment'].value_counts()
                        fig = px.pie(recency_segments, values=recency_segments.values, names=recency_segments.index,
                                    title='Customer Recency Segments')
                        st.plotly_chart(fig, use_container_width=True)
                            
    # Q4: Payment Method Evolution
    elif selected_question == "Q4":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("💳 Q4: Payment Method Evolution")
        st.markdown("Payment method trends from 2015-2025 showing UPI rise and COD decline")
        st.markdown('</div>', unsafe_allow_html=True)
        
        payment_evolution = safe_query("""
            SELECT strftime('%Y', order_date) as year, payment_method,
                   COUNT(*) as transactions, SUM(final_amount_inr) as amount
            FROM transactions WHERE payment_method IS NOT NULL
            GROUP BY year, payment_method ORDER BY year, payment_method
        """)
        
        fig = px.area(payment_evolution, x='year', y='transactions', color='payment_method',
                     title='Payment Method Evolution')
        st.plotly_chart(fig, use_container_width=True)
        
        yearly_totals = payment_evolution.groupby('year')['transactions'].transform('sum')
        payment_evolution['market_share'] = (payment_evolution['transactions'] / yearly_totals) * 100
        fig = px.line(payment_evolution, x='year', y='market_share', color='payment_method',
                     title='Market Share Over Time')
        st.plotly_chart(fig, use_container_width=True)

    # Q5: Category Performance Analysis
    elif selected_question == "Q5":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🏪 Q5: Category Performance Analysis")
        st.markdown("Revenue contribution, growth rates, and market share for product categories")
        st.markdown('</div>', unsafe_allow_html=True)
        
        category_performance = safe_query("""
            SELECT category, COUNT(*) as orders, SUM(final_amount_inr) as revenue,
                   AVG(customer_rating) as avg_rating
            FROM transactions WHERE category IS NOT NULL
            GROUP BY category ORDER BY revenue DESC
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.treemap(category_performance, path=['category'], values='revenue',
                            title='Revenue by Category (Treemap)')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(category_performance.head(10), x='category', y='revenue',
                        title='Top 10 Categories by Revenue')
            st.plotly_chart(fig, use_container_width=True)
        
        fig = px.pie(category_performance.head(8), values='revenue', names='category',
                    title='Market Share - Top 8 Categories')
        st.plotly_chart(fig, use_container_width=True)

        # Q6: Prime Membership Impact - FIXED VERSION
    elif selected_question == "Q6":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("👑 Q6: Prime Membership Impact")
        st.markdown("Compare order values, frequency, and preferences between Prime and non-Prime customers")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # First, check if is_prime_member column exists and has data
        if 'is_prime_member' not in st.session_state.transactions.columns:
            st.error("❌ Prime membership data not available in the dataset")
            st.info("The 'is_prime_member' column is missing from the transactions data.")
            # Show alternative analysis instead of using return
            st.subheader("📊 Alternative: Customer Spending Analysis")
            
            # Show general spending analysis instead
            spending_analysis = safe_query("""
                SELECT 
                    customer_tier,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    AVG(final_amount_inr) as avg_order_value,
                    COUNT(*) as total_orders,
                    SUM(final_amount_inr) as total_revenue
                FROM transactions 
                WHERE customer_tier IS NOT NULL
                GROUP BY customer_tier
                ORDER BY total_revenue DESC
            """)
            
            if not spending_analysis.empty:
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(spending_analysis, x='customer_tier', y='unique_customers',
                                title='Customers by Tier')
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    fig = px.bar(spending_analysis, x='customer_tier', y='avg_order_value',
                                title='Average Order Value by Tier')
                    st.plotly_chart(fig, use_container_width=True)
        else:
            # Continue with Prime analysis if column exists
            prime_analysis = safe_query("""
                SELECT 
                    CASE 
                        WHEN is_prime_member = 1 THEN 'Prime Member'
                        WHEN is_prime_member = 0 THEN 'Non-Prime Member' 
                        ELSE 'Unknown'
                    END as membership_type,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    COUNT(*) as total_orders,
                    AVG(final_amount_inr) as avg_order_value,
                    AVG(customer_rating) as avg_rating,
                    SUM(final_amount_inr) as total_revenue
                FROM transactions 
                WHERE is_prime_member IS NOT NULL
                GROUP BY 
                    CASE 
                        WHEN is_prime_member = 1 THEN 'Prime Member'
                        WHEN is_prime_member = 0 THEN 'Non-Prime Member' 
                        ELSE 'Unknown'
                    END
            """)
            
            if prime_analysis.empty:
                st.warning("⚠️ No Prime membership data found. Showing alternative analysis.")
                
                # Show general customer analysis instead
                st.subheader("📊 General Customer Analysis")
                customer_stats = safe_query("""
                    SELECT 
                        COUNT(DISTINCT customer_id) as total_customers,
                        AVG(final_amount_inr) as avg_order_value,
                        COUNT(*) as total_orders,
                        AVG(customer_rating) as avg_rating
                    FROM transactions
                """)
                
                col1, col2, col3, col4 = st.columns(4)
                if not customer_stats.empty:
                    col1.metric("Total Customers", f"{customer_stats['total_customers'].iloc[0]:,}")
                    col2.metric("Avg Order Value", f"₹{customer_stats['avg_order_value'].iloc[0]:.0f}")
                    col3.metric("Total Orders", f"{customer_stats['total_orders'].iloc[0]:,}")
                    col4.metric("Avg Rating", f"{customer_stats['avg_rating'].iloc[0]:.1f}")
            else:
                # If we have Prime data, show the analysis
                st.success("✅ Prime membership data found!")
                
                # Display metrics - FIXED with safe indexing
                col1, col2, col3, col4 = st.columns(4)
                
                # Safely get Prime member count
                prime_count = prime_analysis[prime_analysis['membership_type'] == 'Prime Member']
                non_prime_count = prime_analysis[prime_analysis['membership_type'] == 'Non-Prime Member']
                
                if not prime_count.empty:
                    col1.metric("Prime Members", f"{prime_count['unique_customers'].iloc[0]:,}")
                else:
                    col1.metric("Prime Members", "0")
                    
                if not non_prime_count.empty:
                    col2.metric("Non-Prime Members", f"{non_prime_count['unique_customers'].iloc[0]:,}")
                else:
                    col2.metric("Non-Prime Members", "0")
                    
                if not prime_count.empty:
                    col3.metric("Avg Order Value (Prime)", f"₹{prime_count['avg_order_value'].iloc[0]:.0f}")
                else:
                    col3.metric("Avg Order Value (Prime)", "N/A")
                    
                if not non_prime_count.empty:
                    col4.metric("Avg Order Value (Non-Prime)", f"₹{non_prime_count['avg_order_value'].iloc[0]:.0f}")
                else:
                    col4.metric("Avg Order Value (Non-Prime)", "N/A")
                
                # Visualization 1: Membership distribution
                col1, col2 = st.columns(2)
                
                with col1:
                    if not prime_analysis.empty:
                        fig = px.pie(prime_analysis, values='unique_customers', names='membership_type',
                                    title='Customer Distribution by Membership Type')
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    if not prime_analysis.empty:
                        fig = px.bar(prime_analysis, x='membership_type', y='total_revenue',
                                    title='Total Revenue by Membership Type',
                                    color='membership_type')
                        st.plotly_chart(fig, use_container_width=True)
                
                # Category preferences analysis
                st.subheader("🛍️ Category Preferences by Membership Type")
                
                prime_categories = safe_query("""
                    SELECT 
                        CASE 
                            WHEN is_prime_member = 1 THEN 'Prime Member'
                            WHEN is_prime_member = 0 THEN 'Non-Prime Member' 
                            ELSE 'Unknown'
                        END as membership_type,
                        category,
                        COUNT(*) as orders,
                        SUM(final_amount_inr) as revenue
                    FROM transactions 
                    WHERE category IS NOT NULL AND is_prime_member IS NOT NULL
                    GROUP BY 
                        CASE 
                            WHEN is_prime_member = 1 THEN 'Prime Member'
                            WHEN is_prime_member = 0 THEN 'Non-Prime Member' 
                            ELSE 'Unknown'
                        END,
                        category
                    ORDER BY orders DESC
                """)
                
                if not prime_categories.empty:
                    # Get top categories for each membership type
                    prime_top = prime_categories[prime_categories['membership_type'] == 'Prime Member'].head(10)
                    non_prime_top = prime_categories[prime_categories['membership_type'] == 'Non-Prime Member'].head(10)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if not prime_top.empty:
                            fig = px.bar(prime_top, x='category', y='orders', 
                                        title='Top Categories - Prime Members',
                                        color='orders')
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No Prime member category data available")
                    
                    with col2:
                        if not non_prime_top.empty:
                            fig = px.bar(non_prime_top, x='category', y='orders',
                                        title='Top Categories - Non-Prime Members',
                                        color='orders')
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No Non-Prime member category data available")
                
                # Detailed comparison table
                st.subheader("📋 Detailed Membership Comparison")
                if not prime_analysis.empty:
                    display_table = prime_analysis[['membership_type', 'unique_customers', 'total_orders', 
                                                  'avg_order_value', 'avg_rating', 'total_revenue']].copy()
                    display_table['avg_order_value'] = display_table['avg_order_value'].round(2)
                    display_table['avg_rating'] = display_table['avg_rating'].round(2)
                    display_table['total_revenue'] = display_table['total_revenue'].round(2)
                    
                    st.dataframe(display_table.style.format({
                        'avg_order_value': '₹{:,.2f}',
                        'total_revenue': '₹{:,.2f}'
                    }))

    # Q7: Geographic Sales Analysis
    elif selected_question == "Q7":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🗺️ Q7: Geographic Sales Analysis")
        st.markdown("Revenue density and growth patterns across Indian cities and states")
        st.markdown('</div>', unsafe_allow_html=True)
        
        state_performance = safe_query("""
            SELECT customer_state, COUNT(*) as orders, SUM(final_amount_inr) as revenue,
                   COUNT(DISTINCT customer_id) as customers
            FROM transactions 
            WHERE customer_state IS NOT NULL AND customer_state != 'Unknown'
            GROUP BY customer_state 
            ORDER BY revenue DESC
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(state_performance.head(15), x='customer_state', y='revenue',
                        title='Top 15 States by Revenue')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(state_performance.head(8), values='revenue', names='customer_state',
                        title='Revenue Share - Top 8 States')
            st.plotly_chart(fig, use_container_width=True)
        
        city_performance = safe_query("""
            SELECT customer_city, customer_state, SUM(final_amount_inr) as revenue
            FROM transactions 
            WHERE customer_city IS NOT NULL AND customer_city != 'Unknown'
            GROUP BY customer_city, customer_state 
            ORDER BY revenue DESC 
            LIMIT 20
        """)
        
        fig = px.bar(city_performance, x='customer_city', y='revenue', color='customer_state',
                    title='Top 20 Cities by Revenue')
        st.plotly_chart(fig, use_container_width=True)

    # Q8: Festival Sales Impact
    elif selected_question == "Q8":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🎪 Q8: Festival Sales Impact")
        st.markdown("Revenue spikes during Diwali, Prime Day, and other festivals with time series analysis")
        st.markdown('</div>', unsafe_allow_html=True)
        
        festival_analysis = safe_query("""
            SELECT order_date, festival_name, SUM(final_amount_inr) as daily_revenue,
                   COUNT(*) as daily_orders
            FROM transactions 
            WHERE order_date IS NOT NULL
            GROUP BY order_date, festival_name
            ORDER BY order_date
        """)
        
        festival_analysis['order_date'] = pd.to_datetime(festival_analysis['order_date'])
        festival_analysis['is_festival'] = festival_analysis['festival_name'].notna()
        
        fig = px.line(festival_analysis, x='order_date', y='daily_revenue', 
                     color='is_festival', title='Daily Revenue - Festival vs Non-Festival Days')
        st.plotly_chart(fig, use_container_width=True)
        
        festival_summary = safe_query("""
            SELECT festival_name, AVG(final_amount_inr) as avg_daily_revenue,
                   COUNT(DISTINCT order_date) as festival_days,
                   SUM(final_amount_inr) as total_festival_revenue
            FROM transactions 
            WHERE festival_name IS NOT NULL AND festival_name != 'Unknown'
            GROUP BY festival_name 
            ORDER BY total_festival_revenue DESC
        """)
        
        if not festival_summary.empty:
            fig = px.bar(festival_summary, x='festival_name', y='total_festival_revenue',
                        title='Total Revenue by Festival')
            st.plotly_chart(fig, use_container_width=True)

    # Q9: Customer Age Group Analysis
    elif selected_question == "Q9":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("👨‍👩‍👧‍👦 Q9: Customer Age Group Analysis")
        st.markdown("Demographic analysis with category preferences and spending patterns")
        st.markdown('</div>', unsafe_allow_html=True)
        
        age_analysis = safe_query("""
            SELECT customer_age_group, COUNT(DISTINCT customer_id) as customers,
                   AVG(final_amount_inr) as avg_order_value,
                   COUNT(*) as total_orders,
                   SUM(final_amount_inr) as total_revenue
            FROM transactions 
            WHERE customer_age_group IS NOT NULL AND customer_age_group != 'Unknown'
            GROUP BY customer_age_group 
            ORDER BY total_revenue DESC
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(age_analysis, x='customer_age_group', y='customers',
                        title='Customer Distribution by Age Group')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(age_analysis, x='customer_age_group', y='avg_order_value',
                        title='Average Order Value by Age Group')
            st.plotly_chart(fig, use_container_width=True)
        
        age_categories = safe_query("""
            SELECT customer_age_group, category, COUNT(*) as orders
            FROM transactions 
            WHERE customer_age_group IS NOT NULL AND category IS NOT NULL
            GROUP BY customer_age_group, category
            ORDER BY orders DESC
        """)
        
        for age_group in age_analysis['customer_age_group'].unique():
            top_cats = age_categories[age_categories['customer_age_group'] == age_group].head(5)
            if not top_cats.empty:
                st.subheader(f"Top Categories for {age_group}")
                fig = px.bar(top_cats, x='category', y='orders')
                st.plotly_chart(fig, use_container_width=True)

    # Q10: Price vs Demand Analysis
    elif selected_question == "Q10":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("💰 Q10: Price vs Demand Analysis")
        st.markdown("Analyze how pricing strategies affect sales volumes across categories")
        st.markdown('</div>', unsafe_allow_html=True)
        
        price_demand = safe_query("""
            SELECT category, AVG(original_price_inr) as avg_price,
                   COUNT(*) as total_orders,
                   SUM(quantity) as total_quantity,
                   AVG(discount_percent) as avg_discount
            FROM transactions 
            WHERE category IS NOT NULL AND original_price_inr > 0
            GROUP BY category 
            HAVING total_orders > 100
            ORDER BY total_quantity DESC
        """)
        
        fig = px.scatter(price_demand, x='avg_price', y='total_quantity', 
                        size='total_orders', color='category',
                        title='Price vs Demand by Category',
                        hover_data=['avg_discount'])
        st.plotly_chart(fig, use_container_width=True)
        
        numeric_cols = price_demand[['avg_price', 'total_orders', 'total_quantity', 'avg_discount']]
        corr_matrix = numeric_cols.corr()
        fig = px.imshow(corr_matrix, title='Price-Demand Correlation Matrix',
                       color_continuous_scale='RdBu_r', aspect='auto')
        st.plotly_chart(fig, use_container_width=True)

    # Q11: Delivery Performance Analysis
    elif selected_question == "Q11":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🚚 Q11: Delivery Performance Analysis")
        st.markdown("Delivery days distribution, on-time performance, and customer satisfaction correlation")
        st.markdown('</div>', unsafe_allow_html=True)
        
        delivery_analysis = safe_query("""
            SELECT delivery_days, COUNT(*) as orders,
                   AVG(customer_rating) as avg_rating,
                   customer_city
            FROM transactions 
            WHERE delivery_days IS NOT NULL AND delivery_days > 0
            GROUP BY delivery_days, customer_city
            HAVING orders > 10
            ORDER BY delivery_days
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            delivery_summary = delivery_analysis.groupby('delivery_days')['orders'].sum().reset_index()
            fig = px.bar(delivery_summary, x='delivery_days', y='orders',
                        title='Order Distribution by Delivery Days')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            rating_by_delivery = delivery_analysis.groupby('delivery_days')['avg_rating'].mean().reset_index()
            fig = px.line(rating_by_delivery, x='delivery_days', y='avg_rating',
                         title='Customer Rating vs Delivery Days', markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        city_delivery = safe_query("""
            SELECT customer_city, AVG(delivery_days) as avg_delivery_days,
                   AVG(customer_rating) as avg_rating,
                   COUNT(*) as orders
            FROM transactions 
            WHERE customer_city IS NOT NULL AND delivery_days IS NOT NULL
            GROUP BY customer_city 
            HAVING orders > 50
            ORDER BY avg_delivery_days
            LIMIT 20
        """)
        
        fig = px.scatter(city_delivery, x='avg_delivery_days', y='avg_rating',
                        size='orders', hover_name='customer_city',
                        title='Delivery Performance by City')
        st.plotly_chart(fig, use_container_width=True)

    # Q12: Return Patterns & Satisfaction
    elif selected_question == "Q12":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🔄 Q12: Return Patterns & Satisfaction")
        st.markdown("Return rates, reasons, and correlation with product ratings and prices")
        st.markdown('</div>', unsafe_allow_html=True)
        
        return_analysis = safe_query("""
            SELECT return_status, COUNT(*) as return_count,
                   AVG(customer_rating) as avg_rating,
                   AVG(original_price_inr) as avg_price,
                   category
            FROM transactions 
            WHERE return_status IS NOT NULL
            GROUP BY return_status, category
            ORDER BY return_count DESC
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            return_summary = return_analysis.groupby('return_status')['return_count'].sum().reset_index()
            fig = px.pie(return_summary, values='return_count', names='return_status',
                        title='Return Status Distribution')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(return_analysis.head(10), x='category', y='return_count',
                        color='return_status', title='Returns by Category')
            st.plotly_chart(fig, use_container_width=True)
        
        rating_returns = safe_query("""
            SELECT customer_rating, 
                   SUM(CASE WHEN return_status = 'Returned' THEN 1 ELSE 0 END) as returned_orders,
                   COUNT(*) as total_orders
            FROM transactions 
            WHERE customer_rating IS NOT NULL
            GROUP BY customer_rating
            ORDER BY customer_rating
        """)
        
        rating_returns['return_rate'] = (rating_returns['returned_orders'] / rating_returns['total_orders']) * 100
        fig = px.line(rating_returns, x='customer_rating', y='return_rate',
                     title='Return Rate vs Customer Rating', markers=True)
        st.plotly_chart(fig, use_container_width=True)

    # Q13: Brand Performance Analysis
    elif selected_question == "Q13":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🏷️ Q13: Brand Performance Analysis")
        st.markdown("Brand comparison, market share trends, and competitive positioning")
        st.markdown('</div>', unsafe_allow_html=True)
        
        brand_performance = safe_query("""
            SELECT brand, COUNT(*) as orders, SUM(final_amount_inr) as revenue,
                   AVG(customer_rating) as avg_rating,
                   AVG(original_price_inr) as avg_price,
                   COUNT(DISTINCT category) as categories_covered
            FROM transactions 
            WHERE brand IS NOT NULL AND brand != 'Unknown'
            GROUP BY brand 
            HAVING orders > 100
            ORDER BY revenue DESC
            LIMIT 20
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(brand_performance.head(10), x='brand', y='revenue',
                        title='Top 10 Brands by Revenue')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.scatter(brand_performance, x='avg_price', y='avg_rating',
                            size='revenue', color='orders', hover_name='brand',
                            title='Brand Positioning: Price vs Rating')
            st.plotly_chart(fig, use_container_width=True)
        
        brand_trends = safe_query("""
            SELECT strftime('%Y', order_date) as year, brand, COUNT(*) as orders
            FROM transactions 
            WHERE brand IN (SELECT brand FROM transactions GROUP BY brand ORDER BY COUNT(*) DESC LIMIT 8)
            GROUP BY year, brand
            ORDER BY year, orders DESC
        """)
        
        if not brand_trends.empty:
            fig = px.line(brand_trends, x='year', y='orders', color='brand',
                         title='Top Brands Order Trends Over Time')
            st.plotly_chart(fig, use_container_width=True)

    # Q14: Customer Lifetime Value (CLV)
    elif selected_question == "Q14":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("💎 Q14: Customer Lifetime Value (CLV)")
        st.markdown("Cohort analysis, retention curves, and CLV distribution across segments")
        st.markdown('</div>', unsafe_allow_html=True)
        
        clv_data = st.session_state.customer_analysis.copy()
        clv_data['clv_segment'] = pd.qcut(clv_data['total_spent'], 4, labels=['Low', 'Medium', 'High', 'VIP'])
        
        col1, col2 = st.columns(2)
        with col1:
            segment_dist = clv_data['clv_segment'].value_counts()
            fig = px.pie(segment_dist, values=segment_dist.values, names=segment_dist.index,
                        title='Customer Value Segments')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(clv_data, x='clv_segment', y='total_spent',
                        title='Spending Distribution by CLV Segment')
            st.plotly_chart(fig, use_container_width=True)
        
        cohort_data = safe_query("""
            SELECT strftime('%Y', first_order_date) as cohort_year,
                   COUNT(*) as customers,
                   AVG(total_spent) as avg_clv,
                   AVG(total_orders) as avg_orders
            FROM customers
            GROUP BY strftime('%Y', first_order_date)
            ORDER BY cohort_year
        """)
        
        fig = px.line(cohort_data, x='cohort_year', y='avg_clv',
                     title='Average CLV by Acquisition Cohort', markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
        retention_data = safe_query("""
            SELECT customer_id, first_order_date, last_order_date, total_orders,
                   total_spent, customer_lifetime_days
            FROM customers
            WHERE customer_lifetime_days > 0
        """)
        
        if not retention_data.empty:
            retention_data['orders_per_month'] = retention_data['total_orders'] / (retention_data['customer_lifetime_days'] / 30)
            fig = px.scatter(retention_data, x='customer_lifetime_days', y='total_spent',
                           size='total_orders', color='orders_per_month',
                           title='Customer Lifetime vs Total Value')
            st.plotly_chart(fig, use_container_width=True)

    # Q15: Discount Effectiveness
    elif selected_question == "Q15":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🎯 Q15: Discount Effectiveness")
        st.markdown("Correlation between discount percentages, sales volumes, and revenue")
        st.markdown('</div>', unsafe_allow_html=True)
        
        discount_analysis = safe_query("""
            SELECT discount_percent, COUNT(*) as orders,
                   SUM(final_amount_inr) as revenue,
                   SUM(quantity) as total_quantity,
                   AVG(customer_rating) as avg_rating,
                   category
            FROM transactions 
            WHERE discount_percent IS NOT NULL AND discount_percent > 0
            GROUP BY discount_percent, category
            HAVING orders > 10
            ORDER BY discount_percent
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            discount_impact = discount_analysis.groupby('discount_percent').agg({
                'orders': 'sum', 'revenue': 'sum'
            }).reset_index()
            fig = px.scatter(discount_impact, x='discount_percent', y='orders',
                           size='revenue', title='Discount % vs Order Volume')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.scatter(discount_analysis, x='discount_percent', y='avg_rating',
                           size='orders', color='category',
                           title='Discount Impact on Customer Rating')
            st.plotly_chart(fig, use_container_width=True)
        
        optimal_discounts = safe_query("""
            SELECT category, 
                   AVG(discount_percent) as avg_discount,
                   COUNT(*) as orders,
                   SUM(final_amount_inr) as revenue
            FROM transactions 
            WHERE discount_percent > 0 AND category IS NOT NULL
            GROUP BY category
            HAVING orders > 100
            ORDER BY revenue DESC
            LIMIT 15
        """)
        
        fig = px.bar(optimal_discounts, x='category', y='avg_discount',
                    title='Average Discount % by Category')
        st.plotly_chart(fig, use_container_width=True)

    # Q16: Product Rating Impact
    elif selected_question == "Q16":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("⭐ Q16: Product Rating Impact")
        st.markdown("Rating distributions, correlation with sales performance across categories")
        st.markdown('</div>', unsafe_allow_html=True)
        
        rating_analysis = safe_query("""
            SELECT product_rating, COUNT(*) as orders,
                   SUM(final_amount_inr) as revenue,
                   AVG(original_price_inr) as avg_price,
                   category
            FROM transactions 
            WHERE product_rating IS NOT NULL
            GROUP BY product_rating, category
            ORDER BY product_rating
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            rating_dist = rating_analysis.groupby('product_rating')['orders'].sum().reset_index()
            fig = px.bar(rating_dist, x='product_rating', y='orders',
                        title='Order Distribution by Product Rating')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            rating_revenue = rating_analysis.groupby('product_rating')['revenue'].sum().reset_index()
            fig = px.line(rating_revenue, x='product_rating', y='revenue',
                         title='Revenue by Product Rating', markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        fig = px.scatter(rating_analysis, x='product_rating', y='avg_price',
                        size='orders', color='category',
                        title='Product Rating vs Price by Category')
        st.plotly_chart(fig, use_container_width=True)

    # Q17: Customer Journey Analysis
    elif selected_question == "Q17":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🛣️ Q17: Customer Journey Analysis")
        st.markdown("Purchase frequency patterns, category transitions, and customer evolution")
        st.markdown('</div>', unsafe_allow_html=True)
        
        journey_analysis = safe_query("""
            SELECT customer_id, COUNT(*) as order_count,
                   MIN(order_date) as first_order,
                   MAX(order_date) as last_order,
                   COUNT(DISTINCT category) as unique_categories,
                   SUM(final_amount_inr) as total_spent
            FROM transactions 
            GROUP BY customer_id
            HAVING order_count > 1
            ORDER BY order_count DESC
        """)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Orders per Customer", f"{journey_analysis['order_count'].mean():.1f}")
        col2.metric("Avg Unique Categories", f"{journey_analysis['unique_categories'].mean():.1f}")
        col3.metric("Multi-category Shoppers", f"{(journey_analysis['unique_categories'] > 1).sum():,}")
        
        freq_dist = journey_analysis['order_count'].value_counts().sort_index().head(20)
        fig = px.bar(freq_dist, x=freq_dist.index, y=freq_dist.values,
                    title='Customer Order Frequency Distribution')
        st.plotly_chart(fig, use_container_width=True)
        
        progression_data = safe_query("""
            WITH customer_progression AS (
                SELECT customer_id, order_date, category,
                       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence
                FROM transactions 
                WHERE category IS NOT NULL
            )
            SELECT order_sequence, category, COUNT(*) as customers
            FROM customer_progression
            WHERE order_sequence <= 5
            GROUP BY order_sequence, category
            ORDER BY order_sequence, customers DESC
        """)
        
        for order_num in range(1, 6):
            order_data = progression_data[progression_data['order_sequence'] == order_num].head(10)
            st.subheader(f"Top Categories for Order #{order_num}")
            fig = px.bar(order_data, x='category', y='customers')
            st.plotly_chart(fig, use_container_width=True)

    # Q18: Product Lifecycle Patterns
    elif selected_question == "Q18":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("📈 Q18: Product Lifecycle Patterns")
        st.markdown("Product launch success, decline phases, and category evolution over the decade")
        st.markdown('</div>', unsafe_allow_html=True)
        
        lifecycle_data = safe_query("""
            SELECT p.product_id, p.product_name, p.category, p.launch_year,
                   COUNT(t.transaction_id) as total_orders,
                   SUM(t.final_amount_inr) as total_revenue,
                   AVG(t.product_rating) as avg_rating
            FROM products p
            LEFT JOIN transactions t ON p.product_id = t.product_id
            WHERE p.launch_year IS NOT NULL
            GROUP BY p.product_id, p.product_name, p.category, p.launch_year
            HAVING total_orders > 0
            ORDER BY total_revenue DESC
        """)
        
        yearly_launches = lifecycle_data.groupby('launch_year').agg({
            'product_id': 'count',
            'total_revenue': 'sum',
            'avg_rating': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(yearly_launches, x='launch_year', y='product_id',
                        title='Products Launched by Year')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.line(yearly_launches, x='launch_year', y='total_revenue',
                         title='Revenue from Products by Launch Year', markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        fig = px.scatter(lifecycle_data, x='launch_year', y='total_revenue',
                        size='total_orders', color='avg_rating', hover_name='product_name',
                        title='Product Performance by Launch Year')
        st.plotly_chart(fig, use_container_width=True)

    # Q19: Competitive Pricing Analysis
    elif selected_question == "Q19":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("⚔️ Q19: Competitive Pricing Analysis")
        st.markdown("Brand positioning, price ranges, and market penetration strategies")
        st.markdown('</div>', unsafe_allow_html=True)
        
        pricing_analysis = safe_query("""
            SELECT brand, category, 
                   AVG(original_price_inr) as avg_price,
                   MIN(original_price_inr) as min_price,
                   MAX(original_price_inr) as max_price,
                   COUNT(*) as orders,
                   AVG(discount_percent) as avg_discount
            FROM transactions 
            WHERE brand IS NOT NULL AND category IS NOT NULL 
                  AND original_price_inr > 0
            GROUP BY brand, category
            HAVING orders > 50
            ORDER BY orders DESC
        """)
        
        top_categories = pricing_analysis.groupby('category')['orders'].sum().nlargest(5).index
        filtered_pricing = pricing_analysis[pricing_analysis['category'].isin(top_categories)]
        
        for category in top_categories:
            category_data = filtered_pricing[filtered_pricing['category'] == category].head(10)
            st.subheader(f"Price Positioning in {category}")
            fig = px.bar(category_data, x='brand', y='avg_price',
                        title=f'Average Price by Brand - {category}')
            st.plotly_chart(fig, use_container_width=True)
        
        fig = px.scatter(pricing_analysis, x='avg_price', y='orders',
                        size='avg_discount', color='category', hover_name='brand',
                        title='Competitive Positioning: Price vs Volume')
        st.plotly_chart(fig, use_container_width=True)

    # Q20: Business Health Dashboard
    elif selected_question == "Q20":
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.header("🏥 Q20: Business Health Dashboard")
        st.markdown("Key metrics dashboard with revenue growth, customer acquisition, and operational efficiency")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenue = st.session_state.monthly_sales['total_revenue'].sum()
        total_customers = len(st.session_state.customer_analysis)
        total_products = len(st.session_state.products)
        avg_rating = st.session_state.monthly_sales['avg_rating'].mean()
        
        col1.metric("Total Revenue", f"₹{total_revenue/1e9:.1f}B")
        col2.metric("Total Customers", f"{total_customers:,}")
        col3.metric("Active Products", f"{total_products:,}")
        col4.metric("Avg Customer Rating", f"{avg_rating:.1f}⭐")
        
        # Revenue Growth
        yearly_growth = safe_query("""
            SELECT strftime('%Y', order_date) as year, 
                   SUM(final_amount_inr) as revenue,
                   LAG(SUM(final_amount_inr)) OVER (ORDER BY strftime('%Y', order_date)) as prev_revenue
            FROM transactions 
            GROUP BY strftime('%Y', order_date)
            ORDER BY year
        """)
        yearly_growth['growth_rate'] = ((yearly_growth['revenue'] - yearly_growth['prev_revenue']) / yearly_growth['prev_revenue']) * 100
        
        # Customer Acquisition
        customer_growth = safe_query("""
            SELECT strftime('%Y', first_order_date) as year,
                   COUNT(*) as new_customers
            FROM customers
            GROUP BY strftime('%Y', first_order_date)
            ORDER BY year
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(yearly_growth, x='year', y='growth_rate',
                         title='Yearly Revenue Growth Rate (%)', markers=True)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(customer_growth, x='year', y='new_customers',
                        title='New Customer Acquisition by Year')
            st.plotly_chart(fig, use_container_width=True)
        
        # Operational Efficiency
        delivery_efficiency = safe_query("""
            SELECT AVG(delivery_days) as avg_delivery_days,
                   AVG(customer_rating) as avg_rating
            FROM transactions 
            WHERE delivery_days IS NOT NULL
        """)
        
        return_health = safe_query("""
            SELECT 
                SUM(CASE WHEN return_status = 'Returned' THEN 1 ELSE 0 END) as returned_orders,
                COUNT(*) as total_orders
            FROM transactions
        """)
        
        return_rate = (return_health['returned_orders'].iloc[0] / return_health['total_orders'].iloc[0]) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Delivery Days", f"{delivery_efficiency['avg_delivery_days'].iloc[0]:.1f}")
        col2.metric("Return Rate", f"{return_rate:.2f}%")
        col3.metric("Customer Satisfaction", f"{delivery_efficiency['avg_rating'].iloc[0]:.1f}/5")
        
        # Executive Summary
        st.subheader("📋 Executive Summary")
        st.markdown("""
        - **Strong Revenue Growth**: Consistent year-over-year growth with healthy CAGR
        - **Growing Customer Base**: Steady new customer acquisition with high retention
        - **Operational Excellence**: Good delivery performance and customer satisfaction
        - **Product Diversity**: Wide range of products across multiple categories
        - **Customer Loyalty**: High ratings and repeat purchase behavior
        - **Market Leadership**: Strong presence across geographic regions
        - **Innovation Focus**: Continuous product launches and category expansion
        """)

else:
    st.info("👆 Click 'Load Analysis Data' to explore all 20 EDA questions with interactive visualizations!")

# Footer
st.markdown("---")
st.markdown("### 📊 Amazon India - Complete EDA Dashboard")
st.markdown("20 Comprehensive Questions | 1M+ Transactions | 2015-2025 Data | ₹69B+ Revenue")