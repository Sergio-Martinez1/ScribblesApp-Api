from fastapi import APIRouter, UploadFile, File, Depends
from auth.authenticate import authenticate

upload_router = APIRouter(prefix='/upload', tags=['Files'])


@upload_router.post('/')
async def upload_file(file: UploadFile = File(...),
                      user: str = Depends(authenticate)):
    path = f"files/{file.filename}"
    return {"path": path, "filename": file.filename}
