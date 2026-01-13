import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from models import ZodiacSign

# Importiere die notwendigen Funktionen und Router
from database import engine, create_db_and_tables, seed_zodiac_signs, seed_zodiac_compatibility
from routers import auth, users
from seed import create_fake_users, create_specific_test_users

# NOTE: Comments are in German as per DEVELOPMENT_GUIDELINES.md
DB_FILE = "./astrodate.db"

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Handles application startup.
    If the database does not exist, it creates it and seeds it with initial data.
    If the database already exists, it uses the existing one.
    """
    print("================== Anwendung startet ==================")
    if not os.path.exists(DB_FILE):
        print("Datenbank nicht gefunden. Initialisiere neue Datenbank...")
        
        # 1. Datenbank und Tabellen erstellen
        print("Erstelle Datenbank und Tabellen...")
        create_db_and_tables()
        
        # 2. Statische Daten füllen
        print("Fülle statische Daten (Tierkreiszeichen und Kompatibilität)...")
        seed_zodiac_signs()
        seed_zodiac_compatibility()
        
        # 3. Test-Benutzerdaten füllen (Seeding)
        print("Fülle Benutzerdaten (Seeding)...")
        with Session(engine) as session:
            all_zodiac_signs = session.exec(select(ZodiacSign)).all()
            create_fake_users(session, all_zodiac_signs)
            create_specific_test_users(session, all_zodiac_signs)
        
        print("================== DATENBANK-INITIALISIERUNG FERTIG ==================")
    else:
        print(f"Verwende existierende Datenbank: {DB_FILE}")
        
    yield
    print("Anwendung heruntergefahren.")

app = FastAPI(lifespan=lifespan, title="AstroDate API")

# Mount the directory for serving user images
app.mount("/userImages", StaticFiles(directory="userImages"), name="userImages")

# Set up CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:5173",  # The origin of our Vue.js frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Binde die Router in die Hauptanwendung ein
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    """
    Ein einfacher Endpunkt zur Überprüfung, ob die API läuft.
    """
    return {"message": "Willkommen zur AstroDate API!"}