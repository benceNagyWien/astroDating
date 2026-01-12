from sqlmodel import Session, select
from datetime import date, datetime
import random
from typing import List, Optional

# Corrected absolute imports
from models import User, UserCreate, ZodiacSign, ZodiacCompatibility, Match
from security import get_password_hash

# --- User Functions ---

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Fetches a user by their email address."""
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Retrieves a list of users with pagination."""
    statement = select(User).offset(skip).limit(limit)
    return db.exec(statement).all()

def create_user(db: Session, user: UserCreate, all_signs: List[ZodiacSign]) -> User:
    """Creates a new user, efficiently determining the zodiac sign from a pre-fetched list."""
    hashed_password = get_password_hash(user.password)
    zodiac_sign = determine_zodiac_sign_for_date(user.birth_date, all_signs)
    
    db_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password,
        zodiac_sign_id=zodiac_sign.id if zodiac_sign else None
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Zodiac & Compatibility Functions ---

def determine_zodiac_sign_for_date(birth_date: date, signs: List[ZodiacSign]) -> Optional[ZodiacSign]:
    """
    (Pure function) Determines the Western Zodiac sign for a birth date from a list of signs.
    """
    for sign in signs:
        if sign.start_month <= sign.end_month:
            if (birth_date.month == sign.start_month and birth_date.day >= sign.start_day) or \
               (birth_date.month == sign.end_month and birth_date.day <= sign.end_day) or \
               (sign.start_month < birth_date.month < sign.end_month):
                return sign
        else:
            if (birth_date.month == sign.start_month and birth_date.day >= sign.start_day) or \
               (birth_date.month > sign.start_month) or \
               (birth_date.month == sign.end_month and birth_date.day <= sign.end_day) or \
               (birth_date.month < sign.end_month):
                return sign
    return None

def get_compatible_user(db: Session, current_user: User) -> Optional[User]:
    """
    Finds a random, compatible user who the current user has not yet swiped on.
    """
    if not current_user or not current_user.zodiac_sign_id:
        return None

    compatible_sign_ids_query = select(ZodiacCompatibility.sign_2_id).where(
        ZodiacCompatibility.sign_1_id == current_user.zodiac_sign_id
    )
    compatible_sign_ids = set(db.exec(compatible_sign_ids_query).all())
    if not compatible_sign_ids:
        return None

    swiped_user_ids_query = select(Match.user_id_to).where(Match.user_id_from == current_user.id)
    swiped_user_ids = set(db.exec(swiped_user_ids_query).all())
    swiped_user_ids.add(current_user.id)

    candidates = db.exec(
        select(User).where(
            User.zodiac_sign_id.in_(compatible_sign_ids), # type: ignore
            User.id.not_in(swiped_user_ids) # type: ignore
        )
    ).all()
    
    return random.choice(candidates) if candidates else None

# --- Match (Like/Swipe) Functions ---

def create_match(db: Session, user_id_from: int, user_id_to: int, is_like: bool) -> Match:
    """Creates a new Match record in the database."""
    existing_match = db.exec(
        select(Match).where(Match.user_id_from == user_id_from, Match.user_id_to == user_id_to)
    ).first()
    if existing_match:
        return existing_match

    match = Match(user_id_from=user_id_from, user_id_to=user_id_to, is_like=is_like)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

def get_users_who_liked_me(db: Session, current_user_id: int) -> List[User]:
    """Returns a list of users who have liked the current user."""
    user_ids = db.exec(
        select(Match.user_id_from).where(Match.user_id_to == current_user_id, Match.is_like == True)
    ).all()
    if not user_ids:
        return []
        
    return db.exec(select(User).where(User.id.in_(user_ids))).all() # type: ignore

def get_users_i_liked(db: Session, current_user_id: int) -> List[User]:
    """Returns a list of users that the current user has liked."""
    user_ids = db.exec(
        select(Match.user_id_to).where(Match.user_id_from == current_user_id, Match.is_like == True)
    ).all()
    if not user_ids:
        return []

    return db.exec(select(User).where(User.id.in_(user_ids))).all() # type: ignore