from sqlmodel import create_engine, Session, SQLModel, select
from typing import Generator

# Wichtig: Importiere die Modelle, damit SQLModel sie "sieht",
# bevor `create_all` aufgerufen wird.
from backend.models import ZodiacSign


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

def seed_zodiac_signs():
    """
    Füllt die ZodiacSign-Tabelle mit den 12 chinesischen Tierkreiszeichen,
    falls die Tabelle leer ist.
    """
    with Session(engine) as session:
        # Überprüfen, ob die Tabelle bereits Daten enthält
        statement = select(ZodiacSign)
        results = session.exec(statement).first()
        
        if results is None:
            print("Fülle die ZodiacSign-Tabelle mit den Anfangsdaten...")
            
            # Die ID entspricht dem Ergebnis von `jahr % 12`
            zodiac_data = [
                ZodiacSign(id=0, english_name="Monkey", german_name="Affe"),
                ZodiacSign(id=1, english_name="Rooster", german_name="Hahn"),
                ZodiacSign(id=2, english_name="Dog", german_name="Hund"),
                ZodiacSign(id=3, english_name="Pig", german_name="Schwein"),
                ZodiacSign(id=4, english_name="Rat", german_name="Ratte"),
                ZodiacSign(id=5, english_name="Ox", german_name="Büffel"),
                ZodiacSign(id=6, english_name="Tiger", german_name="Tiger"),
                ZodiacSign(id=7, english_name="Rabbit", german_name="Hase"),
                ZodiacSign(id=8, english_name="Dragon", german_name="Drache"),
                ZodiacSign(id=9, english_name="Snake", german_name="Schlange"),
                ZodiacSign(id=10, english_name="Horse", german_name="Pferd"),
                ZodiacSign(id=11, english_name="Goat", german_name="Ziege"),
            ]
            
            session.add_all(zodiac_data)
            session.commit()
            print("ZodiacSign-Tabelle erfolgreich gefüllt.")

def get_session() -> Generator[Session, None, None]:
    """
    Stellt eine Datenbank-Session bereit, die in FastAPI Abhängigkeiten verwendet werden kann.
    Die Session wird nach Gebrauch automatisch geschlossen.
    """
    with Session(engine) as session:
        yield session
