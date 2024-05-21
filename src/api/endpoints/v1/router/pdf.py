import io
import pathlib
import os
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse, StreamingResponse


pdf = APIRouter(prefix="/api/v1/pdf", responses={404: {"description": "Not found"}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "pdf")


@pdf.get("/uno")
def get_pdf_stream():

    print("-------------------------")
    print(pathlib.Path(__file__).parent.resolve())
    print("-------------------------")
    print(pathlib.Path().resolve())
    print("-------------------------")
    print(BASE_DIR)
    print("-------------------------")
    print(UPLOAD_DIR)
    print("-------------------------")

    # Open the PDF file from the disk as a file-like object
    f = open("./files/menu.pdf", "rb")

    # To pdf the file in the browser, use "inline" for the media_type
    headers = {"Content-Disposition": "inline; filename=files/menu.pdf"}

    # Create a StreamingResponse object with the file-like object, media type and headers
    response = StreamingResponse(f, media_type="application/pdf", headers=headers)

    # Return the StreamingResponse object
    return response


@pdf.get("/dos")
async def get_pdf_file():
    # To pdf the file in the browser, use "inline" for the media_type
    headers = {"Content-Disposition": "inline; filename=files/menu.pdf"}

    # Create a FileResponse object with the file path, media type and headers
    response = FileResponse(
        "files/menu.pdf", media_type="application/pdf", headers=headers
    )

    # Return the FileResponse object
    return response


@pdf.get("/tres")
def get_pdf():
    # Read the PDF file from the disk as a byte stream
    with open("files/menu.pdf", "rb") as f:
        pdf_bytes = f.read()

    # To pdf the file in the browser, use "inline" for the media_type
    headers = {"Content-Disposition": "inline; filename=files/menu.pdf"}

    # Create a Response object with the file bytes, media type and headers
    response = Response(pdf_bytes, media_type="application/pdf", headers=headers)

    # Return the Response object
    return response
