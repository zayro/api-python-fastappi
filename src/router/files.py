# main.py
import shutil
import os
import time
from fnmatch import fnmatch
from typing import Annotated
from fastapi import APIRouter, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from pathlib import Path


files = APIRouter(
    prefix="/api/v1/file",
    responses={404: {"description": "Not found"}}
)


time_str = time.strftime('%Y-%m%d - %H%M%S')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


@files.get("/list")
def file_list():
    pathDir = "public/files/uploads"

    list_dir = []

    for file in os.listdir(pathDir):
        dir_validate = (os.path.join(pathDir, file))
        isdir = os.path.isdir(dir_validate)
        print('Filename: {:<10} Match: {:<5} Folder: {}'.format(
            file, fnmatch(file, '*.pdf'), isdir))
        if fnmatch(file, '*.pdf'):
            list_dir.append(pathDir + "/" + file)

    return list_dir


@files.get("/list/all")
def file_list():
    path_dir = "public"
    list_match = []

    for path, subdirs, files in os.walk(path_dir):
        for name in files:
            # print(os.path.join(path, name))

            # print('Filename: {:<25} Match: {}'.format( name, fnmatch(name, '*.html')))

            if fnmatch(name, '*.pdf'):
                file_math = os.path.join(path, name)
                list_match.append(path.replace('\\', '/') + '/' + name)

    return list_match
