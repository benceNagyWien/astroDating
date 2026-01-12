"""
Script zum Erstellen von 4 Test-Benutzern mit kompatiblen Sternzeichen.
Alle 4 Benutzer sind untereinander kompatibel (Widder, Löwe, Schütze, Zwillinge).
"""
from datetime import date
from sqlmodel import Session
from database import engine
from crud import create_user
from models import UserCreate

# Benutzer-Daten: Email, Passwort, Geburtsdatum (für kompatible Sternzeichen), Bild-Dateiname
# Widder: März 21 - April 19
# Löwe: Juli 23 - August 22
# Schütze: November 22 - Dezember 21
# Zwillinge: Mai 21 - Juni 20

users_data = [
    {
        "email": "a@a.a",
        "password": "a",
        "birth_date": date(1995, 4, 10),  # Widder
        "bio": "Mystischer Astrologe mit Kristallkugel",
        "image_filename": "user_a.jpg"
    },
    {
        "email": "b@b.b",
        "password": "b",
        "birth_date": date(1993, 8, 5),  # Löwe
        "bio": "Erfahrener Tarot-Leser und Astrologe",
        "image_filename": "user_b.jpg"
    },
    {
        "email": "c@c.c",
        "password": "c",
        "birth_date": date(1990, 12, 10),  # Schütze
        "bio": "Freundlicher Astrologe mit kosmischer Energie",
        "image_filename": "user_c.jpg"
    },
    {
        "email": "d@d.d",
        "password": "d",
        "birth_date": date(1992, 6, 5),  # Zwillinge
        "bio": "Mächtiger Astrologe mit spiritueller Kraft",
        "image_filename": "user_d.jpg"
    }
]

with Session(engine) as session:
    for user_data in users_data:
        # Prüfe ob Benutzer bereits existiert
        from crud import get_user_by_email
        existing_user = get_user_by_email(session, user_data["email"])
        
        if existing_user:
            print(f"Benutzer {user_data['email']} existiert bereits. Überspringe...")
            continue
        
        # Erstelle UserCreate Objekt
        user_create = UserCreate(
            email=user_data["email"],
            password=user_data["password"],
            birth_date=user_data["birth_date"],
            bio=user_data["bio"],
            image_filename=user_data["image_filename"]
        )
        
        # Erstelle den Benutzer
        created_user = create_user(session, user_create)
        print(f"Benutzer erstellt: {created_user.email} (ID: {created_user.id}, Sternzeichen-ID: {created_user.zodiac_sign_id})")

print("\nAlle Test-Benutzer wurden erfolgreich erstellt!")
print("Kompatibilität: Widder, Löwe, Schütze, Zwillinge sind alle untereinander kompatibel.")

