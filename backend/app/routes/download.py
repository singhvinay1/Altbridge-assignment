from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import os
import tempfile
import io
from ..settings import get_output_dir

router = APIRouter()

# In-memory storage for generated files (for serverless environments)
file_storage = {}

@router.get("/download/{filename}")
async def download(filename: str):
    # First try to get from in-memory storage (for serverless)
    if filename in file_storage:
        file_content = file_storage[filename]
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    # Fallback to file system (for local development)
    output_dir = get_output_dir()
    path = os.path.join(output_dir, filename)
    if os.path.exists(path):
        from fastapi.responses import FileResponse
        return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=filename)
    
    raise HTTPException(status_code=404, detail="File not found")

def store_file_in_memory(filename: str, file_content: bytes):
    """Store file content in memory for serverless environments"""
    file_storage[filename] = file_content



