from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Path, Query
from app.internals.company_utils import *
from sqlmodel import Session
from fastapi import APIRouter, File, UploadFile


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    responses={404: {"description": "Not found"}},
)

def get_file_size(file: UploadFile):
    # move the cursor to the end of the file
    file.file._file.seek(0, 2)  # pyright: ignore reportPrivateUsage=none
    file_size = (
        file.file._file.tell()  # pyright: ignore reportPrivateUsage=none
    )  # Getting the size of the file
    # move the cursor back to the beginning of the file
    file.file.seek(0)

    return file_size

@router.post("/upload")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    # Handle file upload logic here
    filesize = file.size
    return {"filesize": filesize}

@router.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

@router.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }