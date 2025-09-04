# Basketball Shot Analyzer - Complete Render.com Deployment Guide

## 🚀 Step-by-Step Deployment Instructions

### Prerequisites ✅
- [x] GitHub repository: `rickdyer20/apexsports-basketball-analyzer`
- [x] Code pushed to GitHub with all deployment files
- [x] Basketball Shot Analyzer working locally on http://localhost:8501

---

## Part 1: Prepare for Deployment

### Step 1: Verify Your Files Are Ready
Your repository should have these files (✅ = Ready):
- ✅ `app.py` - Your main Basketball Shot Analyzer application
- ✅ `requirements.txt` - Python dependencies (streamlit, opencv-python-headless, etc.)
- ✅ `runtime.txt` - Python version (python-3.11.9)
- ✅ `Procfile` - Deployment startup command

---

## Part 2: Deploy on Render.com

### Step 2: Create Render Account

1. **Open browser** and go to: **https://render.com/**
2. **Click "Get Started for Free"**
3. **Sign up using GitHub account** (recommended for easy repository access)
4. **Authorize Render** to access your GitHub repositories

### Step 3: Create New Web Service

1. **Click "New +"** button (top right)
2. **Select "Web Service"**
3. **Connect your repository**:
   - Choose "Build and deploy from a Git repository"
   - Click "Connect" next to `rickdyer20/apexsports-basketball-analyzer`
   - If you don't see your repo, click "Configure account" and grant access

### Step 4: Configure Service Settings

**Basic Settings:**
- **Name**: `basketball-shot-analyzer` (or any name you prefer)
- **Region**: `Oregon (US West)` (or closest to you)
- **Branch**: `main`
- **Root Directory**: Leave blank

**Build & Deploy Settings:**
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false
  ```

**Instance Type:**
- **Select**: `Free` (0 GB RAM, Shared CPU - Perfect for testing)

### Step 5: Environment Variables (Optional but Recommended)

Click "Advanced" and add these environment variables:
- **PYTHONPATH**: `/opt/render/project/src`
- **STREAMLIT_SERVER_HEADLESS**: `true`
- **STREAMLIT_SERVER_ENABLE_CORS**: `false`

### Step 6: Deploy!

1. **Click "Create Web Service"**
2. **Wait for deployment** (usually 5-10 minutes)
3. **Monitor the build logs** - you'll see:
   - Installing Python dependencies
   - Building the application
   - Starting Streamlit

---

## Part 3: Verify Deployment

### Step 7: Test Your App

1. **Once deployed**, Render will show you the URL (like `https://basketball-shot-analyzer.onrender.com`)
2. **Click the URL** to open your Basketball Shot Analyzer
3. **Test key features**:
   - Upload a basketball shot video
   - Verify shot analysis works
   - Check that frame labeling displays properly
   - Test the enhanced elbow detection

### Step 8: Troubleshooting (If Needed)

**If deployment fails:**
1. **Check build logs** in Render dashboard
2. **Common issues**:
   - Missing dependencies → Check `requirements.txt`
   - Port binding errors → Verify start command uses `$PORT`
   - Memory issues → Consider upgrading to paid plan if needed

**If app loads but doesn't work:**
1. **Check application logs** in Render dashboard
2. **Test locally first** to ensure app works on localhost:8501
3. **Check file paths** - use relative paths only

---

## Part 4: Automatic Updates

### Step 9: Set Up Auto-Deploy

- **Auto-deploy is enabled by default**
- **Every push to `main` branch** will trigger a new deployment
- **To deploy manually**: Click "Manual Deploy" in Render dashboard

---

## 🎯 Your Basketball Shot Analyzer Features

Once deployed, your app will have:
- ✅ **Enhanced elbow detection** with biomechanically accurate scoring
- ✅ **Guaranteed frame labeling** for all detected flaws
- ✅ **Professional shot analysis** with detailed metrics
- ✅ **Cloud accessibility** from anywhere in the world
- ✅ **Free hosting** with HTTPS included

---

## 📊 Expected Performance

**Free Tier Limits:**
- **Bandwidth**: 100 GB/month
- **Build time**: 500 hours/month
- **Sleeps after 15 minutes** of inactivity (wakes up automatically)
- **Perfect for**: Testing, demos, personal use

**Your app URL will be**: `https://basketball-shot-analyzer.onrender.com` (or similar)

---

## 🆘 Need Help?

**If you encounter issues:**
1. **Check Render dashboard logs**
2. **Verify your GitHub repository** has all files
3. **Test locally** on http://localhost:8501 first
4. **Double-check** the start command exactly matches the one above

**Remember**: Your Basketball Shot Analyzer is already working perfectly locally - Render deployment is just making it accessible online!
