# Basketball Shot Analyzer - Heroku Deployment Script
# Run this script to deploy to Heroku

Write-Host "=== Basketball Shot Analyzer - Heroku Deployment ===" -ForegroundColor Green

# Check if Heroku CLI is installed
Write-Host "Checking Heroku CLI..." -ForegroundColor Yellow
try {
    heroku --version
    Write-Host "✓ Heroku CLI found" -ForegroundColor Green
} catch {
    Write-Host "✗ Heroku CLI not found. Please install from: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Red
    exit 1
}

# Set up Heroku-specific files
Write-Host "Setting up Heroku configuration files..." -ForegroundColor Yellow
Copy-Item "Procfile_heroku" "Procfile" -Force
Copy-Item "runtime_heroku.txt" "runtime.txt" -Force
Copy-Item "requirements_heroku.txt" "requirements.txt" -Force
Write-Host "✓ Heroku configuration files ready" -ForegroundColor Green

# Create Heroku app (with random suffix to avoid conflicts)
$appName = "basketball-shot-analyzer-$(Get-Random -Minimum 1000 -Maximum 9999)"
Write-Host "Creating Heroku app: $appName" -ForegroundColor Yellow
heroku create $appName

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Heroku app created: $appName" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create Heroku app" -ForegroundColor Red
    exit 1
}

# Configure Heroku environment
Write-Host "Configuring Heroku environment..." -ForegroundColor Yellow
heroku config:set PYTHONPATH=/app -a $appName
heroku config:set STREAMLIT_SERVER_HEADLESS=true -a $appName
heroku stack:set heroku-22 -a $appName
Write-Host "✓ Heroku environment configured" -ForegroundColor Green

# Add git remote if it doesn't exist
Write-Host "Setting up git remote..." -ForegroundColor Yellow
git remote remove heroku 2>$null
heroku git:remote -a $appName
Write-Host "✓ Git remote configured" -ForegroundColor Green

# Commit Heroku files
Write-Host "Committing Heroku configuration..." -ForegroundColor Yellow
git add Procfile runtime.txt requirements.txt
git commit -m "feat: Add Heroku deployment configuration for $appName"

# Deploy to Heroku
Write-Host "Deploying to Heroku..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Cyan
git push heroku main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Deployment successful!" -ForegroundColor Green
    Write-Host "Your app is available at: https://$appName.herokuapp.com" -ForegroundColor Cyan
    
    # Open the app
    Write-Host "Opening app in browser..." -ForegroundColor Yellow
    heroku open -a $appName
} else {
    Write-Host "✗ Deployment failed" -ForegroundColor Red
    Write-Host "Check logs with: heroku logs --tail -a $appName" -ForegroundColor Yellow
    exit 1
}

Write-Host "=== Deployment Complete ===" -ForegroundColor Green
Write-Host "App URL: https://$appName.herokuapp.com" -ForegroundColor Cyan
Write-Host "Logs: heroku logs --tail -a $appName" -ForegroundColor Cyan
Write-Host "Dashboard: heroku open -a $appName" -ForegroundColor Cyan
