"""
NovaMart Marketing Analytics Dashboard
=============================================
Neha Thapa , Masters of AI in Business - Data Visualization Assignment 

A comprehensive Streamlit dashboard for marketing analytics, including
campaign performance, customer insights, product analysis, and ML model evaluation.

Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import confusion_matrix, roc_curve, auc
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="NovaMart Marketing Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
    }
    h2 {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING (with caching)
# =============================================================================
@st.cache_data
def load_data():
    """Load all datasets from CSV files"""
    data = {}
    
    try:
        data['campaigns'] = pd.read_csv('campaign_performance.csv', parse_dates=['date'])
        data['customers'] = pd.read_csv('customer_data.csv')
        data['products'] = pd.read_csv('product_sales.csv')
        data['leads'] = pd.read_csv('lead_scoring_results.csv')
        data['feature_importance'] = pd.read_csv('feature_importance.csv')
        data['learning_curve'] = pd.read_csv('learning_curve.csv')
        data['geographic'] = pd.read_csv('geographic_data.csv')
        data['attribution'] = pd.read_csv('channel_attribution.csv')
        data['funnel'] = pd.read_csv('funnel_data.csv')
        data['journey'] = pd.read_csv('customer_journey.csv')
        data['correlation'] = pd.read_csv('correlation_matrix.csv', index_col=0)
        
        return data
    except FileNotFoundError as e:
        st.error(f"❌ Data file not found: {e}")
        st.info("Please ensure all CSV files are in the same directory as app.py")
        return None

# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================
def sidebar():
    """Create sidebar navigation"""
    st.sidebar.title("📊 NovaMart Analytics")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigate to:",
        [
            "🏠 Executive Overview",
            "📈 Campaign Analytics",
            "👥 Customer Insights",
            "📦 Product Performance",
            "🗺️ Geographic Analysis",
            "🎯 Attribution & Funnel",
            "🤖 ML Model Evaluation"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("**Neha Thapa**\n\nMasters of AI in Business**\n\nData Visualization Assignment\n\n*NovaMart - Marketing Analytics Dashboard*")
    
    return page

# =============================================================================
# PAGE: EXECUTIVE OVERVIEW
# =============================================================================
def page_executive_overview(data):
    """Executive Overview Dashboard with key KPIs"""
    st.title("🏠 Executive Overview")
    st.markdown("Key performance metrics and trends at a glance")
    
    campaigns = data['campaigns']
    customers = data['customers']
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = campaigns['revenue'].sum()
        st.metric("Total Revenue", f"₹{total_revenue/1e7:.2f} Cr", delta="+12.5%")
    
    with col2:
        total_conversions = campaigns['conversions'].sum()
        st.metric("Total Conversions", f"{total_conversions:,}", delta="+8.3%")
    
    with col3:
        avg_roas = campaigns[campaigns['roas'] > 0]['roas'].mean()
        st.metric("Avg ROAS", f"{avg_roas:.2f}x", delta="-2.1%")
    
    with col4:
        total_customers = len(customers)
        st.metric("Total Customers", f"{total_customers:,}", delta="+5.2%")
    
    st.markdown("---")
    
    # Revenue Trend
    st.subheader("📈 Revenue Trend Over Time")
    monthly_revenue = campaigns.groupby(pd.Grouper(key='date', freq='M'))['revenue'].sum().reset_index()
    
    fig_revenue = px.line(
        monthly_revenue, 
        x='date', 
        y='revenue',
        title='Monthly Revenue Trend (₹)',
        labels={'date': 'Month', 'revenue': 'Revenue'},
        markers=True
    )
    fig_revenue.update_layout(hovermode='x unified', height=400)
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Channel Performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Revenue by Channel")
        channel_revenue = campaigns.groupby('channel')['revenue'].sum().sort_values(ascending=True).reset_index()
        fig_channel = px.bar(channel_revenue, x='revenue', y='channel', title='Revenue by Channel')
        fig_channel.update_layout(height=400)
        st.plotly_chart(fig_channel, use_container_width=True)
    
    with col2:
        st.subheader("📍 Revenue by Region")
        region_revenue = campaigns.groupby('region')['revenue'].sum().sort_values(ascending=True).reset_index()
        fig_region = px.bar(region_revenue, x='revenue', y='region', title='Revenue by Region')
        fig_region.update_layout(height=400)
        st.plotly_chart(fig_region, use_container_width=True)
    
    st.markdown("---")
    
    # Customer Segment Performance
    st.subheader("👥 Customer Segment Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        segment_count = customers['customer_segment'].value_counts().reset_index()
        segment_count.columns = ['Segment', 'Count']
        fig_segment = px.pie(segment_count, values='Count', names='Segment', title='Customer Distribution by Segment')
        st.plotly_chart(fig_segment, use_container_width=True)
    
    with col2:
        segment_ltv = customers.groupby('customer_segment')['lifetime_value'].mean().sort_values(ascending=True).reset_index()
        fig_ltv = px.bar(segment_ltv, x='lifetime_value', y='customer_segment', title='Avg Lifetime Value by Segment')
        st.plotly_chart(fig_ltv, use_container_width=True)

# =============================================================================
# PAGE: CAMPAIGN ANALYTICS
# =============================================================================
def page_campaign_analytics(data):
    """Campaign Performance Analysis"""
    st.title("📈 Campaign Analytics")
    st.markdown("Detailed campaign performance metrics and insights")
    
    campaigns = data['campaigns']
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_channel = st.multiselect("Select Channel(s)", campaigns['channel'].unique(), default=campaigns['channel'].unique())
    
    with col2:
        selected_campaign = st.multiselect("Select Campaign Type(s)", campaigns['campaign_type'].unique(), default=campaigns['campaign_type'].unique())
    
    with col3:
        date_range = st.date_input("Select Date Range", [campaigns['date'].min(), campaigns['date'].max()])
    
    # Filter data
    filtered_campaigns = campaigns[
        (campaigns['channel'].isin(selected_channel)) &
        (campaigns['campaign_type'].isin(selected_campaign)) &
        (campaigns['date'].dt.date >= date_range[0]) &
        (campaigns['date'].dt.date <= date_range[1])
    ]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Spend", f"₹{filtered_campaigns['spend'].sum()/1e5:.2f} Lakhs")
    with col2:
        st.metric("Total Impressions", f"{filtered_campaigns['impressions'].sum()/1e6:.2f}M")
    with col3:
        st.metric("Avg CTR", f"{(filtered_campaigns['clicks'].sum() / filtered_campaigns['impressions'].sum() * 100):.2f}%")
    with col4:
        st.metric("Avg CVR", f"{(filtered_campaigns['conversions'].sum() / filtered_campaigns['clicks'].sum() * 100):.2f}%")
    
    st.markdown("---")
    
    # Campaign Performance Comparison
    st.subheader("📊 Campaign Type Performance")
    campaign_perf = filtered_campaigns.groupby('campaign_type').agg({
        'spend': 'sum',
        'revenue': 'sum',
        'conversions': 'sum',
        'roas': 'mean'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(campaign_perf, x='campaign_type', y='spend', title='Spend by Campaign Type', text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(campaign_perf, x='campaign_type', y='revenue', title='Revenue by Campaign Type', text_auto=True)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Daily Trend
    st.subheader("📅 Daily Performance Trends")
    daily_perf = filtered_campaigns.groupby('date').agg({
        'spend': 'sum',
        'revenue': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=daily_perf['date'], y=daily_perf['revenue'], name='Revenue', line=dict(color='#1f77b4')), secondary_y=False)
    fig.add_trace(go.Bar(x=daily_perf['date'], y=daily_perf['spend'], name='Spend', marker=dict(color='#ff7f0e'), opacity=0.6), secondary_y=True)
    
    fig.update_layout(hovermode='x unified', height=400, title_text='Revenue vs Spend Trend')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Revenue', secondary_y=False)
    fig.update_yaxes(title_text='Spend', secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Channel Performance Comparison
    st.subheader("🎯 Channel Performance Matrix")
    channel_metrics = filtered_campaigns.groupby('channel').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    channel_metrics['CTR'] = (channel_metrics['clicks'] / channel_metrics['impressions'] * 100).round(2)
    channel_metrics['CVR'] = (channel_metrics['conversions'] / channel_metrics['clicks'] * 100).round(2)
    channel_metrics['ROAS'] = (channel_metrics['revenue'] / channel_metrics['spend']).round(2)
    
    st.dataframe(channel_metrics[['channel', 'CTR', 'CVR', 'ROAS']], use_container_width=True)

# =============================================================================
# PAGE: CUSTOMER INSIGHTS
# =============================================================================
def page_customer_insights(data):
    """Customer Analytics and Behavior"""
    st.title("👥 Customer Insights")
    st.markdown("Understanding customer demographics, behavior, and segments")
    
    customers = data['customers']
    
    # Customer Demographics
    st.subheader("📊 Customer Demographics")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_age = px.histogram(customers, x='age', nbins=30, title='Age Distribution', labels={'age': 'Age', 'count': 'Number of Customers'})
        fig_age.update_layout(height=400)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        fig_income = px.histogram(customers, x='income', nbins=30, title='Income Distribution', labels={'income': 'Income', 'count': 'Number of Customers'})
        fig_income.update_layout(height=400)
        st.plotly_chart(fig_income, use_container_width=True)
    
    # Income vs Lifetime Value
    st.subheader("💰 Income vs Lifetime Value")
    fig_scatter = px.scatter(
        customers, 
        x='income', 
        y='lifetime_value', 
        color='customer_segment',
        size='purchase_frequency',
        hover_data=['age', 'satisfaction_score'],
        title='Customer Income vs LTV'
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Satisfaction Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("😊 Satisfaction Score Distribution")
        fig_satisfaction = px.box(customers, y='satisfaction_score', title='Satisfaction Score Distribution')
        fig_satisfaction.update_layout(height=400)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    with col2:
        st.subheader("🎯 NPS Category Distribution")
        nps_counts = customers['nps_category'].value_counts().reset_index()
        nps_counts.columns = ['NPS Category', 'Count']
        fig_nps = px.pie(nps_counts, values='Count', names='NPS Category', title='NPS Category Distribution')
        st.plotly_chart(fig_nps, use_container_width=True)
    
    # Churn Analysis
    st.subheader("⚠️ Churn Risk Analysis")
    churn_data = customers.groupby('churn_risk').size().reset_index(name='Count')
    col1, col2 = st.columns(2)
    
    with col1:
        fig_churn = px.pie(churn_data, values='Count', names='churn_risk', title='Churn Risk Distribution')
        st.plotly_chart(fig_churn, use_container_width=True)
    
    with col2:
        high_risk = customers[customers['churn_risk'] == 'High']
        st.metric("High Risk Customers", len(high_risk), delta=f"{len(high_risk)/len(customers)*100:.1f}%")
        st.write(f"**Average Satisfaction**: {high_risk['satisfaction_score'].mean():.2f}/10")
        st.write(f"**Average Support Tickets**: {high_risk['support_tickets'].mean():.1f}")

# =============================================================================
# PAGE: PRODUCT PERFORMANCE
# =============================================================================
def page_product_performance(data):
    """Product Sales Analysis"""
    st.title("📦 Product Performance")
    st.markdown("Product sales, categories, and performance metrics")
    
    products = data['products']
    
    # Sales by Category
    st.subheader("📊 Sales by Product Category")
    category_sales = products.groupby('category')['sales'].sum().sort_values(ascending=True).reset_index()
    
    fig_category = px.bar(category_sales, x='sales', y='category', title='Total Sales by Category')
    fig_category.update_layout(height=400)
    st.plotly_chart(fig_category, use_container_width=True)
    
    # Sales by Subcategory
    st.subheader("🔍 Sales by Subcategory")
    subcategory_sales = products.groupby('subcategory')['sales'].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig_subcat = px.bar(subcategory_sales, x='sales', y='subcategory', orientation='h', title='Top 10 Subcategories by Sales')
    fig_subcat.update_layout(height=400)
    st.plotly_chart(fig_subcat, use_container_width=True)
    
    # Treemap
    st.subheader("🌳 Product Hierarchy (Treemap)")
    fig_tree = px.treemap(
        products,
        labels='product_name',
        parents='category',
        values='sales',
        title='Product Sales Treemap'
    )
    st.plotly_chart(fig_tree, use_container_width=True)
    
    # Quarterly Trends
    st.subheader("📈 Quarterly Sales Trends")
    quarterly_sales = products.groupby('quarter')['sales'].sum().reset_index()
    fig_quarter = px.line(quarterly_sales, x='quarter', y='sales', title='Sales by Quarter', markers=True)
    st.plotly_chart(fig_quarter, use_container_width=True)

# =============================================================================
# PAGE: GEOGRAPHIC ANALYSIS
# =============================================================================
def page_geographic_analysis(data):
    """Geographic Performance Analysis"""
    st.title("🗺️ Geographic Analysis")
    st.markdown("Regional performance and geographic insights")
    
    geographic = data['geographic']
    
    # Geographic Distribution
    st.subheader("🌍 Geographic Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Revenue by State")
        state_revenue = geographic.sort_values('revenue', ascending=True)
        fig_state = px.bar(state_revenue, x='revenue', y='state', title='Revenue by State')
        fig_state.update_layout(height=500)
        st.plotly_chart(fig_state, use_container_width=True)
    
    with col2:
        st.subheader("⭐ Satisfaction by State")
        state_sat = geographic.sort_values('satisfaction_score', ascending=True)
        fig_sat = px.bar(state_sat, x='satisfaction_score', y='state', title='Satisfaction Score by State')
        fig_sat.update_layout(height=500)
        st.plotly_chart(fig_sat, use_container_width=True)
    
    # Choropleth Map
    st.subheader("🗺️ Revenue Map (Geographic)")
    fig_map = px.scatter_geo(
        geographic,
        lat='latitude',
        lon='longitude',
        size='revenue',
        hover_name='state',
        hover_data=['store_count', 'satisfaction_score'],
        title='Revenue by Geographic Location'
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    # State Performance Table
    st.subheader("📋 State Performance Summary")
    st.dataframe(geographic[['state', 'store_count', 'revenue', 'satisfaction_score']], use_container_width=True)

# =============================================================================
# PAGE: ATTRIBUTION & FUNNEL
# =============================================================================
def page_attribution_funnel(data):
    """Attribution and Funnel Analysis"""
    st.title("🎯 Attribution & Funnel Analysis")
    st.markdown("Multi-touch attribution and conversion funnel insights")
    
    attribution = data['attribution']
    funnel = data['funnel']
    journey = data['journey']
    
    # Attribution Models Comparison
    st.subheader("📊 Attribution Model Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### First-Touch Attribution")
        first_touch = attribution[['channel', 'first_touch']].sort_values('first_touch', ascending=True)
        fig_first = px.bar(first_touch, x='first_touch', y='channel', title='First-Touch Attribution')
        st.plotly_chart(fig_first, use_container_width=True)
    
    with col2:
        st.write("### Last-Touch Attribution")
        last_touch = attribution[['channel', 'last_touch']].sort_values('last_touch', ascending=True)
        fig_last = px.bar(last_touch, x='last_touch', y='channel', title='Last-Touch Attribution')
        st.plotly_chart(fig_last, use_container_width=True)
    
    # Marketing Funnel
    st.subheader("🔀 Marketing Conversion Funnel")
    fig_funnel = px.funnel(
        funnel,
        x='visitors',
        y='stage',
        title='Marketing Funnel - Visitor Flow'
    )
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # Customer Journey
    st.subheader("🛤️ Multi-Touchpoint Customer Journeys")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Top Customer Journeys")
        journey_counts = journey['path'].value_counts().head(8).reset_index()
        journey_counts.columns = ['Journey Path', 'Count']
        st.dataframe(journey_counts, use_container_width=True)
    
    with col2:
        fig_journey = px.bar(journey_counts, x='Journey Path', y='Count', title='Top Customer Journey Paths')
        st.plotly_chart(fig_journey, use_container_width=True)

# =============================================================================
# PAGE: ML MODEL EVALUATION
# =============================================================================
def page_ml_model_evaluation(data):
    """ML Model Performance Evaluation"""
    st.title("🤖 ML Model Evaluation")
    st.markdown("Lead Scoring Model - Performance Metrics & Analysis")
    
    leads = data['leads']
    feature_importance = data['feature_importance']
    learning_curve = data['learning_curve']
    
    # Model Performance Metrics
    st.subheader("📊 Model Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    tn, fp, fn, tp = confusion_matrix(leads['actual_converted'], leads['predicted_class']).ravel()
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    
    with col1:
        st.metric("Accuracy", f"{accuracy:.3f}", delta="+2.1%")
    with col2:
        st.metric("Precision", f"{precision:.3f}")
    with col3:
        st.metric("Recall", f"{recall:.3f}")
    with col4:
        st.metric("F1-Score", f"{f1:.3f}")
    
    st.markdown("---")
    
    # Confusion Matrix
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Confusion Matrix")
        cm = confusion_matrix(leads['actual_converted'], leads['predicted_class'])
        fig_cm = px.imshow(
            cm,
            labels=dict(x="Predicted", y="Actual", color="Count"),
            x=['No Conversion', 'Conversion'],
            y=['No Conversion', 'Conversion'],
            title='Confusion Matrix',
            text_auto=True,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_cm, use_container_width=True)
    
    with col2:
        st.subheader("📈 ROC Curve")
        fpr, tpr, _ = roc_curve(leads['actual_converted'], leads['predicted_probability'])
        roc_auc = auc(fpr, tpr)
        
        fig_roc = px.line(x=fpr, y=tpr, title=f'ROC Curve (AUC = {roc_auc:.3f})')
        fig_roc.add_shape(type='line', line=dict(dash='dash'), x0=0, x1=1, y0=0, y1=1)
        fig_roc.update_layout(xaxis_title='False Positive Rate', yaxis_title='True Positive Rate', height=400)
        st.plotly_chart(fig_roc, use_container_width=True)
    
    # Feature Importance
    st.subheader("🔝 Feature Importance (Top Features)")
    fig_importance = px.bar(
        feature_importance.sort_values('importance'),
        x='importance',
        y='feature',
        title='Feature Importance Scores'
    )
    fig_importance.update_layout(height=400)
    st.plotly_chart(fig_importance, use_container_width=True)
    
    # Learning Curve
    st.subheader("📚 Learning Curve")
    fig_learning = px.line(
        learning_curve,
        x='data_size',
        y=['training_score', 'validation_score'],
        title='Model Performance vs Training Data Size',
        labels={'x': 'Data Size', 'value': 'Score', 'variable': 'Dataset'}
    )
    fig_learning.update_layout(height=400)
    st.plotly_chart(fig_learning, use_container_width=True)
    
    # Prediction Distribution
    st.subheader("📊 Prediction Probability Distribution")
    fig_dist = px.histogram(
        leads,
        x='predicted_probability',
        nbins=30,
        title='Distribution of Predicted Probabilities',
        labels={'predicted_probability': 'Predicted Probability', 'count': 'Number of Leads'}
    )
    st.plotly_chart(fig_dist, use_container_width=True)

# =============================================================================
# MAIN APP
# =============================================================================
def main():
    """Main application entry point"""
    # Load data
    data = load_data()
    
    if data is None:
        st.stop()
    
    # Sidebar navigation
    page = sidebar()
    
    # Route to appropriate page
    if page == "🏠 Executive Overview":
        page_executive_overview(data)
    elif page == "📈 Campaign Analytics":
        page_campaign_analytics(data)
    elif page == "👥 Customer Insights":
        page_customer_insights(data)
    elif page == "📦 Product Performance":
        page_product_performance(data)
    elif page == "🗺️ Geographic Analysis":
        page_geographic_analysis(data)
    elif page == "🎯 Attribution & Funnel":
        page_attribution_funnel(data)
    elif page == "🤖 ML Model Evaluation":
        page_ml_model_evaluation(data)

if __name__ == "__main__":
    main()


