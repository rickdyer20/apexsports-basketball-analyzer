# ApexSports Basketball Shot Analyzer - Windows Deployment Script
# Deploy to Google Cloud Run

param(
    [string]$ProjectId = "",
    [string]$Region = "us-central1",
    [string]$ServiceName = "apexsports-basketball-analyzer",
    [string]$Domain = "www.apexsports-llc.com"
)

Write-Host "🏀 Starting ApexSports Basketball Analyzer deployment..." -ForegroundColor Green

# Check if project ID is provided
if (-not $ProjectId) {
    $ProjectId = Read-Host "Enter your Google Cloud Project ID"
}

# Set project
Write-Host "Setting up project: $ProjectId" -ForegroundColor Yellow
gcloud config set project $ProjectId

# Enable required APIs
Write-Host "Enabling required Google Cloud APIs..." -ForegroundColor Yellow
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy
Write-Host "Building Docker image..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$ProjectId/$ServiceName`:latest"

Write-Host "Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $ServiceName `
    --image "gcr.io/$ProjectId/$ServiceName`:latest" `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 2 `
    --concurrency 80 `
    --timeout 300 `
    --max-instances 10 `
    --min-instances 1 `
    --port 8080

# Get service URL
$ServiceUrl = gcloud run services describe $ServiceName --platform managed --region $Region --format 'value(status.url)'

Write-Host "🚀 Deployment complete!" -ForegroundColor Green
Write-Host "Service URL: $ServiceUrl" -ForegroundColor Cyan

Write-Host ""
Write-Host "To complete custom domain setup:" -ForegroundColor Yellow
Write-Host "1. Go to Google Cloud Console -> Cloud Run -> Manage Custom Domains"
Write-Host "2. Add domain mapping for: $Domain"
Write-Host "3. Update your DNS settings with the provided CNAME records"
Write-Host "4. Or use Vercel DNS to point $Domain to $ServiceUrl"

# Save deployment info
$DeployInfo = @"
DEPLOYMENT_INFO:
Service Name: $ServiceName
Project ID: $ProjectId
Region: $Region
Service URL: $ServiceUrl
Deployed: $(Get-Date)
"@

$DeployInfo | Out-File -FilePath "deployment-info.txt"
Write-Host "Deployment information saved to deployment-info.txt" -ForegroundColor Green
