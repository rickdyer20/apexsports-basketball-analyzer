# EXACT Render.com Form Fields - Basketball Shot Analyzer

## 🎯 Copy and Paste These Values Into Render Form

When you get to the "Create a new Web Service" form on Render, fill in exactly:

---

### Repository Section
- **Repository**: `rickdyer20/apexsports-basketball-analyzer` *(auto-filled)*
- **Branch**: `main` *(should be pre-selected)*

---

### Service Details Section
```
Name: basketball-shot-analyzer
Root Directory: [leave blank]
Environment: Python 3
Region: Ohio (US East) or Oregon (US West)
```

---

### Build & Deploy Section
```
Build Command: pip install -r requirements.txt

Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

---

### Plan Section
```
Instance Type: Free ($0/month)
```

---

## 🚀 Then Click "Create Web Service"

**That's it!** The deployment will start automatically.

---

## ⏱️ What Happens Next
1. **Build starts** (you'll see logs in real-time)
2. **Installation of Python packages** (5-10 minutes)
3. **App starts up** on Render's servers
4. **You get a live URL** like: `https://basketball-shot-analyzer-XXXX.onrender.com`

---

## 🔧 If Something Goes Wrong

**Most common issue**: Render auto-detects wrong settings
- **Solution**: Override the Build and Start commands with the exact ones above
- **Check**: Environment is set to "Python 3" (not Node.js or other)

**Your app works locally, so it will work on Render too!** 🎯
