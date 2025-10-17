# Vercel Deployment Guide

This guide will help you deploy your PDF Data Extraction Tool to Vercel.

## Prerequisites

1. **GitHub Repository**: Your code should be pushed to GitHub
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
3. **Google AI API Key**: For the data extraction functionality

## Deployment Steps

### 1. Connect GitHub to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Select your repository from the list

### 2. Configure Environment Variables

In the Vercel dashboard, go to your project settings and add these environment variables:

```
GOOGLE_API_KEY=your_google_ai_api_key_here
FRONTEND_ORIGIN=https://your-app-name.vercel.app
```

**Important**: Replace `your_google_ai_api_key_here` with your actual Google AI API key and `your-app-name` with your actual Vercel app name.

### 3. Configure Build Settings

Vercel should automatically detect the configuration from `vercel.json`, but verify these settings:

- **Framework Preset**: Other
- **Root Directory**: Leave empty (uses root)
- **Build Command**: `cd frontend && npm run build`
- **Output Directory**: `frontend/dist`

### 4. Deploy

1. Click "Deploy" in the Vercel dashboard
2. Wait for the deployment to complete
3. Your app will be available at `https://your-app-name.vercel.app`

## Project Structure for Vercel

```
Altbridge-assignment/
├── api/                    # Vercel serverless functions
│   ├── index.py           # Main FastAPI app with Mangum handler
│   ├── routes/            # API routes
│   ├── services/          # Business logic
│   ├── templates/         # Extraction templates
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── vercel.json           # Vercel configuration
└── DEPLOYMENT.md         # This file
```

## Key Changes Made for Vercel

1. **API Structure**: Created `/api` directory with Vercel-compatible FastAPI setup
2. **Mangum Handler**: Added Mangum to convert FastAPI to AWS Lambda/Vercel format
3. **Routing**: Updated `vercel.json` to route `/api/*` to Python functions
4. **Frontend**: Updated API calls to use `/api` prefix
5. **Environment Variables**: Configured for Vercel deployment

## Troubleshooting

### Common Issues

1. **Environment Variables Not Working**
   - Ensure variables are set in Vercel dashboard
   - Check variable names match exactly (case-sensitive)
   - Redeploy after adding variables

2. **API Routes Not Working**
   - Verify `vercel.json` configuration
   - Check that `/api/index.py` exists
   - Ensure `mangum` is in requirements.txt

3. **Build Failures**
   - Check that all dependencies are in `package.json` and `requirements.txt`
   - Verify Python version compatibility
   - Check build logs in Vercel dashboard

4. **CORS Issues**
   - Update `FRONTEND_ORIGIN` environment variable
   - Ensure it matches your actual Vercel domain

### File Size Limits

- Vercel has a 50MB limit for serverless functions
- PDF files are processed in memory, so large files might cause issues
- Consider implementing file size validation

### Function Timeout

- Default timeout is 10 seconds for Hobby plan
- Increased to 30 seconds in `vercel.json`
- For Pro plan, can be increased to 60 seconds

## Local Development

To test the Vercel setup locally:

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel dev`
3. Your app will be available at `http://localhost:3000`

## Monitoring

- Check Vercel dashboard for deployment status
- Monitor function logs for errors
- Use Vercel Analytics for performance insights

## Support

If you encounter issues:

1. Check Vercel deployment logs
2. Verify environment variables
3. Test API endpoints individually
4. Check browser console for frontend errors

## Next Steps

After successful deployment:

1. Test all functionality with sample PDFs
2. Set up custom domain (optional)
3. Configure monitoring and alerts
4. Set up CI/CD for automatic deployments
