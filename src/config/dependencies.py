import os
from fastapi import Depends, HTTPException
from starlette import status
from .settings import TestingSettings, Settings, BaseAppSettings, LocalSettings
from src.exceptions import BaseSecurityError
from src.notifications import EmailSenderInterface, EmailSender
from src.security.http import get_token
from src.security.interfaces import JWTAuthManagerInterface
from src.security.token_manager import JWTAuthManager
from src.storages import S3StorageInterface, S3StorageClient


def get_settings() -> BaseAppSettings:
    env_mode = os.getenv("ENVIRONMENT", "local")
    if env_mode == "testing":
        return TestingSettings()
    if env_mode == "local":
        return LocalSettings()
    return Settings()  # env_mode == "docker" or else


def get_jwt_auth_manager(
    settings: BaseAppSettings = Depends(get_settings),
) -> JWTAuthManagerInterface:
    return JWTAuthManager(
        secret_key_access=settings.SECRET_KEY_ACCESS,
        secret_key_refresh=settings.SECRET_KEY_REFRESH,
        algorithm=settings.JWT_SIGNING_ALGORITHM,
    )


def get_email_notificator(
    settings: BaseAppSettings = Depends(get_settings),
) -> EmailSenderInterface:
    return EmailSender(
        hostname=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        email=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
        template_dir=settings.PATH_TO_EMAIL_TEMPLATES_DIR,
        activation_email_template_name=settings.ACTIVATION_EMAIL_TEMPLATE_NAME,
        activation_complete_email_template_name=settings.ACTIVATION_COMPLETE_EMAIL_TEMPLATE_NAME,
        password_email_template_name=settings.PASSWORD_RESET_TEMPLATE_NAME,
        password_complete_email_template_name=settings.PASSWORD_RESET_COMPLETE_TEMPLATE_NAME,
        password_change_email_template_name=settings.PASSWORD_CHANGE_NAME,
        send_payment_email_template_name=settings.SEND_PAYMENT_EMAIL_TEMPLATE_NAME,
        send_refund_email_template_name=settings.SEND_REFUND_EMAIL_TEMPLATE_NAME,
        send_cancellation_email_template_name=settings.SEND_CANCELLATION_EMAIL_TEMPLATE_NAME,
    )


def get_s3_storage_client(
    settings: BaseAppSettings = Depends(get_settings),
) -> S3StorageInterface:
    return S3StorageClient(
        endpoint_url=settings.s3_storage_endpoint,
        access_key=settings.S3_STORAGE_ACCESS_KEY,
        secret_key=settings.S3_STORAGE_SECRET_KEY,
        bucket_name=settings.S3_BUCKET_NAME,
    )


async def get_current_user_id(
    token: str = Depends(get_token),
    jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager),
) -> int:
    try:
        payload = jwt_manager.decode_access_token(token)
        user_id = int(payload.get("user_id"))
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user_id missing",
            )
        return user_id
    except BaseSecurityError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
