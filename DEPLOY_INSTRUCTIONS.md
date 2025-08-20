# 🚀 Deploy Basketball Shot Analyzer to www.apexsports-llc.com

## Quick Start Deployment

### Option 1: Streamlit Community Cloud (Easiest - FREE)

1. **Upload to GitHub**:
   ```bash
   # Create new repository at github.com named: apexsports-basketball-analyzer
   # Then run these commands (replace YOUR_USERNAME):
   
   git remote set-url origin https://github.com/YOUR_USERNAME/apexsports-basketball-analyzer.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository: `apexsports-basketball-analyzer`
   - Main file path: `app.py`
   - Click "Deploy"
   - Your app will be live at: `https://YOUR_USERNAME-apexsports-basketball-analyzer.streamlit.app`

3. **Point Your Domain**:
   - In Namecheap, add CNAME record:
     - Host: `www`
     - Value: `YOUR_USERNAME-apexsports-basketball-analyzer.streamlit.app`
   - Add A record:
     - Host: `@`
     - Value: Use Cloudflare proxy or redirect to www

### Option 2: Vercel (More Professional)

1. **Setup Vercel Account**:
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub
   - Install Vercel CLI: `npm install -g vercel`

2. **Deploy Project**:
   ```bash
   vercel login
   vercel --prod
   ```

3. **Configure Domain**:
   - In Vercel dashboard, go to your project
   - Add domain: `www.apexsports-llc.com`
   - Follow DNS instructions for Namecheap

### Option 3: Google Cloud Run (Full Production)

**Prerequisites**:
- Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

**Deployment**:
```bash
# Build and deploy
docker build -t basketball-analyzer .
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/basketball-analyzer
gcloud run deploy basketball-analyzer --image gcr.io/YOUR_PROJECT_ID/basketball-analyzer --platform managed --region us-central1 --allow-unauthenticated
```

## 🌐 Domain Configuration (Namecheap + Cloudflare)

### Setup Cloudflare (Recommended)

1. **Add Site to Cloudflare**:
   - Go to [cloudflare.com](https://cloudflare.com)
   - Add `apexsports-llc.com`
   - Copy the Cloudflare nameservers

2. **Update Namecheap DNS**:
   - In Namecheap dashboard, go to Domain List
   - Click "Manage" next to apexsports-llc.com
   - Go to "Nameservers" section
   - Select "Custom DNS"
   - Enter Cloudflare nameservers:
     - `vera.ns.cloudflare.com`
     - `walt.ns.cloudflare.com`

3. **Configure DNS in Cloudflare**:
   ```
   Type: A     Name: @     Content: [Your app IP]     Proxy: ON
   Type: CNAME Name: www   Content: @                 Proxy: ON
   ```

### Direct Namecheap Configuration (Alternative)

If you prefer to stay with Namecheap DNS:

1. **Go to Advanced DNS in Namecheap**
2. **Add Records**:
   ```
   Type: A Record     Host: @     Value: [Your app IP]
   Type: CNAME       Host: www   Value: [Your app domain]
   ```

## 📊 Monitoring & Updates

- **Streamlit**: Automatic deploys on GitHub push
- **Vercel**: Automatic deploys with preview URLs
- **Google Cloud**: Manual deploys, full control

## 🆘 Troubleshooting

### Common Issues:
1. **Dependencies**: Make sure `requirements.txt` is complete
2. **Ports**: Streamlit Cloud uses port 8501 automatically
3. **File Paths**: Use relative paths in your code
4. **Memory**: Large video files might need optimization

### Support:
- Streamlit: [docs.streamlit.io](https://docs.streamlit.io)
- Vercel: [vercel.com/docs](https://vercel.com/docs)
- Google Cloud: [cloud.google.com/run/docs](https://cloud.google.com/run/docs)

## 🎯 Next Steps

1. Choose your deployment method (Streamlit Cloud recommended for simplicity)
2. Upload code to GitHub
3. Deploy application
4. Configure domain DNS
5. Test your live site at www.apexsports-llc.com

Your Basketball Shot Analyzer will be live and professional! 🏀✨
