# Basketball Shot Analyzer - Heroku Deployment Guide

## Prerequisites
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Create a Heroku account: https://signup.heroku.com/

## Deployment Steps

### 1. Login to Heroku
```bash
heroku login
```

### 2. Create Heroku App
```bash
heroku create basketball-shot-analyzer-app
```

### 3. Set up Heroku-specific files
```bash
# Copy Heroku-specific files
copy Procfile_heroku Procfile
copy runtime_heroku.txt runtime.txt
copy requirements_heroku.txt requirements.txt
```

### 4. Configure Heroku
```bash
# Set stack to latest
heroku stack:set heroku-22 -a basketball-shot-analyzer-app

# Configure environment variables
heroku config:set PYTHONPATH=/app -a basketball-shot-analyzer-app
heroku config:set STREAMLIT_SERVER_HEADLESS=true -a basketball-shot-analyzer-app
```

### 5. Deploy to Heroku
```bash
# Add and commit Heroku files
git add .
git commit -m "feat: Add Heroku deployment configuration"

# Deploy to Heroku
git push heroku main
```

### 6. Open the App
```bash
heroku open -a basketball-shot-analyzer-app
```

## Troubleshooting

### Check logs
```bash
heroku logs --tail -a basketball-shot-analyzer-app
```

### Restart app
```bash
heroku restart -a basketball-shot-analyzer-app
```

### Scale dynos
```bash
heroku ps:scale web=1 -a basketball-shot-analyzer-app
```
