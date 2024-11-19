import os
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError, NotFound

try:
    storage_client = storage.Client()
    print("Google Cloud Storage client initialized successfully.")
except GoogleCloudError as e:
    print(f"Error al inicializar el cliente de Google Cloud Storage: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")

bucket_name = "autonomous-time-418513.firebasestorage.app"


def upload_file(file_path: str, destination_blob_name: str) -> str:
    """
    Sube un archivo al bucket de Google Cloud Storage.
    """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        print(f"Archivo '{file_path}' subido exitosamente a '{destination_blob_name}'.")
        return f"gs://{bucket_name}/{destination_blob_name}"
    except FileNotFoundError:
        print("Error: El archivo a subir no se encontró en la ruta especificada.")
    except GoogleCloudError as e:
        print(f"Error de Google Cloud al subir el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado al subir el archivo: {e}")


def download_file(source_blob_name: str, destination_file_name: str):
    """
    Descarga un archivo del bucket de Google Cloud Storage.
    """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(
            f"Archivo '{source_blob_name}' descargado exitosamente a '{destination_file_name}'."
        )
    except NotFound:
        print("Error: El archivo especificado no se encontró en el bucket.")
    except GoogleCloudError as e:
        print(f"Error de Google Cloud al descargar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado al descargar el archivo: {e}")


def delete_file(blob_name: str):
    """
    Elimina un archivo del bucket de Google Cloud Storage.
    """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        print(f"Archivo '{blob_name}' eliminado exitosamente del bucket.")
    except NotFound:
        print("Error: El archivo especificado no se encontró en el bucket.")
    except GoogleCloudError as e:
        print(f"Error de Google Cloud al eliminar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado al eliminar el archivo: {e}")


def list_files_in_bucket():
    """
    Lista todos los archivos en el bucket de Google Cloud Storage.
    """
    try:
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()
        files = [blob.name for blob in blobs]
        print("Archivos en el bucket:")
        for file in files:
            print(file)
        return files
    except GoogleCloudError as e:
        print(f"Error al listar archivos en el bucket: {e}")
    except Exception as e:
        print(f"Error inesperado al listar archivos: {e}")
