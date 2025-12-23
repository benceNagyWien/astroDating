from fastapi import FastAPI
from contextlib import asynccontextmanager

# Importiere die Funktionen aus unserer database.py
from backend.database import create_db_and_tables

# NOTE: Comments are in German as per DEVELOPMENT_GUIDELINES.md

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Diese Funktion wird beim Starten der FastAPI Anwendung ausgeführt.
    Hier rufen wir die Funktion zum Erstellen der Datenbanktabellen auf.
    """
    print("Starte Anwendung und erstelle Datenbanktabellen...")
    create_db_and_tables()
    yield
    print("Anwendung heruntergefahren.")

app = FastAPI(lifespan=lifespan, title="AstroDate API")

@app.get("/")
def read_root():
    """
    Ein einfacher Endpunkt zur Überprüfung, ob die API läuft.
    """
    return {"message": "Willkommen zur AstroDate API!"}

