from typing import Optional
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship

# ======================================================================================
# NOTE: The database schema is now based on the Western (Tropical) Zodiac.
# ======================================================================================

# Gemeinsame Eigenschaften für einen Benutzer
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    birth_date: date
    bio: Optional[str] = None
    image_filename: Optional[str] = None  # Dateiname des Profilbildes

# Eigenschaften, die über die API bei der Erstellung empfangen werden
class UserCreate(UserBase):
    password: str

# Eigenschaften, die über die API zurückgegeben werden, ohne das Passwort
class UserRead(UserBase):
    id: int
    zodiac_sign_id: Optional[int] = None


class ZodiacSign(SQLModel, table=True):
    """
    Stellt eines der 12 westlichen Sternzeichen mit seinem Datumsbereich dar.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    english_name: str = Field(index=True, unique=True)
    german_name: str = Field(unique=True)
    start_month: int
    start_day: int
    end_month: int
    end_day: int
    
    users: list["User"] = Relationship(back_populates="zodiac_sign")

# Datenbankmodell für den Benutzer
class User(UserBase, table=True):
    """
    Stellt einen Benutzer in der Datenbank dar.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    
    # Fremdschlüsselbeziehung zur ZodiacSign-Tabelle.
    # Dies wird vom Backend nach der Benutzerregistrierung berechnet.
    zodiac_sign_id: Optional[int] = Field(default=None, foreign_key="zodiacsign.id")
    zodiac_sign: Optional[ZodiacSign] = Relationship(back_populates="users")

class ZodiacCompatibility(SQLModel, table=True):
    """
    Eine statische Nachschlagetabelle, die definiert, welche Sternzeichen kompatibel sind.
    z.B. sign_1: 'Aries', sign_2: 'Leo'
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    sign_1: str = Field(index=True, nullable=False)
    sign_2: str = Field(index=True, nullable=False)

class Match(SQLModel, table=True):
    """
    Stellt eine Swipe-Aktion von einem Benutzer zum anderen dar.
    Ein gegenseitiges Match tritt auf, wenn zwei Benutzer einen 'like'-Eintrag für den anderen haben.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Der Benutzer, der die Swipe-Aktion durchgeführt hat
    user_id_from: int = Field(foreign_key="user.id", nullable=False, index=True)
    
    # Der Benutzer, auf den geswiped wurde
    user_id_to: int = Field(foreign_key="user.id", nullable=False, index=True)
    
    is_like: bool = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# Schema für die Login-Antwort
class Token(SQLModel):
    access_token: str
    token_type: str

# Schema für die im JWT kodierten Daten
class TokenData(SQLModel):
    email: str | None = None


