import firebase_admin
from firebase_admin import credentials, firestore
import os

if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()


def create_hero_firestore(hero_data: dict) -> dict:
    doc_ref = db.collection("heroes").document()
    doc_ref.set(hero_data)
    hero_data["id"] = doc_ref.id
    return hero_data


def get_heroes_firestore() -> list:
    heroes = []
    docs = db.collection("heroes").stream()
    for doc in docs:
        hero = doc.to_dict()
        hero["id"] = doc.id
        heroes.append(hero)
    return heroes


def get_hero_by_id_firestore(hero_id: str) -> dict:
    doc_ref = db.collection("heroes").document(hero_id)
    doc = doc_ref.get()
    if doc.exists:
        hero = doc.to_dict()
        hero["id"] = doc.id
        return hero
    else:
        return None


def delete_hero_firestore(hero_id: str) -> bool:
    doc_ref = db.collection("heroes").document(hero_id)
    if doc_ref.get().exists:
        doc_ref.delete()
        return True
    else:
        return False
