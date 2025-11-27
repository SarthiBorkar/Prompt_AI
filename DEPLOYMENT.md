# Deployment Guide

## Why Netlify Won't Work

**Netlify is NOT compatible with this application** because:

1. **Netlify is for static sites** (HTML/CSS/JS) and serverless functions
2. **This is a FastAPI backend** that requires a continuous running server with Uvicorn
3. **Netlify cannot run `python main.py api`** as a persistent web server

### The Error You Saw

The Netlify deployment failed during dependency installation because:
- The project uses Python dependencies (crewai, langchain, etc.) that require Python 3.12 or lower
- Some dependencies like `tiktoken` require Rust compilation which Netlify's build environment may not support properly
- Even if dependencies install successfully, Netlify still cannot run the FastAPI server

## 🆓 100% FREE Deployment Options

### 1. Hugging Face Spaces (BEST - Recommended for AI Apps)

**Why Hugging Face:**
- ✅ 100% FREE forever
- ✅ Never sleeps
- ✅ Perfect for AI/ML applications
- ✅ Persistent storage
- ✅ Easy deployment
- ⚠️ Repository must be public

**Steps:**
```bash
# 1. Create account at https://huggingface.co

# 2. Create new Space
# Go to https://huggingface.co/new-space
# - Name: prompt-ai-agent
# - License: MIT
# - SDK: Docker
# - Hardware: CPU (free)

# 3. Create Dockerfile in your project root
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
EOF

# 4. Push to Hugging Face
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/prompt-ai-agent
git push hf main

# 5. Add secrets (environment variables) in Space settings
# GROQ_API_KEY, PAYMENT_SERVICE_URL, etc.

# Done! Your app will be live at:
# https://YOUR_USERNAME-prompt-ai-agent.hf.space
```

### 2. Render.com (100% Free, but sleeps)

**Why Render:**
- ✅ 100% FREE
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ⚠️ Sleeps after 15 minutes of inactivity (takes ~30s to wake up)

**Steps:**
1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: prompt-ai-agent
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env` in the "Environment" section
6. Click "Create Web Service"

**Your app will be live at**: `https://prompt-ai-agent.onrender.com`

### 3. Fly.io (100% Free with generous limits)

**Why Fly.io:**
- ✅ 100% FREE tier (3 VMs, 160GB bandwidth/month)
- ✅ No sleeping
- ✅ Fast global deployment
- ⚠️ Requires credit card (for verification, won't be charged)

**Steps:**
```bash
# 1. Install flyctl
curl -L https://fly.io/install.sh | sh

# 2. Login
flyctl auth login

# 3. Create app
flyctl launch
# Answer prompts:
# - App name: prompt-ai-agent
# - Region: Choose closest to you
# - Database: No
# - Deploy now: No

# 4. Add secrets
flyctl secrets set GROQ_API_KEY=your_key
flyctl secrets set PAYMENT_SERVICE_URL=your_url
# (add all other env vars)

# 5. Deploy
flyctl deploy
```

### 4. PythonAnywhere (Free with limitations)

**Why PythonAnywhere:**
- ✅ 100% FREE
- ✅ Designed for Python apps
- ⚠️ Limited CPU seconds/day
- ⚠️ No custom domain on free tier
- ⚠️ Manual setup required

**Steps:**
1. Sign up at https://www.pythonanywhere.com
2. Go to "Web" → "Add a new web app"
3. Choose "Manual configuration" → Python 3.12
4. In Bash console:
   ```bash
   git clone https://github.com/YOUR_USERNAME/promptAI.git
   cd promptAI
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Configure WSGI file (in Web tab, click on WSGI config file):
   ```python
   import sys
   path = '/home/YOUR_USERNAME/promptAI'
   if path not in sys.path:
       sys.path.append(path)

   from main import app as application
   ```
6. Reload web app

**Your app will be at**: `https://YOUR_USERNAME.pythonanywhere.com`

---

## Other Deployment Platforms

### 1. Railway (Easiest - Limited Free)

**Why Railway:**
- Supports FastAPI/Python out of the box
- Automatic HTTPS
- Free tier available
- Simple deployment from GitHub

**Steps:**
```bash
# 1. Push to GitHub (if not already done)
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Go to https://railway.app
# 3. Click "New Project" → "Deploy from GitHub repo"
# 4. Select this repository
# 5. Add environment variables from .env
# 6. Railway will auto-detect Python and run: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 2. Render

**Why Render:**
- Similar to Railway
- Free tier with auto-sleep
- Good for APIs

**Steps:**
1. Go to https://render.com
2. New → Web Service
3. Connect your GitHub repo
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py api`
   - **Python Version**: 3.12
5. Add environment variables
6. Deploy!

### 3. Heroku

**Additional files needed:**

**Procfile**:
```
web: uvicorn main:app --host=0.0.0.0 --port=${PORT}
```

**Steps:**
```bash
# Install Heroku CLI
# Then:
heroku login
heroku create your-app-name
heroku config:set GROQ_API_KEY=your_key
# (add all other env vars)
git push heroku main
```

### 4. DigitalOcean App Platform

**Steps:**
1. Go to https://cloud.digitalocean.com/apps
2. Create App → From GitHub
3. Select this repo
4. Set build command: `pip install -r requirements.txt`
5. Set run command: `python main.py api`
6. Add environment variables
7. Deploy!

## Local Testing Before Deployment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test locally
python main.py api

# Visit http://127.0.0.1:8000/docs to test the API
```

## Environment Variables Required

All platforms need these variables:
```env
GROQ_API_KEY=your_groq_api_key
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_key
AGENT_IDENTIFIER=your_agent_identifier
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
SELLER_VKEY=your_seller_vkey
NETWORK=Preprod
```

## FREE Deployment Options Compared

| Platform | Difficulty | 100% Free? | Limitations | Best For |
|----------|-----------|------------|-------------|----------|
| **Hugging Face Spaces** | ⭐ Easy | ✅ Yes | Public repos only | AI/ML apps (BEST FOR THIS!) |
| **Render.com** | ⭐⭐ Easy | ✅ Yes | Sleeps after 15min inactive | Side projects |
| **Railway.app** | ⭐ Easy | ⚠️ $5 credit/month | Limited hours | Testing |
| **Fly.io** | ⭐⭐⭐ Medium | ✅ Yes | 3 VMs, 160GB/month | Production-ready |
| **PythonAnywhere** | ⭐⭐ Easy | ✅ Yes | Limited CPU, custom domain ❌ | Simple APIs |
| **Replit** | ⭐ Easy | ⚠️ Limited | Public code, sleeps | Quick demos |
| Heroku | ❌ | ❌ No | Ended Nov 2022 | N/A |
| Netlify | ❌ Incompatible | N/A | Static sites only | N/A |

**Recommendation: Use Hugging Face Spaces** - It's 100% free, perfect for AI apps, and doesn't sleep!
