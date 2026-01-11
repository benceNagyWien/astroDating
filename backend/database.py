from sqlmodel import create_engine, Session, SQLModel, select
from typing import Generator

# Wichtig: Importiere die Modelle, damit SQLModel sie "sieht",
# bevor `create_all` aufgerufen wird.
# noinspection PyUnresolvedReferences
from .models import User, ZodiacSign, ZodiacCompatibility, Match


# NOTE: Comments are in German as per DEVELOPMENT_GUIDELINES.md

# Die SQLite Datenbank-URL
DATABASE_URL = "sqlite:///./astrodate.db"

# Erstelle die SQLAlchemy Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """
    Erstellt alle Tabellen in der Datenbank basierend auf den SQLModel Metadaten.
    Diese Funktion sollte beim Start der Anwendung aufgerufen werden.
    """
    SQLModel.metadata.create_all(engine)

def seed_zodiac_signs():
    """
    Füllt die ZodiacSign-Tabelle mit den 12 westlichen Tierkreiszeichen und ihren Datumsgrenzen,
    falls die Tabelle leer ist.
    """
    with Session(engine) as session:
        statement = select(ZodiacSign)
        results = session.exec(statement).first()
        
        if results is None:
            print("Fülle die ZodiacSign-Tabelle mit den Anfangsdaten (westliche Tierkreiszeichen)...")
            
            zodiac_data = [
                ZodiacSign(english_name="Aries", german_name="Widder", start_month=3, start_day=21, end_month=4, end_day=19),
                ZodiacSign(english_name="Taurus", german_name="Stier", start_month=4, start_day=20, end_month=5, end_day=20),
                ZodiacSign(english_name="Gemini", german_name="Zwillinge", start_month=5, start_day=21, end_month=6, end_day=20),
                ZodiacSign(english_name="Cancer", german_name="Krebs", start_month=6, start_day=21, end_month=7, end_day=22),
                ZodiacSign(english_name="Leo", german_name="Löwe", start_month=7, start_day=23, end_month=8, end_day=22),
                ZodiacSign(english_name="Virgo", german_name="Jungfrau", start_month=8, start_day=23, end_month=9, end_day=22),
                ZodiacSign(english_name="Libra", german_name="Waage", start_month=9, start_day=23, end_month=10, end_day=22),
                ZodiacSign(english_name="Scorpio", german_name="Skorpion", start_month=10, start_day=23, end_month=11, end_day=21),
                ZodiacSign(english_name="Sagittarius", german_name="Schütze", start_month=11, start_day=22, end_month=12, end_day=21),
                ZodiacSign(english_name="Capricorn", german_name="Steinbock", start_month=12, start_day=22, end_month=1, end_day=19),
                ZodiacSign(english_name="Aquarius", german_name="Wassermann", start_month=1, start_day=20, end_month=2, end_day=18),
                ZodiacSign(english_name="Pisces", german_name="Fische", start_month=2, start_day=19, end_month=3, end_day=20),
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
