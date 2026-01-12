from sqlmodel import create_engine, Session, SQLModel, select
from typing import Generator

# Wichtig: Importiere die Modelle, damit SQLModel sie "sieht",
# bevor `create_all` aufgerufen wird.
# noinspection PyUnresolvedReferences
# pylint: disable=import-error
from models import ZodiacSign, ZodiacCompatibility  # type: ignore


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

def seed_zodiac_compatibility():
    """
    Füllt die ZodiacCompatibility-Tabelle mit den Kompatibilitätsdaten unter Verwendung von Fremdschlüsseln.
    Die Tabelle wird bei jedem Start geleert und neu gefüllt, um Konsistenz zu gewährleisten.
    Jede Kompatibilität wird in beide Richtungen gespeichert (bidirektional).
    """
    with Session(engine) as session:
        # 1. Vorhandene Einträge löschen
        existing_entries = session.exec(select(ZodiacCompatibility)).all()
        if existing_entries:
            print("Lösche vorhandene Kompatibilitätseinträge...")
            for entry in existing_entries:
                session.delete(entry)
            session.commit()
        
        print("Fülle die ZodiacCompatibility-Tabelle mit den Kompatibilitätsdaten...")

        # 2. Alle Sternzeichen abrufen, um eine Namens-zu-ID-Zuordnung zu erstellen
        all_signs = session.exec(select(ZodiacSign)).all()
        if not all_signs:
            print("Warnung: ZodiacSign-Tabelle ist leer. Überspringe das Seeding der Kompatibilität.")
            return
            
        signs_by_german_name = {sign.german_name: sign.id for sign in all_signs}

        # 3. Kompatibilitätsdaten basierend auf deutschen Namen
        compatibility_data = {
            "Widder": ["Löwe", "Schütze", "Zwillinge", "Waage", "Wassermann"],
            "Stier": ["Jungfrau", "Steinbock", "Krebs", "Skorpion", "Fische"],
            "Zwillinge": ["Waage", "Wassermann", "Widder", "Löwe", "Schütze"],
            "Krebs": ["Skorpion", "Fische", "Stier", "Jungfrau", "Steinbock"],
            "Löwe": ["Widder", "Schütze", "Zwillinge", "Waage", "Wassermann"],
            "Jungfrau": ["Stier", "Steinbock", "Krebs", "Skorpion", "Fische"],
            "Waage": ["Zwillinge", "Wassermann", "Widder", "Löwe", "Schütze"],
            "Skorpion": ["Krebs", "Fische", "Stier", "Jungfrau", "Steinbock"],
            "Schütze": ["Widder", "Löwe", "Zwillinge", "Waage", "Wassermann"],
            "Steinbock": ["Stier", "Jungfrau", "Krebs", "Skorpion", "Fische"],
            "Wassermann": ["Zwillinge", "Waage", "Widder", "Löwe", "Schütze"],
            "Fische": ["Krebs", "Skorpion", "Stier", "Jungfrau", "Steinbock"],
        }
        
        # 4. Kompatibilitätseinträge mit IDs erstellen
        compatibility_entries = []
        seen_pairs = set()

        for sign_1_name, compatible_signs_names in compatibility_data.items():
            for sign_2_name in compatible_signs_names:
                sign_1_id = signs_by_german_name.get(sign_1_name)
                sign_2_id = signs_by_german_name.get(sign_2_name)

                if sign_1_id is None or sign_2_id is None:
                    continue

                pair = tuple(sorted((sign_1_id, sign_2_id)))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    # Fügt beide Richtungen hinzu, um die Abfrage zu vereinfachen
                    compatibility_entries.append(ZodiacCompatibility(sign_1_id=sign_1_id, sign_2_id=sign_2_id))
                    compatibility_entries.append(ZodiacCompatibility(sign_1_id=sign_2_id, sign_2_id=sign_1_id))
        
        session.add_all(compatibility_entries)
        session.commit()
        print(f"ZodiacCompatibility-Tabelle erfolgreich gefüllt mit {len(compatibility_entries)} Einträgen.")

def get_session() -> Generator[Session, None, None]:
    """
    Stellt eine Datenbank-Session bereit, die in FastAPI Abhängigkeiten verwendet werden kann.
    Die Session wird nach Gebrauch automatisch geschlossen.
    """
    with Session(engine) as session:
        yield session
