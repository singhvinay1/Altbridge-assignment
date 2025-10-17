from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List
import os
import time
import io
import base64
from ..services.pdf_extractor import extract_text_from_pdf
from ..services.llm_extract import extract_structured_data
from ..services.excel_writer import write_excel
from ..services.templates import load_template

router = APIRouter()


@router.post("/extract")
async def extract(files: List[UploadFile] = File(...), template_id: str = Form(...)):
    if template_id not in ("template1", "template2"):
        raise HTTPException(status_code=400, detail="Invalid template_id")

    # Extract text & run LLM per file to produce rows per PDF
    try:
        template = load_template(template_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    rows = []
    for f in files:
        content = await f.read()
        text = extract_text_from_pdf(content)
        structured_rows = extract_structured_data(text, template)
        # For template1 and template2, we only want the template structure once
        if template_id in ("template1", "template2"):
            if not rows:  # Only add template structure once
                rows.extend(structured_rows)
        else:
            # For other templates, extend as before
            rows.extend(structured_rows)

    filename, file_content = write_excel(rows, template)
    
    # For serverless environments, return the file directly as base64
    # This ensures the file is available immediately without storage issues
    file_base64 = base64.b64encode(file_content).decode('utf-8')
    
    return JSONResponse({
        "filename": filename,
        "file_data": file_base64,
        "message": "Extraction complete. File ready for download."
    })


