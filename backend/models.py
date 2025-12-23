from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

# ======================================================================================
# NOTE: The column names are in English as per the development guidelines.
# The data stored within, such as 'zodiac_sign', will be in German for the frontend.
# ======================================================================================

class User(SQLModel, table=True):
    """
    Represents a user in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    birth_year: int = Field(index=True, nullable=False)
    zodiac_sign: str = Field(index=True) # Will store the German name of the sign
    bio: Optional[str] = None

class ZodiacCompatibility(SQLModel, table=True):
    """
    A static lookup table defining which zodiac signs are compatible.
    e.g., sign_1: 'Rat', sign_2: 'Dragon'
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    sign_1: str = Field(index=True, nullable=False)
    sign_2: str = Field(index=True, nullable=False)

class Match(SQLModel, table=True):
    """
    Represents a swipe action from one user to another.
    A mutual match occurs when two users have a 'like' record for each other.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # The user who performed the swipe action
    user_id_from: int = Field(foreign_key="user.id", nullable=False, index=True)
    
    # The user who was swiped on
    user_id_to: int = Field(foreign_key="user.id", nullable=False, index=True)
    
    is_like: bool = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

