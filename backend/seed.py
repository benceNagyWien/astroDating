# Deutsche Kommentare gemäß den Entwicklungsrichtlinien.

import os
import random
from faker import Faker
from sqlmodel import Session
from datetime import date, timedelta

from database import engine, create_db_and_tables, seed_zodiac_signs, seed_zodiac_compatibility
from models import User
from security import get_password_hash
from crud import get_zodiac_sign_by_date  # Importiere die neue Logik

# Initialisiert den Faker-Generator für deutsche Daten
fake = Faker("de_DE")

def create_fake_users(db: Session):
    """
    Erstellt 100 gefälschte Benutzer und fügt sie der Datenbank hinzu.
    Jedem Benutzer wird ein Profilbild aus dem Ordner /userImages/ zugewiesen
    und das korrekte Sternzeichen basierend auf dem Geburtsdatum zugewiesen.
    """
    print("Starte das Seeding von 100 Benutzern...")
    
    # Annahme: Es gibt 100 Bilder mit den Namen 1.jpg bis 100.jpg
    image_files = [f"{i}.jpg" for i in range(1, 101)]
    random.shuffle(image_files)

    for i, image_file in enumerate(image_files):
        # Generiert ein glaubwürdiges Geburtsdatum (18-65 Jahre alt)
        today = date.today()
        start_date = today - timedelta(days=65*365)
        end_date = today - timedelta(days=18*365)
        birth_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        # Ermittelt das korrekte Sternzeichen für das generierte Geburtsdatum
        zodiac_sign = get_zodiac_sign_by_date(db, birth_date)
        
        # Erstellt einen neuen Benutzer mit gefälschten Daten
        user = User(
            email=fake.email(),
            hashed_password=get_password_hash("password123"),  # Standardpasswort für alle
            birth_date=birth_date,
            bio=fake.paragraph(nb_sentences=3),
            image_filename=image_file,
            zodiac_sign=zodiac_sign  # Weise das gefundene Sternzeichen-Objekt zu
        )
        db.add(user)
        sign_name = zodiac_sign.german_name if zodiac_sign else "N/A"
        print(f"Benutzer {i+1}/{len(image_files)} erstellt: {user.email} ({sign_name}) mit Bild {user.image_filename}")

    db.commit()
    print("Seeding von 100 Benutzern erfolgreich abgeschlossen.")

if __name__ == "__main__":
    # Dieser Block wird nur ausgeführt, wenn das Skript direkt gestartet wird.
    print("Initialisiere die Datenbank und die statischen Daten...")
    create_db_and_tables()
    
    # Füllt die statischen Tabellen (Sternzeichen und Kompatibilität).
    # Diese Funktionen erstellen ihre eigene DB-Sitzung.
    seed_zodiac_signs()
    seed_zodiac_compatibility()
    
    print("Datenbank initialisiert.")

    # Erstellt eine neue Datenbanksitzung und führt das User-Seeding durch
    with Session(engine) as session:
        create_fake_users(session)
