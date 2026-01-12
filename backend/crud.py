# This file was reconstructed by the Gemini CLI.
# It contains the essential CRUD (Create, Read, Update, Delete) operations.

from sqlmodel import Session, select
from typing import Optional
from datetime import date

# Import models and security functions from other modules in the application
from models import User, UserCreate, ZodiacSign
from security import get_password_hash


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Retrieves a single user from the database by their ID.
    """
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieves a single user from the database by their email address.
    """
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()


def get_zodiac_sign_by_date(db: Session, birth_date: date) -> Optional[ZodiacSign]:
    """
    Determines the Western Zodiac sign for a given birth date.
    This function handles signs that span across the new year (e.g., Capricorn).
    """
    signs = db.exec(select(ZodiacSign)).all()
    for sign in signs:
        # Case 1: The sign's date range is within the same year (e.g., Aries: Mar 21 - Apr 19)
        if sign.start_month <= sign.end_month:
            if (birth_date.month == sign.start_month and birth_date.day >= sign.start_day) or \
               (birth_date.month == sign.end_month and birth_date.day <= sign.end_day) or \
               (sign.start_month < birth_date.month < sign.end_month):
                return sign
        # Case 2: The sign's date range crosses over the new year (e.g., Capricorn: Dec 22 - Jan 19)
        else:
            if (birth_date.month == sign.start_month and birth_date.day >= sign.start_day) or \
               (birth_date.month > sign.start_month) or \
               (birth_date.month == sign.end_month and birth_date.day <= sign.end_day) or \
               (birth_date.month < sign.end_month):
                return sign
    return None


def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user in the database.
    - Hashes the plain-text password.
    - Determines the user's zodiac sign based on their birth date.
    - Saves the new user record.
    """
    # Hash the user's password for security
    hashed_password = get_password_hash(user.password)
    
    # Exclude the plain-text password and create a dictionary for the new user
    user_data = user.model_dump(exclude={"password"})
    
    # Find the corresponding zodiac sign
    zodiac_sign = get_zodiac_sign_by_date(db, user.birth_date)
    
    # Create the new User object
    db_user = User(**user_data, hashed_password=hashed_password, zodiac_sign=zodiac_sign)
    
    # Add the new user to the database session
    db.add(db_user)
    # Commit the changes to the database
    db.commit()
    # Refresh the object to get the newly created ID and other defaults
    db.refresh(db_user)
    
    return db_user