from cloudevents.http import CloudEvent
import functions_framework
from google.cloud import storage
from PIL import Image
import os

# Configura el cliente de Google Cloud Storage
storage_client = storage.Client()


# Esta función se activa cuando hay un cambio en un bucket de Google Cloud Storage
@functions_framework.cloud_event
def generate_thumbnail(cloud_event: CloudEvent) -> tuple:
    """Esta función se activa cuando hay un cambio en el bucket de Google Cloud Storage,
    específicamente en la carpeta 'heroes_images/'. La función solo se ejecuta para
    eventos de creación de archivo y descarga el archivo si es nuevo.

    Args:
        cloud_event: El CloudEvent que activó esta función.
    Returns:
        Una tupla con el event_id, event_type, bucket, name, metageneration y timeCreated.
    """
    event_type = cloud_event["type"]

    if event_type != "google.cloud.storage.object.v1.finalized":
        print(f"Ignorando evento de tipo: {event_type}")
        return

    data = cloud_event.data
    bucket_name = data["bucket"]
    name = data["name"]

    if not name.startswith("heroes_images/"):
        print(f"Ignorando archivo fuera de 'heroes_images': {name}")
        return

    # Descargar el archivo desde el bucket
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(name)

    local_file_name = f"/tmp/{os.path.basename(name)}"
    thumbnail_file_name = f"/tmp/thumbnail_{os.path.basename(name)}"

    try:
        # Descargar el archivo
        blob.download_to_filename(local_file_name)
        print(f"Archivo descargado correctamente: {local_file_name}")

        # Verificar si el archivo descargado es una imagen
        with Image.open(local_file_name) as img:
            # Crear la miniatura
            img.thumbnail((128, 128))  # Cambia el tamaño según sea necesario
            img.save(thumbnail_file_name)
            print(f"Miniatura creada: {thumbnail_file_name}")

        # Subir la miniatura al bucket en la carpeta 'heroes_miniatures'
        miniatures_blob = bucket.blob(
            f"heroes_miniatures/thumbnail_{os.path.basename(name)}"
        )
        miniatures_blob.upload_from_filename(thumbnail_file_name)
        print("Miniatura subida correctamente al bucket.")

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return

    # Retornar la información relevante del evento
    return event_type, bucket_name, name
