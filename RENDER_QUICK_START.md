# Basketball Shot Analyzer - Render.com Deployment (Updated)

## 🎯 ACTUAL Steps for Current Render.com Interface

### Step 1: Sign Up/Login
1. Go to: **https://render.com/**
2. Click **"Get Started for Free"** or **"Sign In"**
3. Choose **"Sign in with GitHub"**
4. Authorize Render to access your repositories

### Step 2: Create New Web Service
1. After login, you'll see the dashboard
2. Click **"New +"** button (top right)
3. Select **"Web Service"** from the dropdown
4. You'll see "Create a new Web Service" page

### Step 3: Connect Repository
1. **Select source**: Choose **"Build and deploy from a Git repository"**
2. **Connect GitHub account** (if not already connected)
3. **Find your repository**: Look for `apexsports-basketball-analyzer`
4. Click **"Connect"** next to your repository

### Step 4: Configure Service (Exact Form Fields)

**Repository & Branch:**
- **Repository**: `rickdyer20/apexsports-basketball-analyzer` (auto-filled)
- **Branch**: `main` (should be selected by default)

**Service Configuration:**
- **Name**: `basketball-shot-analyzer` (you can customize this)
- **Root Directory**: Leave blank (empty field)
- **Environment**: `Python 3` (select from dropdown)
- **Region**: `Ohio (US East)` or `Oregon (US West)` (your choice)

**Build & Deploy Commands:**
- **Build Command**: 
```
pip install -r requirements.txt
```
- **Start Command**: 
```
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

**Pricing Plan:**
- **Instance Type**: Select **"Free"** (should show: "$0/month")

### Step 5: Optional - Environment Variables
Click **"Advanced"** if you want to add environment variables:
- `STREAMLIT_SERVER_HEADLESS` = `true`
- `PYTHONPATH` = `/opt/render/project/src`

### Step 6: Deploy
1. **Review your settings**
2. Click **"Create Web Service"** (bottom of form)
3. **Wait for deployment** (5-15 minutes)
4. **Watch the build logs** in real-time

---

## 🎉 Your App Will Be Live!

**URL Format**: `https://basketball-shot-analyzer-XXXX.onrender.com`

**What to expect:**
- Build takes 5-15 minutes
- First load after sleep takes ~30-60 seconds
- Automatic deployments on every GitHub push

---

## 🔧 If Render Auto-Detects Wrong Settings

If Render tries to auto-detect your app and fills in wrong values:
1. **Override the Build Command** with: `pip install -r requirements.txt`
2. **Override the Start Command** with: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
3. **Make sure Environment** is set to `Python 3`

---

## 🆘 Troubleshooting

**Common Issues:**
- **Wrong Python version detected**: Change Environment to "Python 3"
- **Build fails**: Check that requirements.txt exists in your repo root
- **App doesn't start**: Verify the start command exactly matches above
- **Port errors**: Make sure start command includes `--server.port=$PORT`
