# Basketball Shot Analyzer - Render.com Deployment Guide

## Quick Deployment to Render (FREE)

Render.com offers free hosting for web applications without requiring payment verification.

### Step 1: Push to GitHub
```bash
git add .
git commit -m "feat: Add Render.com deployment configuration"
git push origin main
```

### Step 2: Deploy on Render.com

1. **Visit**: https://render.com/
2. **Sign up/Login** with your GitHub account
3. **Click "New Web Service"**
4. **Connect your repository**: `rickdyer20/apexsports-basketball-analyzer`
5. **Configure the service**:
   - **Name**: `basketball-shot-analyzer`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false`
   - **Instance Type**: `Free`

6. **Click "Create Web Service"**

### Step 3: Environment Variables (Optional)
- `PYTHONPATH`: `/opt/render/project/src`
- `STREAMLIT_SERVER_HEADLESS`: `true`

### Your app will be available at:
`https://basketball-shot-analyzer.onrender.com`

## Alternative: Manual Render Deployment

If you prefer manual setup, you can also:
1. Create a GitHub repository
2. Upload your code
3. Connect to Render.com
4. Deploy automatically from GitHub

## Benefits of Render vs Heroku:
- ✅ **Free tier available** (no payment verification required)
- ✅ **Automatic deployments** from GitHub
- ✅ **Better Streamlit support** (no auto-detection issues like Railway)
- ✅ **Easy SSL/HTTPS** included
- ✅ **Good performance** for Python apps
