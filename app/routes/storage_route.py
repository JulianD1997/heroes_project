from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.storage.cloud_storage import (
    upload_file,
    download_file,
    delete_file,
    list_files_in_bucket,
)
import shutil
import os
from pathlib import Path

temp_dir = Path("./temp_files")
temp_dir.mkdir(exist_ok=True)

storage_router = APIRouter()


@storage_router.post("/upload/")
async def upload_to_storage(file: UploadFile = File(...)):
    file_path = temp_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        destination_blob_name = file.filename
        file_url = upload_file(str(file_path), destination_blob_name)
        os.remove(file_path)
        return {"file_url": file_url}
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail="Error uploading file") from e


@storage_router.get("/download/{file_name}")
async def download_from_storage(file_name: str, background_tasks: BackgroundTasks):
    temp_file_path = temp_dir / file_name
    try:
        download_file(file_name, str(temp_file_path))

        # Agrega una tarea en segundo plano para eliminar el archivo después de 5 minutos
        background_tasks.add_task(delete_file_after_delay, temp_file_path, delay=300)

        return {"message": f"File downloaded successfully to {temp_file_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error downloading file") from e


@storage_router.delete("/delete/{file_name}")
async def delete_from_storage(file_name: str):
    try:
        delete_file(file_name)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting file") from e


@storage_router.get("/view")
async def get_all():
    try:
        files = list_files_in_bucket()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error listing files") from e


def delete_file_after_delay(file_path: Path, delay: int = 300):
    import time

    time.sleep(delay)
    if file_path.exists():
        file_path.unlink()  # Elimina el archivo
        print(f"Archivo {file_path} eliminado después de {delay} segundos.")
