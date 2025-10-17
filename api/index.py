from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Import the route modules
from .routes import extract as extract_route
from .routes import download as download_route

load_dotenv()

app = FastAPI(title="PDF Extraction Tool API", version="0.1.0")

# Get frontend origin from environment
frontend_origin = os.getenv("FRONTEND_ORIGIN", "https://your-app.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

# Include routers
app.include_router(extract_route.router, prefix="")
app.include_router(download_route.router, prefix="")

# Vercel handler
from mangum import Mangum
handler = Mangum(app)
