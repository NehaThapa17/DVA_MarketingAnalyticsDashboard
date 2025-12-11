# 🚀 Deployment Guide

## GitHub Setup

### 1. Initialize Git Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: NovaMart Marketing Analytics Dashboard"
```

### 2. Create GitHub Repository
- Go to [github.com/new](https://github.com/new)
- Create a new repository named `marketing-analytics-dashboard`
- Choose Public (for free Streamlit Cloud)
- Do NOT initialize with README (you already have one)

### 3. Add Remote and Push
```bash
git remote add origin https://github.com/yourusername/marketing-analytics-dashboard.git
git branch -M main
git push -u origin main
```

---

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- All files committed and pushed to GitHub
- All CSV data files in the repository

### Step-by-Step Deployment

1. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign in with GitHub"
   - Authorize Streamlit to access your repositories

2. **Deploy New App**
   - Click "New app" button
   - Select:
     - **Repository**: yourusername/marketing-analytics-dashboard
     - **Branch**: main
     - **Main file path**: `app.py`
   - Click "Deploy"

3. **Configuration**
   - Streamlit will build and deploy automatically
   - First deployment takes 2-3 minutes
   - You'll get a public URL: `https://share.streamlit.io/yourusername/marketing-analytics-dashboard/app.py`

### Custom Domain (Optional)
- Streamlit Cloud supports custom domains
- See [Streamlit Cloud docs](https://docs.streamlit.io/cloud/get-started) for details

---

## Post-Deployment

### Verify Deployment
- Open your Streamlit Cloud URL
- Test all dashboard pages
- Check that data loads correctly
- Verify all charts display properly

### Update Your Code
After pushing changes to GitHub:
```bash
git add .
git commit -m "Update: [description of changes]"
git push origin main
```

Streamlit Cloud will automatically redeploy within 1-2 minutes.

### Monitor Performance
- Check Streamlit Cloud dashboard for logs
- Monitor app usage and performance
- Streamlit Cloud provides free 1GB of storage per app

---

## Environment Variables (Optional)

If you need sensitive data (API keys, etc.):

1. In Streamlit Cloud dashboard, go to app settings
2. Add secrets in "Secrets management"
3. Access in code with:
   ```python
   import streamlit as st
   api_key = st.secrets["api_key"]
   ```

---

## Troubleshooting Deployment

### App Won't Build
- Check build logs in Streamlit Cloud
- Ensure `requirements.txt` has all dependencies
- Verify `app.py` syntax is correct

### Module Import Errors
- Check that all imports are in `requirements.txt`
- Package names must match PyPI names exactly

### Data Files Not Found
- Ensure CSV files are in repository root
- Check file paths in `load_data()` function
- Data paths should be relative: `'campaign_performance.csv'`

### Slow Performance
- Data is cached with `@st.cache_data`
- Streamlit Cloud has resource limits for free tier
- Consider preprocessing large datasets locally

---

## Free Tier Limits

Streamlit Cloud free tier includes:
- Public apps only
- 1GB storage per app
- CPU & memory limits
- 3 apps per account
- Monthly usage tracked

For production needs, consider paid plans.

---

## Alternative Deployment Options

### Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Docker
```bash
# Create Dockerfile
docker build -t marketing-dashboard .
docker run -p 8501:8501 marketing-dashboard
```

### AWS/Azure/GCP
- Use cloud platform's container services
- Deploy Docker image
- See respective platform documentation

---

## Support & Documentation

- [Streamlit Cloud Docs](https://docs.streamlit.io/cloud)
- [Streamlit Community](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

---

**Last Updated**: December 2024
