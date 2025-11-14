# Vercel Deployment Setup

This repository includes automated deployment to Vercel via GitHub Actions.

## Required Secrets

Add these secrets in your GitHub repository settings (Settings → Secrets and variables → Actions):

### 1. Vercel CLI Token
```bash
# Get your Vercel token
vercel login
vercel whoami
# Copy the token from Vercel dashboard → Settings → Tokens
```
Add as: `VERCEL_TOKEN`

### 2. Vercel Organization ID
```bash
# In your project directory
vercel link
# This creates .vercel/project.json with your org ID
cat .vercel/project.json
```
Add the `orgId` as: `VERCEL_ORG_ID`

### 3. Vercel Project ID
```bash
# From the same .vercel/project.json file
cat .vercel/project.json
```
Add the `projectId` as: `VERCEL_PROJECT_ID`

### 4. Project Domain (Optional)
Add your Vercel project domain as: `VERCEL_PROJECT_DOMAIN`
Example: `kugou-widget.vercel.app`

## Environment Variables (Vercel Dashboard)

Set these in your Vercel project dashboard:

- `FIREBASE_CREDENTIALS` - Your Firebase service account JSON
- `FIREBASE_DATABASE_URL` - Your Firebase Realtime Database URL

## Manual Setup Commands

If you prefer manual deployment:

```bash
# Install Vercel CLI
npm i -g vercel

# Login and link project
vercel login
vercel link

# Deploy
vercel --prod
```

## Workflow Features

- ✅ Automatic deployment on push to main
- ✅ Deployment preview on pull requests  
- ✅ Health check after deployment
- ✅ Demo endpoint testing
- ✅ Build artifact caching
- ✅ Production environment deployment

## Troubleshooting

**Deployment fails with "VERCEL_TOKEN not found":**
- Add your Vercel token to repository secrets

**Build fails with Python runtime errors:**
- Check `vercel.json` uses `@vercel/python@4.1.0`
- Ensure `api/requirements.txt` has all dependencies

**Health check fails:**
- Check Vercel function logs
- Verify deployment URL is correct
- Ensure environment variables are set