from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# ======================================================================================
# NOTE: The database schema is now based on the Chinese Zodiac.
# The column names are in English as per the development guidelines.
# The data stored within, such as 'german_name', will be in German for the frontend.
# ======================================================================================

# Schema for the login response
class Token(SQLModel):
    access_token: str
    token_type: str

# Schema for the data encoded in the JWT
class TokenData(SQLModel):
    username: str | None = None

class ZodiacSign(SQLModel, table=True):
    """
    Represents one of the 12 Chinese Zodiac signs.
    The ID corresponds to the result of `year % 12`.
    """
    id: int = Field(primary_key=True)
    english_name: str = Field(index=True, unique=True)
    german_name: str = Field(unique=True)
    
    users: List["User"] = Relationship(back_populates="zodiac_sign")

# Shared properties for a user
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    birth_year: int = Field(index=True)
    bio: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return via API, without the password
class UserRead(UserBase):
    id: int
    zodiac_sign_id: Optional[int] = None

# Database model for the User
class User(UserBase, table=True):
    """
    Represents a user in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    
    # Foreign key relationship to the ZodiacSign table.
    # This will be calculated by the backend after user registration.
    zodiac_sign_id: Optional[int] = Field(default=None, foreign_key="zodiacsign.id")
    zodiac_sign: Optional[ZodiacSign] = Relationship(back_populates="users")

class ZodiacCompatibility(SQLModel, table=True):
    """
    a `zodiac_sign` szöveges mezőt lecserélem egy `zodiac_sign_id` numerikus hivatkozásra, ami sokkal szakszerűbb megoldás.    A static lookup table defining which zodiac signs are compatible.
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