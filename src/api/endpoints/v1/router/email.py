import os
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
import secrets
import time
from datetime import datetime, timedelta
from mailjet_rest import Client

# Mailjet: leer de variables de entorno
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")
MAILJET_FROM_EMAIL = os.getenv("MAILJET_FROM_EMAIL", "zayro8905@gmail.com")
MAILJET_FROM_NAME = os.getenv("MAILJET_FROM_NAME", "Mi App")


email = APIRouter(prefix="/api/v1/email", responses={404: {"description": "Not found"}})

# Para este ejemplo, usaremos un diccionario en memoria para almacenar los códigos.
# En un entorno de producción, deberías usar una base de datos o caché como Redis.
verification_codes = {}


class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str


SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "zayro8905@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def generate_verification_code():
    return secrets.token_hex(4)  # Genera un código hexadecimal de 8 caracteres


def send_email_mailjet(email: EmailSchema, verification_code: str):
    """Envía el email usando Mailjet (v3.1)."""
    try:
        mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version="v3.1")
        data = {
            "Messages": [
                {
                    "From": {"Email": MAILJET_FROM_EMAIL, "Name": MAILJET_FROM_NAME},
                    "To": [{"Email": email.email, "Name": email.email}],
                    "Subject": email.subject,
                    "TextPart": f"{email.body}\n\nCódigo de verificación: {verification_code}",
                    "HTMLPart": f"<p>{email.body}</p><p><b>Código de verificación:</b> {verification_code}</p>",
                }
            ]
        }
        result = mailjet.send.create(data=data)
        status = result.status_code if hasattr(result, "status_code") else result.get("Status")
        if int(status) >= 400:
            raise Exception(f"Mailjet error: {result.status_code} {result.json() if hasattr(result, 'json') else result}")
    except Exception as e:
        # No lanzar HTTPException desde el hilo de background; loggear o relanzar si se usa directamente
        raise


@email.post("/send-verification-email-mailjet")
def send_verification_email_mailjet(email: EmailSchema):
    """
    Genera código y envía el email en background usando Mailjet.
    """
    try:
        verification_code = generate_verification_code()
        expiration_time = datetime.utcnow() + timedelta(minutes=30)
        verification_codes[email.email] = {"code": verification_code, "expiration": expiration_time}

        email.body = f"Este es tu código de verificación. Expira en 30 minutos."

        return {"message": "Email de verificación enviado en segundo plano (Mailjet)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@email.post("/send-verification-email/")
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


@email.post("/verify-email/")
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
