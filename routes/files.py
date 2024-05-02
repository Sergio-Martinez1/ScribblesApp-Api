from fastapi import APIRouter, UploadFile, File, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from services.files import FilesService
from db_config.database import get_db
from auth.authenticate import authenticate

files_router = APIRouter(prefix="/files", tags=["Files"])


@files_router.post("/")
async def upload_file(request: Request,
                      file: UploadFile = File(...),
                      user: str = Depends(authenticate),
                      db: Session = Depends(get_db)):
    url = await FilesService().upload_file(db=db, username=user, file=file)
    return JSONResponse(content={"url": url},
                        status_code=status.HTTP_201_CREATED)


@files_router.delete("/{filename}", status_code=status.HTTP_200_OK)
async def delete_file(filename: str,
                      request: Request,
                      user: str = Depends(authenticate),
                      db: Session = Depends(get_db)):
    await FilesService().delete_file(db=db, username=user, filename=filename)
    return JSONResponse(content={"message": "File deleted sucessfully"},
                        status_code=status.HTTP_200_OK)
