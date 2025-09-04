# Basketball Shot Analyzer - Quick Start Guide for Render.com

## 🎯 5-Minute Deployment Guide

Your Basketball Shot Analyzer is ready to deploy! Follow these exact steps:

---

## Step 1: Go to Render.com
1. Open: **https://render.com/**
2. Click **"Get Started for Free"**
3. Choose **"Continue with GitHub"**

---

## Step 2: Create Web Service
1. Click the **"New +"** button (top right)
2. Select **"Web Service"**
3. Find your repository: **`apexsports-basketball-analyzer`**
4. Click **"Connect"**

---

## Step 3: Fill Out the Form

**Copy and paste these exact settings:**

**Service Details:**
- **Name**: `basketball-shot-analyzer`
- **Region**: `Oregon (US West)`
- **Branch**: `main`
- **Root Directory**: (leave blank)

**Build Settings:**
- **Runtime**: `Python 3`
- **Build Command**: 
```
pip install -r requirements.txt
```
- **Start Command**: 
```
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false
```

**Plan:**
- **Instance Type**: `Free`

---

## Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Your app will be live at the URL Render provides!

---

## 🎉 That's It!

Your Basketball Shot Analyzer with enhanced elbow detection and frame labeling will be live on the internet!

**What happens next:**
- Every time you push to GitHub, your app automatically updates
- Your app sleeps after 15 minutes of inactivity (free tier)
- First visitor wakes it up (takes ~30 seconds)

**Troubleshooting:**
- If deployment fails, check the build logs in Render dashboard
- Your app works locally, so it should work on Render too!

---

## 🔗 Useful Links
- **Render Dashboard**: https://dashboard.render.com/
- **Your GitHub Repo**: https://github.com/rickdyer20/apexsports-basketball-analyzer
- **Local App**: http://localhost:8501
