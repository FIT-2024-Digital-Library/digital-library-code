from minio import Minio


minio_client = Minio(
    "play.min.io",  # URL MinIO сервера
    access_key="ACCESSKEYID",
    secret_key="SECRETACCESSKEY",
    secure=False
)
