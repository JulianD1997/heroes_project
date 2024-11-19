from fastapi import FastAPI
from app.routes.hero_route import hero_router
from app.routes.storage_route import storage_router

app = FastAPI()

app.include_router(hero_router, prefix="/api", tags=["Heroes"])
app.include_router(storage_router, prefix="/storage", tags=["Storage"])


@app.get("/")
def read_root():
    return {"message": "¡Hola, Mundo desde FastAPI!"}
