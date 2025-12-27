from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

# Wichtig: Importiere die Modelle, damit SQLModel sie "sieht",
# bevor `create_all` aufgerufen wird.
from backend import models


# NOTE: Comments are in German as per DEVELOPMENT_GUIDELINES.md

# Die SQLite Datenbank-URL
# TODO: Dies sollte später aus Umgebungsvariablen oder einer Konfigurationsdatei geladen werden.
DATABASE_URL = "sqlite:///./astrodate.db"

# Erstelle die SQLAlchemy Engine
# connect_args={"check_same_thread": False} ist notwendig für SQLite mit FastAPI,
# da FastAPI mehrere Threads verwendet und SQLite standardmäßig nicht darauf ausgelegt ist.
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """
    Erstellt alle Tabellen in der Datenbank basierend auf den SQLModel Metadaten.
    Diese Funktion sollte beim Start der Anwendung aufgerufen werden.
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Stellt eine Datenbank-Session bereit, die in FastAPI Abhängigkeiten verwendet werden kann.
    Die Session wird nach Gebrauch automatisch geschlossen.
    """
    with Session(engine) as session:
        yield session
