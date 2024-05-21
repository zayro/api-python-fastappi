import os

from pydantic import BaseModel, Field

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    # Configuración general de la aplicación
    APP_NAME: str = Field("My FastAPI App")
    DEBUG: bool = Field(default=False)

    # Configuración de la base de datos
    DATABASE_URL: str = Field("postgresql://postgres:zayro@localhost/enterprise")

    # Configuración de Redis
    REDIS_HOST: str = Field("localhost")
    REDIS_PORT: int = Field(6379)
    REDIS_DB: int = Field(0)

    # Configuración de RabbitMQ
    RABBITMQ_HOST: str = Field(default=os.getenv("RABBITMQ_HOST", "localhost"))
    RABBITMQ_PORT: int = Field(default=int(os.getenv("RABBITMQ_PORT", 5672)))
    RABBITMQ_USER: str = Field(default=os.getenv("RABBITMQ_USER", "guest"))
    RABBITMQ_PASSWORD: str = Field(default=os.getenv("RABBITMQ_PASSWORD", "guest"))
    RABBITMQ_HOST: str = Field("localhost")
    RABBITMQ_PORT: int = Field(5672)
    RABBITMQ_USER: str = Field("guest")
    RABBITMQ_PASSWORD: str = Field("guest")

    # Configuración de la JWT
    JWT_SECRET_KEY: str = Field("myjwtsecret")
    JWT_ALGORITHM: str = Field("HS256")
    JWT_EXPIRATION_HOURS: int = Field(1440)


# Crear una instancia de la configuración
settings = Settings()
