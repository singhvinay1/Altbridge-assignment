# Vercel Deployment Guide

This guide will help you deploy the PDF Data Extraction Tool to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Google AI API Key**: For the backend functionality

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure your code is pushed to GitHub with the following structure:
```
Altbridge-assignment/
├── frontend/          # React app
├── backend/           # FastAPI app
├── templates/         # Extraction templates
├── vercel.json        # Vercel configuration
└── .vercelignore      # Files to ignore
```

### 2. Deploy to Vercel

#### Option A: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from project root**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new
   - Set up project settings
   - Deploy

#### Option B: Deploy via Vercel Dashboard

1. **Go to [vercel.com/dashboard](https://vercel.com/dashboard)**
2. **Click "New Project"**
3. **Import your GitHub repository**
4. **Configure project settings**:
   - Framework Preset: `Other`
   - Root Directory: `./` (project root)
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/dist`

### 3. Configure Environment Variables

In your Vercel project dashboard:

1. **Go to Settings → Environment Variables**
2. **Add the following variables**:

   | Name | Value | Environment |
   |------|-------|-------------|
   | `GOOGLE_API_KEY` | Your Google AI API key | Production, Preview, Development |
   | `FRONTEND_ORIGIN` | `https://your-app-name.vercel.app` | Production, Preview, Development |

### 4. Update CORS Settings

After deployment, update the `FRONTEND_ORIGIN` in your backend settings to match your Vercel domain.

### 5. Test Your Deployment

1. **Visit your deployed app**: `https://your-app-name.vercel.app`
2. **Test the API**: `https://your-app-name.vercel.app/api/health`
3. **Upload a sample PDF** and test extraction

## Project Structure for Vercel

The deployment uses this structure:

```
/ (root)
├── frontend/          # Static React build
│   ├── dist/         # Built frontend (generated)
│   └── vercel.json   # Frontend config
├── backend/
│   └── api/          # Serverless functions
│       ├── index.py  # Main API handler
│       └── requirements.txt
├── templates/        # Shared templates
└── vercel.json       # Main Vercel config
```

## API Endpoints

After deployment, your API will be available at:

- **Health Check**: `https://your-app.vercel.app/api/health`
- **Extract Data**: `https://your-app.vercel.app/api/extract`
- **Download Files**: `https://your-app.vercel.app/api/download/{filename}`

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that all dependencies are in `package.json`
   - Ensure build commands are correct
   - Check Vercel build logs

2. **API Not Working**:
   - Verify environment variables are set
   - Check CORS configuration
   - Ensure Google API key is valid

3. **File Upload Issues**:
   - Check file size limits (Vercel has 4.5MB limit for serverless)
   - Verify multipart form handling

### File Size Limitations

- **Vercel Serverless**: 4.5MB request limit
- **Vercel Pro**: 4.5MB request limit
- **Vercel Enterprise**: 4.5MB request limit

For larger files, consider:
- Using Vercel Blob for file storage
- Implementing chunked uploads
- Using external file storage (AWS S3, etc.)

## Custom Domain (Optional)

1. **Go to Project Settings → Domains**
2. **Add your custom domain**
3. **Configure DNS records** as instructed
4. **Update environment variables** with new domain

## Monitoring

- **Vercel Analytics**: Built-in performance monitoring
- **Function Logs**: Check serverless function logs
- **Error Tracking**: Monitor API errors

## Cost Considerations

- **Hobby Plan**: Free tier with limitations
- **Pro Plan**: $20/month for higher limits
- **Enterprise**: Custom pricing

Check [Vercel Pricing](https://vercel.com/pricing) for current details.

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **Support**: Available for Pro/Enterprise plans
