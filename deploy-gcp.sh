#!/bin/bash

# ApexSports Basketball Shot Analyzer - Deployment Script
# Deploy to Google Cloud Run with custom domain

set -e

echo "🏀 Starting ApexSports Basketball Analyzer deployment..."

# Configuration
PROJECT_ID="your-gcp-project-id"  # Replace with your GCP project ID
SERVICE_NAME="apexsports-basketball-analyzer"
REGION="us-central1"  # Change if needed
DOMAIN="www.apexsports-llc.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud CLI not found. Please install Google Cloud CLI first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    print_error "Not authenticated with gcloud. Please run: gcloud auth login"
    exit 1
fi

print_status "Setting up project configuration..."

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
print_status "Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy
print_status "Building Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME:latest

print_status "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --concurrency 80 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 1 \
    --port 8080

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

print_status "Service deployed successfully!"
print_status "Service URL: $SERVICE_URL"

# Domain mapping instructions
print_warning "To complete custom domain setup:"
print_warning "1. Go to Google Cloud Console -> Cloud Run -> Manage Custom Domains"
print_warning "2. Add domain mapping for: $DOMAIN"
print_warning "3. Update your DNS settings with the provided CNAME records"
print_warning "4. Or use Vercel DNS to point $DOMAIN to $SERVICE_URL"

echo ""
print_status "🚀 Deployment complete! Your Basketball Shot Analyzer is live!"
print_status "Service URL: $SERVICE_URL"

# Save deployment info
echo "DEPLOYMENT_INFO:" > deployment-info.txt
echo "Service Name: $SERVICE_NAME" >> deployment-info.txt
echo "Project ID: $PROJECT_ID" >> deployment-info.txt
echo "Region: $REGION" >> deployment-info.txt
echo "Service URL: $SERVICE_URL" >> deployment-info.txt
echo "Deployed: $(date)" >> deployment-info.txt

print_status "Deployment information saved to deployment-info.txt"
