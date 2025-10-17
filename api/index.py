import sys
import os
from mangum import Mangum

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the FastAPI app
try:
    from main import app
except ImportError:
    # Fallback: create a simple FastAPI app
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from routes import extract as extract_route
    from routes import download as download_route
    
    app = FastAPI(title="PDF Extraction Tool API", version="0.1.0")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/api/health")
    async def api_health():
        return {"status": "ok"}
    
    app.include_router(extract_route.router, prefix="/api")
    app.include_router(download_route.router, prefix="/api")

# Create the Vercel handler using Mangum
handler = Mangum(app, lifespan="off")
