# 📊 NovaMart Marketing Analytics Dashboard

> A comprehensive Streamlit dashboard for marketing analytics, built with Python and interactive visualizations.

**Masters of AI in Business - Data Visualization Assignment**

---

## 🎯 Overview

This project provides a production-ready Streamlit dashboard for analyzing marketing data across multiple dimensions:

- **Campaign Performance**: Revenue trends, channel analysis, conversion metrics
- **Customer Analytics**: Demographics, segmentation, lifetime value, churn risk
- **Product Performance**: Sales by category, subcategory, and quarterly trends
- **Geographic Analysis**: Regional performance and satisfaction metrics
- **Attribution & Funnel**: Multi-touch attribution and conversion funnel analysis
- **ML Model Evaluation**: Lead scoring model performance with ROC curves and feature importance

---

## 📁 Project Structure

```
marketing_dataset/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Dataset documentation
├── GITHUB_README.md               # This file
│
└── data/
    ├── campaign_performance.csv    # Daily campaign metrics (5,858 records)
    ├── customer_data.csv          # Customer profiles (5,000 records)
    ├── product_sales.csv          # Product sales (1,440 records)
    ├── lead_scoring_results.csv   # ML predictions vs actuals (2,000 records)
    ├── feature_importance.csv     # Feature importance scores
    ├── learning_curve.csv         # Model learning curve
    ├── geographic_data.csv        # State-level metrics (15 states)
    ├── channel_attribution.csv    # Attribution model comparison
    ├── funnel_data.csv           # Marketing funnel stages
    ├── customer_journey.csv       # Multi-touchpoint journeys
    └── correlation_matrix.csv     # Metric correlations
```

---

## 🚀 Quick Start

### Local Development

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/marketing-analytics-dashboard.git
cd marketing-analytics-dashboard
```

#### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the Application
```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## ☁️ Streamlit Cloud Deployment

### Deploy to Streamlit Cloud

1. **Prepare Your Repository**
   ```bash
   git add .
   git commit -m "Initial commit: NovaMart Marketing Analytics Dashboard"
   git push origin main
   ```

2. **Create Streamlit Cloud Account**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign up with GitHub

3. **Deploy Your App**
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Share Your Dashboard**
   - Streamlit Cloud generates a public URL: `https://share.streamlit.io/yourusername/repo-name/app.py`

### Streamlit Cloud Configuration

Create `.streamlit/config.toml` for Streamlit Cloud (optional):

```toml
[client]
showErrorDetails = false

[logger]
level = "info"

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

---

## 📊 Dashboard Pages

### 🏠 Executive Overview
- Key performance indicators (Revenue, Conversions, ROAS, Customer Count)
- Monthly revenue trend
- Revenue by channel and region
- Customer segment analysis

### 📈 Campaign Analytics
- Campaign performance metrics with filters
- Channel performance comparison
- Daily performance trends
- Campaign type analysis

### 👥 Customer Insights
- Demographics (age, income distribution)
- Income vs Lifetime Value scatter plot
- Satisfaction score analysis
- NPS and churn risk assessment

### 📦 Product Performance
- Sales by product category
- Top performing subcategories
- Product hierarchy treemap
- Quarterly sales trends

### 🗺️ Geographic Analysis
- Revenue distribution by state
- Regional satisfaction scores
- Geographic scatter visualization
- State performance summary

### 🎯 Attribution & Funnel
- Multi-touch attribution models (first-touch, last-touch)
- Marketing conversion funnel
- Customer journey paths
- Touchpoint analysis

### 🤖 ML Model Evaluation
- Model performance metrics (Accuracy, Precision, Recall, F1)
- Confusion matrix
- ROC curve with AUC score
- Feature importance analysis
- Learning curve visualization

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥1.28.0 | Web framework |
| `pandas` | ≥2.0.0 | Data processing |
| `numpy` | ≥1.24.0 | Numerical computing |
| `plotly` | ≥5.17.0 | Interactive visualizations |
| `scikit-learn` | ≥1.3.0 | Machine learning metrics |
| `altair` | ≥5.0.0 | Additional visualizations |

---

## 🔧 Development

### Running Tests Locally
```bash
streamlit run app.py
```

### Building for Production
The app is production-ready. Simply push to GitHub and deploy to Streamlit Cloud.

### Code Structure

The `app.py` file is organized into sections:

1. **Configuration**: Streamlit page config and styling
2. **Data Loading**: Cached data loading from CSV files
3. **Sidebar Navigation**: Multi-page navigation
4. **Page Functions**: Individual dashboard pages
5. **Main Entry Point**: Router to selected page

---

## 📈 Data Insights

### Key Dataset Characteristics

| Dataset | Records | Key Features | Time Period |
|---------|---------|--------------|-------------|
| Campaign Performance | 5,858 | Channel, ROI, Conversions | 2023-2024 |
| Customer Data | 5,000 | Demographics, Lifetime Value, Churn | 2023-2024 |
| Product Sales | 1,440 | Categories, Subcategories, Hierarchy | Quarterly |
| Lead Scoring | 2,000 | Features, Predictions, Probabilities | Recent |
| Geographic Data | 15 States | Regional Metrics, Coordinates | Current |

### Built-in Insights

- **Seasonality**: Diwali (Oct-Nov) & Christmas (Dec) show 30-40% revenue boost
- **Channel Performance**: Email highest CVR, Google Ads highest volume
- **Customer Segments**: Premium customers have 2.5x higher LTV
- **Geographic Patterns**: West and South regions outperform

---

## 🎨 Customization

### Change Title/Branding
Edit the `st.set_page_config()` section in `app.py`:
```python
st.set_page_config(
    page_title="Your Title",
    page_icon="🎯",
    layout="wide"
)
```

### Update Data Paths
Modify the data folder path in the `load_data()` function:
```python
data_path = "your_data_folder/"
```

### Modify Colors/Theme
Update Streamlit Cloud config in `.streamlit/config.toml`

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: Data file not found`
- **Solution**: Ensure all CSV files are in the same directory as `app.py` or update `data_path` variable

**Issue**: Dashboard loads slowly
- **Solution**: Data is cached with `@st.cache_data` decorator. Clear cache with `streamlit cache clear`

**Issue**: Charts not displaying
- **Solution**: Ensure Plotly is installed: `pip install --upgrade plotly`

**Issue**: Streamlit Cloud deployment fails
- **Solution**: 
  - Check that `requirements.txt` has all dependencies
  - Ensure main file is set to `app.py`
  - Check GitHub logs in Streamlit Cloud dashboard

---

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/)

---

## 📝 License

This project is part of the "Masters of AI in Business" curriculum.

---

## 👥 Contributors

- Your Name / Team

---

## 📧 Support

For issues, questions, or improvements:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

## 🔄 Version History

- **v1.0.0** (2024-12-11): Initial release with 7 dashboard pages
  - Executive Overview
  - Campaign Analytics
  - Customer Insights
  - Product Performance
  - Geographic Analysis
  - Attribution & Funnel
  - ML Model Evaluation

---

**Made with ❤️ using Streamlit**
