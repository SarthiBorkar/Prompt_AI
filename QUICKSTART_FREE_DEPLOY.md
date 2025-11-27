# Quick Start: Free Deployment in 5 Minutes

## Option 1: Hugging Face Spaces (Recommended - Never Sleeps)

### Step 1: Create Account
- Go to https://huggingface.co
- Sign up (free)

### Step 2: Create New Space
- Click your profile → "New Space"
- Name: `prompt-ai-agent`
- License: MIT
- SDK: **Docker** (important!)
- Hardware: CPU basic (free)
- Click "Create Space"

### Step 3: Deploy
```bash
# Add Hugging Face as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/prompt-ai-agent

# Push code (Dockerfile already included)
git push hf main
```

### Step 4: Add Environment Variables
- In your Space, go to Settings → Variables and secrets
- Add these secrets:
  - `GROQ_API_KEY` = your Groq API key
  - `PAYMENT_SERVICE_URL` = http://localhost:3001/api/v1
  - `PAYMENT_API_KEY` = your payment key
  - `NETWORK` = Preprod
  - (add others from your `.env`)

### Step 5: Done!
Your app will be live at: `https://YOUR_USERNAME-prompt-ai-agent.hf.space`

Visit `/docs` to test the API.

---

## Option 2: Render.com (Easier Setup, but Sleeps After 15min)

### Step 1: Sign Up
- Go to https://render.com
- Sign up with GitHub

### Step 2: Create Web Service
- Click "New +" → "Web Service"
- Connect this repository
- Click "Connect"

### Step 3: Configure
```
Name: prompt-ai-agent
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 4: Add Environment Variables
In the "Environment" section, add:
- `GROQ_API_KEY`
- `PAYMENT_SERVICE_URL`
- `NETWORK`
- (all variables from your `.env`)

### Step 5: Deploy
Click "Create Web Service"

Your app will be at: `https://prompt-ai-agent.onrender.com`

**Note**: Sleeps after 15 minutes of inactivity. First request takes ~30s to wake up.

---

## Comparison

| Feature | Hugging Face | Render |
|---------|--------------|--------|
| Always On | ✅ Yes | ❌ Sleeps after 15min |
| Setup Difficulty | Medium | Easy |
| Deployment | Git push | Auto from GitHub |
| Custom Domain | ❌ | ✅ |
| Best For | AI apps, APIs | Hobby projects |

## Troubleshooting

### Hugging Face: Build Failed
- Check Dockerfile exists
- Ensure `requirements.txt` is committed
- Check build logs in Space settings

### Render: Service Won't Start
- Verify start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Check environment variables are set
- View logs in Render dashboard

### Both: Application Error
- Verify all environment variables from `.env` are added
- Check `GROQ_API_KEY` is valid
- Test locally first: `python main.py api`

## Need Help?

1. Check full deployment guide: `DEPLOYMENT.md`
2. Test locally first to ensure app works
3. Check platform-specific logs for errors

**Recommended**: Start with Hugging Face Spaces for AI/ML apps - it's free and never sleeps!
