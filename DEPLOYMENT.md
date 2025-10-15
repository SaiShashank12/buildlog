# BuildLog Deployment Guide

## Prerequisites

- GitHub repository: https://github.com/SaiShashank12/buildlog
- Appwrite instance running (currently: https://nyc.cloud.appwrite.io)
- Environment variables from `.env` file

## Required Environment Variables

```
APPWRITE_ENDPOINT=https://nyc.cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=your_database_id
APPWRITE_PROJECTS_COLLECTION_ID=your_projects_collection_id
APPWRITE_BUILD_LOGS_COLLECTION_ID=your_build_logs_collection_id
APPWRITE_STORAGE_BUCKET_ID=your_storage_bucket_id
OPENAI_API_KEY=your_openai_key
OPENAI_ENABLED=true
```

---

## Option 1: Railway (Recommended - Easiest)

### Why Railway?
- $5/month free credit
- Automatic GitHub deployment
- Zero config for Python apps
- Built-in environment variables
- Perfect for FastAPI + Appwrite

### Deployment Steps

1. **Sign up at railway.app**
   - Connect your GitHub account

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `SaiShashank12/buildlog`

3. **Configure Environment Variables**
   - Go to Variables tab
   - Add all environment variables from `.env`

4. **Deploy**
   - Railway auto-detects `requirements.txt`
   - Automatically installs dependencies
   - Runs: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Get Your URL**
   - Railway provides: `https://your-app.railway.app`

### Cost
- Free: $5 credit/month (~500 hours)
- Paid: $5/month for unlimited

---

## Option 2: Render (Best Free Tier)

### Why Render?
- Completely free tier (with sleep after inactivity)
- Easy Python deployment
- Good for hackathon demos
- Custom domains on free tier

### Deployment Steps

1. **Sign up at render.com**
   - Connect GitHub account

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect `SaiShashank12/buildlog`

3. **Configure Build Settings**
   - Name: `buildlog`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   - Go to "Environment" tab
   - Add all variables from `.env`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

6. **Get Your URL**
   - Render provides: `https://buildlog.onrender.com`

### Free Tier Limitations
- App sleeps after 15 minutes of inactivity
- Cold start takes 30-60 seconds
- 750 hours/month free

---

## Option 3: Fly.io (Container-based, Global Edge)

### Why Fly.io?
- Generous free tier (3 VMs with 256MB RAM)
- Global edge deployment
- Runs Docker containers
- Fast cold starts

### Required Files (already created below)

1. `Dockerfile` - Container configuration
2. `fly.toml` - Fly.io configuration

### Deployment Steps

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up and authenticate**
   ```bash
   fly auth signup
   # or
   fly auth login
   ```

3. **Launch app (from project root)**
   ```bash
   fly launch
   ```
   - Choose app name: `buildlog-[your-name]`
   - Select region: Choose closest to users
   - Don't deploy yet (we need to set env vars)

4. **Set environment variables**
   ```bash
   fly secrets set APPWRITE_ENDPOINT=https://nyc.cloud.appwrite.io/v1
   fly secrets set APPWRITE_PROJECT_ID=your_project_id
   fly secrets set APPWRITE_API_KEY=your_api_key
   fly secrets set APPWRITE_DATABASE_ID=your_database_id
   fly secrets set APPWRITE_PROJECTS_COLLECTION_ID=your_projects_collection_id
   fly secrets set APPWRITE_BUILD_LOGS_COLLECTION_ID=your_build_logs_collection_id
   fly secrets set APPWRITE_STORAGE_BUCKET_ID=your_storage_bucket_id
   fly secrets set OPENAI_API_KEY=your_openai_key
   fly secrets set OPENAI_ENABLED=true
   ```

5. **Deploy**
   ```bash
   fly deploy
   ```

6. **Get Your URL**
   - Fly provides: `https://buildlog-yourname.fly.dev`

7. **View logs**
   ```bash
   fly logs
   ```

### Free Tier
- Up to 3 shared-cpu-1x VMs with 256MB RAM
- 160GB outbound data transfer
- Perfect for hackathon projects

---

## Deployment Files Needed for Fly.io

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### fly.toml
```toml
app = "buildlog"
primary_region = "ewr"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

---

## Quick Comparison

| Feature | Railway | Render | Fly.io |
|---------|---------|--------|--------|
| Free Tier | $5 credit/month | 750 hrs/month | 3 VMs always-on |
| Setup Difficulty | Easiest | Easy | Medium |
| Cold Starts | No | Yes (slow) | Yes (fast) |
| Custom Domain | Yes | Yes | Yes |
| Best For | Quick deploy | Hackathons | Production-ready |

---

## Recommendation

**For Hackathon Submission: Use Railway**
- Fastest deployment (2 minutes)
- No cold starts
- Works perfectly with Appwrite
- $5 credit lasts entire hackathon

**For Long-term Free: Use Fly.io**
- Always-on free tier
- Fast performance
- Global edge network

**For Demo: Use Render**
- Completely free
- Good enough for demos
- Just warn users about cold starts

---

## Post-Deployment Checklist

- [ ] Test signup/login flow
- [ ] Verify Appwrite connection
- [ ] Create a test project
- [ ] Add a test build log
- [ ] Check analytics page
- [ ] Test AI features (if OpenAI key is set)
- [ ] Verify dark mode works
- [ ] Test status changes
- [ ] Check mobile responsiveness

---

## Troubleshooting

### App won't start
- Check environment variables are set correctly
- Verify Appwrite credentials
- Check logs for errors

### 401 Unauthorized errors
- Verify APPWRITE_API_KEY is correct
- Check APPWRITE_PROJECT_ID matches your Appwrite project
- Ensure Appwrite endpoint is accessible

### Static files not loading
- Check that `app/templates` and `app/static` are deployed
- Verify paths in template mounting (main.py line ~50)

### Sessions not persisting
- Ensure cookies are enabled
- Check HTTPS is enabled (required for secure cookies)
- Verify session token format matches Appwrite requirements

---

## Current Status

✅ Code pushed to GitHub: https://github.com/SaiShashank12/buildlog
✅ Latest PR merged: Authentication + Project Status
✅ Main branch up to date
✅ Ready to deploy

**Next Steps:**
1. Choose deployment platform (Railway recommended)
2. Create account and connect GitHub
3. Add environment variables
4. Deploy and test
5. Share demo link for hackathon submission
