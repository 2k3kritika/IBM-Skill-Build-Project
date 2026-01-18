# Deployment Guide: Vercel (Frontend) + Render (Backend)

This guide provides step-by-step instructions for deploying the AI-Powered Burnout Detection application to production:
- **Frontend**: Deploy React app to Vercel
- **Backend**: Deploy FastAPI app to Render
- **Database**: Use Supabase (already configured)

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Deployment on Render](#backend-deployment-on-render)
3. [Frontend Deployment on Vercel](#frontend-deployment-on-vercel)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Testing the Deployment](#testing-the-deployment)
6. [Troubleshooting](#troubleshooting)
7. [Updating Your Deployment](#updating-your-deployment)

---

## ✅ Prerequisites

Before deploying, ensure you have:

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com) (free tier available)
3. **Render Account** - Sign up at [render.com](https://render.com) (free tier available)
4. **Supabase Project** - Already set up (see [SUPABASE_DEPLOYMENT.md](SUPABASE_DEPLOYMENT.md))
5. **Google Gemini API Key** - Already obtained

---

## 🚀 Backend Deployment on Render

### Step 1: Prepare Your Backend for Deployment

#### 1.1 Create `render.yaml` Configuration (Optional but Recommended)

Create a `render.yaml` file in the `backend` directory:

```yaml
services:
  - type: web
    name: burnout-detection-api
    env: python
    pythonVersion: "3.11.0"
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: GOOGLE_GEMINI_API_KEY
        sync: false
      - key: GEMINI_MODEL_NAME
        value: gemini-pro
      - key: ALLOWED_ORIGINS
        sync: false
```

**Important Notes:**
- `pythonVersion: "3.11.0"` explicitly sets Python version (prevents Render from using Python 3.13)
- Build command upgrades pip first to avoid compatibility issues
- Uses `psycopg2-binary` in requirements.txt (not `psycopg`)

#### 1.2 Create `Procfile` (Alternative Method)

If not using `render.yaml`, create a `Procfile` in the `backend` directory:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### 1.3 Create `runtime.txt` (Optional)

Create `runtime.txt` in the `backend` directory to specify Python version:

```
python-3.11.0
```

### Step 2: Push Code to GitHub

Make sure your code is committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 3: Create Render Web Service

1. **Go to Render Dashboard**
   - Visit [render.com](https://render.com)
   - Sign in or create an account

2. **Create New Web Service**
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub account if not already connected
   - Select your repository (`IBM_skill_project`)

3. **Configure Service Settings**
   
   **Basic Settings:**
   - **Name**: `burnout-detection-api` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Python Version**: `3.11.0` (⚠️ **CRITICAL**: Set this explicitly in the dashboard!)
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   
   **⚠️ IMPORTANT**: 
   - **You MUST set Python Version to `3.11.0`** in the Render dashboard settings
   - Render may default to Python 3.13, which causes build failures with `pydantic-core`
   - Look for "Python Version" dropdown in the service settings
   - If you don't see it, go to **Settings** → **Environment** → Add `PYTHON_VERSION=3.11.0`

4. **Configure Environment Variables**
   
   Click **"Advanced"** → **"Add Environment Variable"** and add:
   
   ```
   DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
   GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL_NAME=gemini-pro
   PYTHON_VERSION=3.11.0
   ```
   
   **Important**: Replace with your actual values:
   - `DATABASE_URL`: Your Supabase connection string
   - `GOOGLE_GEMINI_API_KEY`: Your actual Gemini API key

5. **Deploy**
   - Click **"Create Web Service"**
   - Render will start building and deploying your backend
   - Wait for deployment to complete (5-10 minutes)

### Step 4: Get Your Backend URL

Once deployed, Render will provide a URL like:
```
https://burnout-detection-api.onrender.com
```

**Save this URL** - you'll need it for frontend configuration.

### Step 5: Update CORS Settings

After deployment, update your backend CORS settings to allow your Vercel frontend domain.

**Option 1: Update in Code (Recommended)**

Edit `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "http://127.0.0.1:3000",  # Local development
        "https://your-frontend.vercel.app",  # Production (update this)
        "https://*.vercel.app",  # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Option 2: Use Environment Variable**

Update `backend/app/main.py`:

```python
import os

# Get allowed origins from environment variable
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then add to Render environment variables:
```
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://*.vercel.app
```

### Step 6: Redeploy Backend

After updating CORS settings:
1. Commit and push changes to GitHub
2. Render will automatically redeploy (or manually trigger redeploy)

---

## 🎨 Frontend Deployment on Vercel

### Step 1: Prepare Your Frontend for Deployment

#### 1.1 Update API Base URL

Edit `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://your-backend.onrender.com/api'  // Update with your Render URL
    : 'http://localhost:8000/api');
```

**Or use environment variable** (recommended):

Keep the current code:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
```

#### 1.2 Create `vercel.json` (Optional)

Create `vercel.json` in the `frontend` directory:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "headers": {
        "cache-control": "public, max-age=31536000, immutable"
      }
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### Step 2: Push Code to GitHub

Make sure your frontend code is committed:

```bash
git add frontend/
git commit -m "Prepare frontend for Vercel deployment"
git push origin main
```

### Step 3: Deploy to Vercel

#### Method 1: Via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Sign in or create an account

2. **Import Project**
   - Click **"Add New..."** → **"Project"**
   - Connect GitHub if not already connected
   - Select your repository (`IBM_skill_project`)

3. **Configure Project**
   
   **Framework Preset**: `Create React App`
   
   **Root Directory**: `frontend`
   
   **Build Command**: `npm run build` (should be auto-detected)
   
   **Output Directory**: `build` (should be auto-detected)
   
   **Install Command**: `npm install` (should be auto-detected)

4. **Configure Environment Variables**
   
   Click **"Environment Variables"** and add:
   
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com/api
   ```
   
   **Important**: Replace `your-backend.onrender.com` with your actual Render backend URL

5. **Deploy**
   - Click **"Deploy"**
   - Vercel will build and deploy your frontend
   - Wait for deployment to complete (2-5 minutes)

#### Method 2: Via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

4. **Follow Prompts**
   - Link to existing project or create new
   - Set environment variables when prompted

### Step 4: Get Your Frontend URL

After deployment, Vercel will provide a URL like:
```
https://your-project-name.vercel.app
```

**Save this URL** - you'll use it to access your application.

---

## ⚙️ Post-Deployment Configuration

### Step 1: Update Backend CORS with Frontend URL

1. Go to Render dashboard → Your backend service → **Environment**
2. Add or update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS=https://your-project-name.vercel.app,https://*.vercel.app
   ```
3. Redeploy the backend service

### Step 2: Verify Environment Variables

**Backend (Railway):**
- ✅ `DATABASE_URL` - Supabase connection string
- ✅ `GOOGLE_GEMINI_API_KEY` - Gemini API key
- ✅ `GEMINI_MODEL_NAME` - `gemini-pro`
- ✅ `ALLOWED_ORIGINS` - Your Vercel frontend URL

**Frontend (Vercel):**
- ✅ `REACT_APP_API_URL` - Your Render backend URL + `/api`

### Step 3: Test Database Connection

1. Go to Render dashboard → Your backend service → **Logs**
2. Check that the backend connects to Supabase successfully
3. Look for any connection errors

---

## 🧪 Testing the Deployment

### Test 1: Backend Health Check

Open in browser:
```
https://your-backend.onrender.com/health
```

Expected response:
```json
{"status": "healthy"}
```

### Test 2: Backend API Docs

Open in browser:
```
https://your-backend.onrender.com/docs
```

You should see the FastAPI interactive documentation.

### Test 3: Frontend Application

Open in browser:
```
https://your-project-name.vercel.app
```

You should see your React application.

### Test 4: End-to-End Test

1. Open your Vercel frontend URL
2. Fill out the user information form
3. Submit the form
4. Check browser console (F12) for any errors
5. Verify data is saved in Supabase dashboard

### Test 5: API Integration

Open browser console (F12) on your Vercel frontend and check:
- No CORS errors
- API calls are going to Render backend URL
- Responses are received successfully

---

## 🔧 Troubleshooting

### Backend Issues

**Problem: Build fails on Render**

**Solution:**
- Check Render build logs for specific errors
- **Verify Python version is set to 3.11.0** in Render dashboard (not 3.13)
- Verify `requirements.txt` includes all dependencies
- Ensure `psycopg2-binary` is used (not `psycopg`)
- Check that `startCommand` is correct
- Try updating pip first: `pip install --upgrade pip && pip install -r requirements.txt`

**Common Build Errors:**
- **Rust compilation errors**: Usually means Python version mismatch or outdated package versions
- **"can't execute an empty query"**: Database initialization issue (already fixed in code)
- **Package not found**: Check `requirements.txt` has correct package names

**Problem: Backend crashes after deployment**

**Solution:**
- Check Render logs for error messages
- Verify all environment variables are set correctly
- Ensure `DATABASE_URL` is correct and accessible
- Check that Supabase project is active (not paused)

**Problem: CORS errors**

**Solution:**
- Verify `ALLOWED_ORIGINS` includes your Vercel URL
- Check backend logs for CORS-related errors
- Ensure frontend `REACT_APP_API_URL` points to correct backend
- Redeploy backend after updating CORS settings

**Problem: Database connection errors**

**Solution:**
- Verify `DATABASE_URL` in Render environment variables
- Check Supabase project is active
- Ensure database password is correct
- Test connection string locally first

### Frontend Issues

**Problem: Build fails on Vercel**

**Solution:**
- Check Vercel build logs
- Verify `package.json` is correct
- Ensure Node.js version is compatible (16+)
- Check for any build errors in logs

**Problem: Frontend shows "Cannot connect to server"**

**Solution:**
- Verify `REACT_APP_API_URL` is set correctly in Vercel
- Check that backend URL is accessible
- Ensure backend is running (check Render dashboard)
- Verify CORS settings allow Vercel domain

**Problem: API calls return 404**

**Solution:**
- Verify `REACT_APP_API_URL` ends with `/api`
- Check backend routes are correct
- Ensure backend is deployed and running
- Check browser console for specific error messages

**Problem: Environment variables not working**

**Solution:**
- Vercel requires `REACT_APP_` prefix for React env vars
- Redeploy after adding/changing environment variables
- Clear browser cache
- Check Vercel environment variables are set correctly

### General Issues

**Problem: Changes not reflecting after deployment**

**Solution:**
- Clear browser cache
- Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Check that code is pushed to GitHub
- Verify deployment completed successfully

**Problem: Slow response times**

**Solution:**
- Render free tier spins down after inactivity (cold starts)
- Consider upgrading to paid tier for always-on service
- Use Vercel's edge functions for better performance
- Optimize database queries

---

## 🔄 Updating Your Deployment

### Updating Backend

1. **Make changes locally**
2. **Test locally** to ensure everything works
3. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Update backend"
   git push origin main
   ```
4. **Render will automatically redeploy** (or manually trigger redeploy)

### Updating Frontend

1. **Make changes locally**
2. **Test locally** to ensure everything works
3. **Commit and push to GitHub**:
   ```bash
   git add frontend/
   git commit -m "Update frontend"
   git push origin main
   ```
4. **Vercel will automatically redeploy**

### Updating Environment Variables

**Render (Backend):**
1. Go to Render dashboard → Your service → **Environment**
2. Add/update environment variables
3. Click **"Save Changes"**
4. Service will automatically redeploy

**Vercel (Frontend):**
1. Go to Vercel dashboard → Your project → **Settings** → **Environment Variables**
2. Add/update environment variables
3. Click **"Save"**
4. Redeploy the project (or it will redeploy on next push)

---

## 📊 Monitoring and Logs

### Render Logs

1. Go to Render dashboard → Your backend service
2. Click **"Logs"** tab
3. View real-time logs
4. Filter by errors, warnings, etc.

### Vercel Logs

1. Go to Vercel dashboard → Your project
2. Click **"Deployments"**
3. Click on a deployment → **"View Function Logs"**
4. View build and runtime logs

### Supabase Monitoring

1. Go to Supabase dashboard → Your project
2. Check **"Database"** → **"Logs"** for query performance
3. Monitor **"Usage"** for database activity

---

## 💰 Cost Considerations

### Free Tier Limits

**Render:**
- Free tier spins down after 15 minutes of inactivity
- 750 hours/month free
- Automatic SSL certificates
- Custom domains supported

**Vercel:**
- Unlimited deployments
- Automatic SSL certificates
- Custom domains supported
- 100GB bandwidth/month on free tier

**Supabase:**
- 500MB database storage free
- 2GB bandwidth/month free
- Unlimited API requests

### Upgrading

Consider upgrading if you need:
- Always-on backend (Render)
- More bandwidth (Vercel)
- Larger database (Supabase)
- Better performance
- Priority support

---

## 🔒 Security Best Practices

1. **Never commit secrets**
   - Use environment variables for all sensitive data
   - Add `.env` to `.gitignore`
   - Use Render/Vercel environment variables

2. **Use HTTPS**
   - Both Render and Vercel provide automatic SSL
   - Always use HTTPS URLs in production

3. **Restrict CORS**
   - Only allow your frontend domain
   - Don't use `allow_origins=["*"]` in production

4. **Rotate API keys regularly**
   - Update Gemini API key periodically
   - Rotate Supabase database password

5. **Monitor logs**
   - Check for suspicious activity
   - Set up alerts for errors

---

## 📝 Quick Reference

### Backend URLs
- **Production**: `https://your-backend.onrender.com`
- **Health Check**: `https://your-backend.onrender.com/health`
- **API Docs**: `https://your-backend.onrender.com/docs`

### Frontend URLs
- **Production**: `https://your-project-name.vercel.app`
- **Preview**: `https://your-project-name-git-branch.vercel.app`

### Environment Variables Checklist

**Backend (Render):**
```
DATABASE_URL=postgresql://...
GOOGLE_GEMINI_API_KEY=...
GEMINI_MODEL_NAME=gemini-pro
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

**Frontend (Vercel):**
```
REACT_APP_API_URL=https://your-backend.onrender.com/api
```

---

## ✅ Deployment Checklist

Before going live, verify:

- [ ] Backend deployed successfully on Render
- [ ] Frontend deployed successfully on Vercel
- [ ] All environment variables set correctly
- [ ] CORS configured to allow frontend domain
- [ ] Database connection working
- [ ] API endpoints accessible
- [ ] Frontend can communicate with backend
- [ ] Health check endpoints working
- [ ] SSL certificates active (automatic)
- [ ] Custom domains configured (if needed)
- [ ] Monitoring and logs accessible
- [ ] Error handling working correctly

---

## 🎓 Next Steps

1. **Set up custom domains** (optional)
   - Configure custom domain in Vercel
   - Configure custom domain in Render
   - Update DNS records

2. **Set up monitoring**
   - Configure error tracking (Sentry, etc.)
   - Set up uptime monitoring
   - Configure alerts

3. **Optimize performance**
   - Enable caching
   - Optimize images
   - Use CDN for static assets

4. **Set up CI/CD**
   - Configure automatic deployments
   - Set up testing pipelines
   - Configure preview deployments

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Deployment](https://react.dev/learn/start-a-new-react-project#production-ready-frameworks)
- [Supabase Documentation](https://supabase.com/docs)

---

**Congratulations! 🎉 Your application is now deployed and accessible worldwide!**

For issues or questions, refer to the troubleshooting section or check the platform-specific documentation.
