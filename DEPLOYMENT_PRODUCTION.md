# 🏀 ApexSports Basketball Analyzer - Deployment Guide

Deploy your Basketball Shot Analyzer to www.apexsports-llc.com using Google Cloud Run with Vercel DNS.

## 📋 Prerequisites

1. **Google Cloud CLI** installed and authenticated
2. **Vercel CLI** (optional, for domain management)
3. **Docker** (optional, for local testing)
4. **Google Cloud Project** with billing enabled

## 🚀 Deployment Steps

### Step 1: Setup Google Cloud Project

```bash
# Install Google Cloud CLI if not already installed
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Create or select project
gcloud projects create your-apexsports-project --name="ApexSports LLC"
gcloud config set project your-apexsports-project

# Enable billing (required for Cloud Run)
# Go to https://console.cloud.google.com/billing
```

### Step 2: Configure Deployment

1. Edit `deploy-gcp.sh` and update:
   ```bash
   PROJECT_ID="your-gcp-project-id"  # Your actual project ID
   REGION="us-central1"              # Choose your preferred region
   DOMAIN="www.apexsports-llc.com"   # Your domain
   ```

### Step 3: Deploy to Google Cloud Run

```bash
# Make deploy script executable (Linux/Mac)
chmod +x deploy-gcp.sh

# Run deployment
./deploy-gcp.sh

# Or run manually on Windows:
bash deploy-gcp.sh
```

### Step 4: Custom Domain Setup with Namecheap

#### Option A: Direct DNS (Simplest)
1. Deploy to Cloud Run and get your service URL
2. In Namecheap Dashboard → Domain List → Manage → Advanced DNS
3. Add CNAME record:
   ```
   Type: CNAME
   Host: www
   Value: your-service-url.run.app (without https://)
   TTL: Automatic
   ```
4. Optional: Add A record for apex domain (@ host)

#### Option B: Cloudflare DNS (Recommended)
1. Add domain to Cloudflare (free plan)
2. Update nameservers in Namecheap to Cloudflare's
3. In Cloudflare DNS:
   ```
   Type: CNAME
   Name: www
   Target: your-service-url.run.app
   Proxy: Enabled (orange cloud)
   ```
4. Benefits: Free SSL, CDN, caching, DDoS protection

#### Option C: Vercel Proxy
1. Update `vercel.json` with your Cloud Run URL
2. Deploy to Vercel: `vercel --prod`
3. In Namecheap DNS, point to Vercel:
   ```
   Type: CNAME
   Host: www
   Value: cname.vercel-dns.com
   ```

## 🔧 Configuration Options

### Environment Variables
Add these in Cloud Run if needed:
- `PYTHONUNBUFFERED=1`
- `PORT=8080`

### Resource Limits
Current configuration:
- **Memory**: 2GB
- **CPU**: 2 cores
- **Concurrency**: 80 requests
- **Timeout**: 5 minutes
- **Min Instances**: 1 (always warm)
- **Max Instances**: 10

## 🔍 Monitoring & Debugging

### Check Deployment Status
```bash
gcloud run services describe apexsports-basketball-analyzer --region=us-central1
```

### View Logs
```bash
gcloud logs read --service=apexsports-basketball-analyzer --limit=50
```

### Test Service
```bash
curl https://your-service-url.run.app/_stcore/health
```

## 💰 Cost Estimates

**Google Cloud Run Pricing** (approximate):
- Free tier: 2 million requests/month
- After free tier: ~$0.40 per million requests
- Memory: ~$0.0000025 per GB-second
- CPU: ~$0.0000024 per vCPU-second

**Typical monthly cost for moderate usage**: $10-50

## 🛠️ Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check build logs
   gcloud builds log $(gcloud builds list --limit=1 --format="value(id)")
   ```

2. **Service Won't Start**
   - Check logs: `gcloud logs read --service=apexsports-basketball-analyzer`
   - Verify port 8080 in Dockerfile
   - Check health endpoint: `/_stcore/health`

3. **Domain Issues**
   - Verify DNS propagation: `dig www.apexsports-llc.com`
   - Check SSL certificate status in Cloud Console
   - Allow 15+ minutes for DNS propagation

### Performance Optimization

1. **Cold Starts**: Min instances set to 1 (reduces cold starts)
2. **Memory**: 2GB allocated for video processing
3. **CPU**: 2 cores for MediaPipe analysis
4. **Concurrency**: 80 concurrent users supported

## 📱 Testing

1. **Local Testing**:
   ```bash
   streamlit run app.py --server.port 8502
   ```

2. **Docker Testing**:
   ```bash
   docker build -t apexsports-test .
   docker run -p 8080:8080 apexsports-test
   ```

3. **Production Testing**:
   - Upload test video
   - Check analysis results
   - Test download functionality
   - Verify mobile responsiveness

## 🔐 Security

- HTTPS enforced automatically
- CORS configured for web access
- No authentication required (public app)
- Frame protection enabled
- Content type sniffing disabled

## 📊 Analytics

Consider adding:
- Google Analytics
- Cloud Monitoring dashboards
- Error reporting
- Performance monitoring

## 🔄 Updates

To update the deployment:
```bash
# Run deployment script again
./deploy-gcp.sh
```

The service will automatically rollout the new version with zero downtime.

---

## 🎯 Quick Start Commands

```bash
# 1. Set your project ID
export PROJECT_ID="your-gcp-project-id"

# 2. Deploy
./deploy-gcp.sh

# 3. Check status
gcloud run services list

# 4. View your app
open https://your-service-url.run.app
```

Your Basketball Shot Analyzer will be live at www.apexsports-llc.com! 🏀
