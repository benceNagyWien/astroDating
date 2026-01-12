# Deutsche Kommentare gemäß den Entwicklungsrichtlinien.

import os
import random
from faker import Faker
from sqlmodel import Session
from datetime import date, timedelta

from database import engine, create_db_and_tables, seed_zodiac_signs
from models import User
from security import get_password_hash

# Initialisiert den Faker-Generator für deutsche Daten
fake = Faker("de_DE")

def create_fake_users(db: Session):
    """
    Erstellt 100 gefälschte Benutzer und fügt sie der Datenbank hinzu.
    Jedem Benutzer wird ein Profilbild aus dem Ordner /userImages/ zugewiesen.
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
        
        # Erstellt einen neuen Benutzer mit gefälschten Daten
        user = User(
            email=fake.unique.email(),
            hashed_password=get_password_hash("password123"),  # Standardpasswort für alle
            birth_date=birth_date,
            bio=fake.paragraph(nb_sentences=3),
            image_filename=image_file,
            zodiac_sign_id=random.randint(1, 12) # Weist ein zufälliges Sternzeichen zu
        )
        db.add(user)
        print(f"Benutzer {i+1}/100 erstellt: {user.email} mit Bild {user.image_filename}")

    db.commit()
    print("Seeding von 100 Benutzern erfolgreich abgeschlossen.")

if __name__ == "__main__":
    # Erstellt die Datenbank und die Tabellen
    print("Erstelle Datenbank und Tabellen...")
    create_db_and_tables()
    print("Datenbank und Tabellen erfolgreich erstellt.")
    
    # Füllt die ZodiacSign-Tabelle mit den Anfangsdaten
    seed_zodiac_signs()

    # Erstellt eine Datenbanksitzung und führt das User-Seeding durch
    with Session(engine) as session:
        create_fake_users(session)