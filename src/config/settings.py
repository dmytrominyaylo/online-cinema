import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()
env_mode: str = os.getenv("ENVIRONMENT", "local")


class BaseAppSettings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    # For test in SQL database
    PATH_TO_DB: str = str(BASE_DIR / "database" / "cinema.db")

    PATH_TO_EMAIL_TEMPLATES_DIR: str = str(BASE_DIR / "notifications" / "templates")
    ACTIVATION_EMAIL_TEMPLATE_NAME: str = "activation_request.html"
    ACTIVATION_COMPLETE_EMAIL_TEMPLATE_NAME: str = "activation_complete.html"
    PASSWORD_RESET_TEMPLATE_NAME: str = "password_reset_request.html"
    PASSWORD_RESET_COMPLETE_TEMPLATE_NAME: str = "password_reset_complete.html"
    PASSWORD_CHANGE_NAME: str = "password_change.html"

    SEND_PAYMENT_EMAIL_TEMPLATE_NAME: str = "send_payment.html"
    SEND_REFUND_EMAIL_TEMPLATE_NAME: str = "send_refund.html"
    SEND_CANCELLATION_EMAIL_TEMPLATE_NAME: str = "send_cancellation.html"

    LOGIN_TIME_DAYS: int = 7

    EMAIL_HOST: str = os.getenv("EMAIL_HOST", "host")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", 25))
    EMAIL_HOST_USER: str = os.getenv("EMAIL_HOST_USER", "testuser")
    EMAIL_HOST_PASSWORD: str = os.getenv("EMAIL_HOST_PASSWORD", "test_password")
    EMAIL_USE_TLS: bool = os.getenv("EMAIL_USE_TLS", "False").lower() == "true"
    MAILHOG_API_PORT: int = os.getenv("MAILHOG_API_PORT", 8025)

    S3_STORAGE_HOST: str = os.getenv("MINIO_HOST", "localhost")
    S3_STORAGE_PORT: int = os.getenv("MINIO_PORT", 9000)
    S3_STORAGE_ACCESS_KEY: str = os.getenv("MINIO_ROOT_USER", "minioadmin")
    S3_STORAGE_SECRET_KEY: str = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
    S3_BUCKET_NAME: str = os.getenv("MINIO_STORAGE", "online-cinema-bucket")

    @property
    def s3_storage_endpoint(self) -> str:
        return f"http://{self.S3_STORAGE_HOST}:{self.S3_STORAGE_PORT}"

    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
    )

    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", os.urandom(99))
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", os.urandom(64))
    STRIPE_CURRENCY: str = os.getenv("STRIPE_CURRENCY", "usd")


class Settings(BaseAppSettings):
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "test_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "test_password")
    POSTGRES_DB_PORT: int = int(os.getenv("POSTGRES_DB_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test_db")

    SECRET_KEY_ACCESS: str = os.getenv("SECRET_KEY_ACCESS", os.urandom(32))
    SECRET_KEY_REFRESH: str = os.getenv("SECRET_KEY_REFRESH", os.urandom(32))
    JWT_SIGNING_ALGORITHM: str = os.getenv("JWT_SIGNING_ALGORITHM", "HS256")


class TestingSettings(BaseAppSettings):
    SECRET_KEY_ACCESS: str = "SECRET_KEY_ACCESS"
    SECRET_KEY_REFRESH: str = "SECRET_KEY_REFRESH"
    JWT_SIGNING_ALGORITHM: str = "HS256"


class LocalSettings(Settings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if env_mode == "local":
            self.POSTGRES_HOST = "localhost"
            self.S3_STORAGE_HOST = "localhost"
            self.EMAIL_HOST = "localhost"
