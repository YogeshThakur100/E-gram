import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
router = APIRouter()

@router.get("/output.html")
def serve_output_html():
    home_path = os.path.expanduser("~")
    file_path = os.path.join(home_path, 'Documents', 'grampanchayat', 'reports', 'output.html')
    print('file_path ---->' , file_path)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    return {"error": "File not found"}