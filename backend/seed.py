# Deutsche Kommentare gemäß den Entwicklungsrichtlinien.

import os
import random
from faker import Faker
from sqlmodel import Session
from datetime import date, timedelta

from database import engine, create_db_and_tables, seed_zodiac_signs, seed_zodiac_compatibility
from models import User, UserCreate
from security import get_password_hash
from crud import get_zodiac_sign_by_date, create_user, get_user_by_email

# Initialisiert den Faker-Generator für deutsche Daten
fake = Faker("de_DE")

def create_specific_test_users(db: Session):
    """
    Erstellt 4 vordefinierte, untereinander kompatible Test-Benutzer, falls sie noch nicht existieren.
    Dies ist nützlich für manuelle Tests und Demonstrationen.
    """
    print("\nPrüfe und erstelle 4 spezifische Test-Benutzer...")

    users_data = [
        {"email": "a@a.a", "password": "a", "birth_date": date(1995, 4, 10), "bio": "Mystischer Astrologe", "image_filename": "user_a.jpg"},
        {"email": "b@b.b", "password": "b", "birth_date": date(1993, 8, 5), "bio": "Erfahrener Tarot-Leser", "image_filename": "user_b.jpg"},
        {"email": "c@c.c", "password": "c", "birth_date": date(1990, 12, 10), "bio": "Freundlicher Astrologe", "image_filename": "user_c.jpg"},
        {"email": "d@d.d", "password": "d", "birth_date": date(1992, 6, 5), "bio": "Mächtiger Astrologe", "image_filename": "user_d.jpg"}
    ]

    for user_data in users_data:
        if not get_user_by_email(db, user_data["email"]):
            user_create = UserCreate(**user_data)
            created_user = create_user(db, user_create)
            sign_name = created_user.zodiac_sign.german_name if created_user.zodiac_sign else 'N/A'
            print(f"Spezifischer Benutzer erstellt: {created_user.email} ({sign_name})")
        else:
            # This case is unlikely with the new auto-delete DB logic, but good practice.
            print(f"Spezifischer Benutzer {user_data['email']} existiert bereits. Überspringe...")
    
    print("Spezifisches Test-Benutzer-Seeding abgeschlossen.")


def create_fake_users(db: Session):
    """
    Erstellt 100 gefälschte, zufällige Benutzer und fügt sie der Datenbank hinzu.
    """
    print("\nStarte das Seeding von 100 zufälligen Benutzern...")
    
    image_files = [f"{i}.jpg" for i in range(1, 101)]
    random.shuffle(image_files)

    users_to_create = []
    for i, image_file in enumerate(image_files):
        birth_date = fake.date_between(start_date='-65y', end_date='-18y')
        zodiac_sign = get_zodiac_sign_by_date(db, birth_date)
        
        user = User(
            email=fake.email(),
            hashed_password=get_password_hash("password123"),
            birth_date=birth_date,
            bio=fake.paragraph(nb_sentences=3),
            image_filename=image_file,
            zodiac_sign=zodiac_sign
        )
        users_to_create.append(user)

    db.add_all(users_to_create)
    db.commit() # Commit all 100 users at once for efficiency
    print("Seeding von 100 zufälligen Benutzern erfolgreich abgeschlossen.")


if __name__ == "__main__":
    print("Initialisiere die Datenbank und die statischen Daten...")
    create_db_and_tables()
    
    seed_zodiac_signs()
    seed_zodiac_compatibility()
    
    print("Datenbank initialisiert.")

    with Session(engine) as session:
        print("\nWähle eine Seeding-Methode:")
        print("1: 4 spezifische Test-Benutzer erstellen")
        print("2: 100 zufällige Fake-Benutzer erstellen")
        print("3: Alle Benutzer erstellen (100 zufällige + 4 spezifische)")
        choice = input("Auswahl (1, 2, oder 3): ")
        
        if choice == '1':
            create_specific_test_users(session)
        elif choice == '2':
            create_fake_users(session)
        elif choice == '3':
            create_fake_users(session)
            create_specific_test_users(session)
        else:
            print("Ungültige Auswahl.")