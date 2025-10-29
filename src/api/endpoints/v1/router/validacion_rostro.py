from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io
import face_recognition
import os
from datetime import datetime

rostro = APIRouter(prefix="/api/v1/rostro", tags=["rostro"])

SAVE_DIR = "public/imagenes_con_rostro"
os.makedirs(SAVE_DIR, exist_ok=True)


@rostro.post("/validar-rostro/")
async def validar_rostro(file: UploadFile = File(...)):
    print("Validando rostro en la imagen subida...")
    print(f"Nombre del archivo: {file.filename}")

    """
    Valida si una imagen contiene un rostro humano.
    Si se detecta, guarda la imagen en una carpeta local.
    """

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = face_recognition.load_image_file(io.BytesIO(contents))
        face_locations = face_recognition.face_locations(image_np)

        if len(face_locations) > 0:
            # Guardar la imagen con un nombre único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            save_path = os.path.join(SAVE_DIR, filename)
            image.save(save_path)
            return {"tiene_rostro": True, "cantidad_rostros": len(face_locations), "ruta_guardado": save_path}
        else:
            return {"tiene_rostro": False, "cantidad_rostros": 0}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
