from typing import Optional
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship

# ======================================================================================
# NOTE: The database schema is now based on the Western (Tropical) Zodiac.
# ======================================================================================

# Shared properties for a user
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    birth_date: date
    bio: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return via API, without the password
class UserRead(UserBase):
    id: int
    zodiac_sign_id: Optional[int] = None

class ZodiacSign(SQLModel, table=True):
    """
    Represents one of the 12 Western Zodiac signs with its date range.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    english_name: str = Field(index=True, unique=True)
    german_name: str = Field(unique=True)
    start_month: int
    start_day: int
    end_month: int
    end_day: int
    
    users: list["User"] = Relationship(back_populates="zodiac_sign")

# Database model for the User
class User(UserBase, table=True):
    """
    Represents a user in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str
    
    # Foreign key relationship to the ZodiacSign table.
    # This will be calculated by the backend after user registration.
    zodiac_sign_id: Optional[int] = Field(default=None, foreign_key="zodiacsign.id")
    zodiac_sign: Optional[ZodiacSign] = Relationship(back_populates="users")

class ZodiacCompatibility(SQLModel, table=True):
    """

    A static lookup table defining which zodiac signs are compatible.
    e.g., sign_1: 'Aries', sign_2: 'Leo'
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

# Schema for the login response
class Token(SQLModel):
    access_token: str
    token_type: str

# Schema for the data encoded in the JWT
class TokenData(SQLModel):
    email: str | None = None