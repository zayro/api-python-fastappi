# main.py
import shutil
import os
import time
from typing import Annotated
from fastapi import APIRouter, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse


upload = APIRouter(
    prefix="/api/v1/upload", responses={404: {"description": "Not found"}}
)


time_str = time.strftime("%Y-%m%d - %H%M%S")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


@upload.get("/download/{file_name}")
def upload_download(file_name: str):
    upload_folder = "public/files/uploads/" + file_name
    upload_dir = os.path.join(os.getcwd(), upload_folder)
    # DEPENDS ON WHERE YOUR FILE LOCATES

    print("-----------------------")
    print(upload_dir)
    print("-----------------------")
    return FileResponse(
        path=upload_dir, media_type="application/octet-stream", filename=file_name
    )


@upload.get("/download/view/{file_name}")
def upload_download_file(file_name: str):
    upload_folder = "public/files/uploads/" + file_name
    upload_dir = os.path.join(os.getcwd(), upload_folder)
    # DEPENDS ON WHERE YOUR FILE LOCATES
    return FileResponse(upload_dir)


@upload.post("/file/single")
async def create_upload_file(file: UploadFile):
    upload_folder = "public/files/uploads"
    upload_dir = os.path.join(os.getcwd(), upload_folder)
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    dest = os.path.join(upload_dir, file.filename)
    print(dest)

    # Get the file size (in bytes)
    file.file.seek(0, 2)
    file_size = file.file.tell()

    # move the cursor back to the beginning
    await file.seek(0)

    if file_size > 2 * 1024 * 1024:
        # more than 2 MB
        raise HTTPException(status_code=400, detail="File too large")

    # check the content type (MIME type)
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # copy the file contents
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}


@upload.post("/file/multiple")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):

    upload_folder = "public/files/uploads"
    upload_dir = os.path.join(os.getcwd(), upload_folder)
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    for file in files:
        file_location = f"{upload_folder}/{file.filename}"
        print(file_location)
        with open(file_location, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {"filenames": [file.filename for file in files]}


@upload.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}
