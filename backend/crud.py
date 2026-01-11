from sqlmodel import Session, select
from datetime import date

from backend.models import User, UserCreate, ZodiacSign
from backend.security import get_password_hash

# English comments are used in the code as requested.

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """
    Ruft eine Liste von Benutzern aus der Datenbank ab.
    Unterstützt Paginierung durch Skip und Limit.
    """
    statement = select(User).offset(skip).limit(limit)
    return db.exec(statement).all()

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Fetches a user from the database by their email address.
    """
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()

def get_zodiac_sign_for_date(db: Session, birth_date: date) -> ZodiacSign | None:
    """
    Finds the correct zodiac sign for a given birth date.
    This logic handles signs that cross over the year-end (e.g., Capricorn).
    """
    month = birth_date.month
    day = birth_date.day
    
    # First, check for the special case of Capricorn, which spans Dec-Jan.
    # If the date is in late December or early January, it's Capricorn.
    capricorn_sign = db.exec(select(ZodiacSign).where(ZodiacSign.english_name == "Capricorn")).first()
    if capricorn_sign:
        if (month == capricorn_sign.start_month and day >= capricorn_sign.start_day) or \
           (month == capricorn_sign.end_month and day <= capricorn_sign.end_day):
            return capricorn_sign
    
    # For all other signs, they are within a simple date range (not crossing year-end).
    statement = select(ZodiacSign).where(
        (ZodiacSign.start_month == month and day >= ZodiacSign.start_day) |
        (ZodiacSign.end_month == month and day <= ZodiacSign.end_day)
    ).where(ZodiacSign.english_name != "Capricorn") # Exclude the special case
    
    return db.exec(statement).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    # Hash the password before saving
    hashed_password = get_password_hash(user.password)
    
    # Find the user's zodiac sign
    zodiac_sign = get_zodiac_sign_for_date(db, user.birth_date)
    
    # Create the User object for the database, excluding the plain password
    db_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password,
        zodiac_sign_id=zodiac_sign.id if zodiac_sign else None
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
