from fastapi import FastAPI
from contextlib import asynccontextmanager

# Importiere die Funktionen aus unserer database.py
from backend.database import create_db_and_tables, seed_zodiac_signs

# NOTE: Comments are in German as per DEVELOPMENT_GUIDELINES.md

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Diese Funktion wird beim Starten der FastAPI Anwendung ausgeführt.
    Hier rufen wir die Funktionen zum Erstellen der Datenbanktabellen
    und zum Füllen der statischen Daten auf.
    """
    print("Starte Anwendung und erstelle Datenbanktabellen...")
    create_db_and_tables()
    print("Fülle statische Daten (Tierkreiszeichen)...")
    seed_zodiac_signs()
    yield
    print("Anwendung heruntergefahren.")

app = FastAPI(lifespan=lifespan, title="AstroDate API")

@app.get("/")
def read_root():
    """
    Ein einfacher Endpunkt zur Überprüfung, ob die API läuft.
    """
    return {"message": "Willkommen zur AstroDate API!"}

