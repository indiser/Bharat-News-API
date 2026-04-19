# 🚀 Deployment Protocol

## Prerequisites

- [ ] GitHub repository with clean code pushed
- [ ] Neon PostgreSQL database created
- [ ] Vercel account created
- [ ] Database seeded with `python seed.py`

---

## Step 1: Vercel Deployment

### 1.1 Import Repository

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Select your GitHub repository: `Bharat-News-Api`
4. Click **"Import"**

### 1.2 Configure Build Settings

**DO NOT click Deploy yet!**

- **Framework Preset**: `Other`
- **Root Directory**: `./`
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)

### 1.3 Add Environment Variables

Click **"Environment Variables"** dropdown and add:

| Key | Value | Example |
|-----|-------|---------|
| `DATABASE_URL` | Your Neon connection string | `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/bharatnews?sslmode=require` |
| `CRON_SECRET` | Custom secure password | `my_super_secret_key_2026` |

**Important Notes:**
- Copy your exact Neon connection string (includes `?sslmode=require`)
- Generate a strong `CRON_SECRET` (save it for Step 2)
- Both variables apply to: **Production**, **Preview**, and **Development**

### 1.4 Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for build completion
3. Copy your live URL (e.g., `https://bharat-news-api.vercel.app`)
4. Test endpoint: `https://your-url.vercel.app/api/news`

---

## Step 2: GitHub Actions Setup

### 2.1 Navigate to Repository Secrets

1. Go to your GitHub repository
2. Click **Settings** (top menu)
3. Expand **Secrets and variables** → Click **Actions**

### 2.2 Add Repository Secrets

Click **"New repository secret"** for each:

#### Secret 1: API_URL
- **Name**: `API_URL`
- **Value**: `https://your-vercel-url.vercel.app`
- **Example**: `https://bharat-news-api.vercel.app`
- ⚠️ **No trailing slash!**

#### Secret 2: CRON_SECRET
- **Name**: `CRON_SECRET`
- **Value**: (Same password you set in Vercel)
- **Example**: `my_super_secret_key_2026`
- ⚠️ **Must match Vercel exactly!**

### 2.3 Verify Secrets

Your Actions secrets page should show:
```
API_URL         Updated X seconds ago
CRON_SECRET     Updated X seconds ago
```

---

## Step 3: Verify Automation

### 3.1 Manual Trigger Test

1. Go to **Actions** tab in GitHub
2. Click **"Hourly News Fetcher"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 30-60 seconds
5. Check run status (should be green ✓)

### 3.2 Check Logs

Click on the workflow run to see:
```
✓ Checkout code
✓ Trigger Vercel cron endpoint
✓ Response: {"status":"success","message":"Database updated"}
```

### 3.3 Verify Database

Test your API endpoint:
```bash
curl https://your-vercel-url.vercel.app/api/news
```

Should return JSON with news data.

---

## Step 4: Automatic Hourly Updates

GitHub Actions will now automatically:
- Run every hour at `:00` (e.g., 1:00, 2:00, 3:00)
- Call `https://your-url.vercel.app/api/cron/update`
- Refresh database with latest news

**No further action required!**

---

## 🔍 Troubleshooting

### Issue: Vercel deployment fails
**Solution**: Check `requirements.txt` has all dependencies

### Issue: GitHub Actions returns 401 Unauthorized
**Solution**: Verify `CRON_SECRET` matches in both Vercel and GitHub

### Issue: GitHub Actions returns 404
**Solution**: Check `API_URL` has no trailing slash and is correct

### Issue: Database not updating
**Solution**: 
1. Check Vercel logs: `vercel logs <deployment-url>`
2. Verify `DATABASE_URL` is correct
3. Ensure database was seeded with `python seed.py`

---

## ✅ Deployment Checklist

- [ ] Vercel deployment successful
- [ ] Environment variables added to Vercel
- [ ] GitHub Actions secrets configured
- [ ] Manual workflow test passed
- [ ] API endpoint returns data
- [ ] Hourly automation verified (wait 1 hour)

---

## 📝 Quick Reference

| Service | URL |
|---------|-----|
| Vercel Dashboard | https://vercel.com/dashboard |
| GitHub Actions | https://github.com/YOUR_USERNAME/Bharat-News-Api/actions |
| API Docs | https://your-url.vercel.app/docs |
| Live API | https://your-url.vercel.app/api/news |

---

**🎉 Deployment Complete!**

Your Bharat News API is now live and auto-updating every hour.
