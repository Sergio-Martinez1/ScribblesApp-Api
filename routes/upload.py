import shutil
from fastapi import APIRouter, UploadFile, File, Depends, Request
from auth.authenticate import authenticate

upload_router = APIRouter(prefix="/files", tags=["Files"])


@upload_router.post("/")
async def upload_file(request: Request,
                      file: UploadFile = File(...),
                      user: str = Depends(authenticate)):
    path = f"files/{file.filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = f"{request.url}" + f"{file.filename}"
    return {"url": url, "type": file.content_type}
