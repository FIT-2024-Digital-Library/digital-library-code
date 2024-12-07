from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from minio.error import S3Error
import io

from app.storage.config import minio_client, minio_cred


router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Чтение файла в память
        file_data = await file.read()
        file_stream = io.BytesIO(file_data)

        # Загрузка файла в MinIO
        minio_client.put_object(
            minio_cred.BUCKET_NAME,  # Имя бакета
            file.filename,  # Имя файла
            file_stream,  # Данные файла
            len(file_data)  # Размер файла
        )
        return {"message": "File uploaded successfully"}
    except S3Error as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.get("/download/{file_name}")
async def download_file(file_name: str):
    try:
        # Скачивание файла из MinIO
        response = minio_client.get_object(minio_cred.BUCKET_NAME, file_name)
        return StreamingResponse(
            response.stream(), media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file_name}"}
        )
    except S3Error as err:
        raise HTTPException(status_code=500, detail=str(err))
