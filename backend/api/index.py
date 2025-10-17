from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.extract import router as extract_router
from app.routes.download import router as download_router
from app.settings import settings

app = FastAPI(title="PDF Data Extraction API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(extract_router, prefix="/api")
app.include_router(download_router, prefix="/api")

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# For Vercel serverless
handler = app
