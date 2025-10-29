from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
import secrets
import time
from datetime import datetime, timedelta


validacion_correo = APIRouter(prefix="/api/v1/validacion_correo", tags=["validacion_correo"], responses={404: {"description": "Not found"}})

# Para este ejemplo, usaremos un diccionario en memoria para almacenar los códigos.
# En un entorno de producción, deberías usar una base de datos o caché como Redis.
verification_codes = {}


class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "zayro8905@gmail.com"
SMTP_PASSWORD = "dwllaiexubaojtev"


def generate_verification_code():
    return secrets.token_hex(4)  # Genera un código hexadecimal de 8 caracteres


def send_email(email: EmailSchema, verification_code: str):
    msg = MIMEText(email.body + f"\n\nCódigo de verificación: {verification_code}")
    msg["Subject"] = email.subject
    msg["From"] = SMTP_USER
    msg["To"] = email.email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [email.email], msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@validacion_correo.post("/demo")
async def send_verification():

    return {"message": "Email de verificación enviado en segundo plano"}


@validacion_correo.post("/send-verification-email/")
async def send_verification_email(email: EmailSchema, background_tasks: BackgroundTasks):
    verification_code = generate_verification_code()
    expiration_time = datetime.utcnow() + timedelta(minutes=30)  # Código expira en 30 minutos
    verification_codes[email.email] = {"code": verification_code, "expiration": expiration_time}

    email.body = f"Este es tu código de verificación. Expira en 30 minutos."
    background_tasks.add_task(send_email, email, verification_code)
    return {"message": "Email de verificación enviado en segundo plano"}


class VerificationRequest(BaseModel):
    email: EmailStr
    code: str


@validacion_correo.post("/verify-email/")
async def verify_email(verification_request: VerificationRequest):
    email = verification_request.email
    code = verification_request.code

    if email in verification_codes:
        stored_code_data = verification_codes[email]
        if stored_code_data["code"] == code:
            if datetime.utcnow() <= stored_code_data["expiration"]:
                del verification_codes[email]  # Elimina el código después de la verificación exitosa
                return {"message": "Correo electrónico verificado exitosamente"}
            else:
                del verification_codes[email]
                raise HTTPException(status_code=400, detail="El código ha expirado")
        else:
            raise HTTPException(status_code=400, detail="Código inválido")
    else:
        raise HTTPException(status_code=404, detail="Código no encontrado para este correo electrónico")
