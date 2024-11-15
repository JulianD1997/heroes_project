from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from app.database.firebase_db import (
    create_hero_firestore,
    get_heroes_firestore,
    get_hero_by_id_firestore,
    delete_hero_firestore,
)
from app.storage.cloud_storage import upload_file
from pydantic import BaseModel
import os
import shutil
from pathlib import Path


class Hero(BaseModel):
    name: str
    age: int | None = None
    secret_name: str
    image_url: str | None = None


hero_router = APIRouter()


@hero_router.post("/heroes/", response_model=Hero)
async def create_hero(
    name: str = Form(...),
    age: int = Form(None),
    secret_name: str = Form(...),
    image: UploadFile = File(...),
):
    temp_dir = Path("./temp_files")
    temp_dir.mkdir(exist_ok=True)
    file_path = temp_dir / image.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    destination_blob_name = f"heroes_images/{name}.png"
    image_url = upload_file(str(file_path), destination_blob_name)
    os.remove(file_path)

    hero_data = {
        "name": name,
        "age": age,
        "secret_name": secret_name,
        "image_url": image_url,
    }
    return create_hero_firestore(hero_data)


@hero_router.get("/heroes/", response_model=List[Hero])
def read_heroes():
    return get_heroes_firestore()


@hero_router.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: str):
    hero = get_hero_by_id_firestore(hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@hero_router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: str):
    success = delete_hero_firestore(hero_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hero not found")
    return {"ok": True}
