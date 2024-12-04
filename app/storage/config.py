from minio import Minio
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MINIO_', env_file="./config/minio-client.env")

    BUCKET_NAME: str
    HOSTNAME: str
    PORT: int
    LOGIN: str
    PASSWORD: str

    @property
    def minio_url(self) -> str:
        """Hostname with port"""
        return f"{self.minio.HOSTNAME}:{self.minio.PORT}"


minio_cred = MinioSettings()

minio_client = Minio(
    minio_cred.minio_url,
    access_key=minio_cred.LOGIN,
    secret_key=minio_cred.PASSWORD,
    secure=False
)
