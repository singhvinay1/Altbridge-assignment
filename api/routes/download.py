from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from settings import get_output_dir

router = APIRouter()


@router.get("/download/{filename}")
async def download(filename: str):
    output_dir = get_output_dir()
    path = os.path.join(output_dir, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=filename)



