from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import List

import crud
from database import get_session
from models import UserRead, User
from security import decode_access_token
from crud import get_user_by_email


# English comments are used in the code as requested.
# This router will handle user interaction endpoints like discover, swipe, and matches.
router = APIRouter(
    prefix="/users",
    tags=["Users & Matching"],
)

# HTTP Bearer token security scheme
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
) -> User:
    """
    Dependency-Funktion, die den aktuell eingeloggten Benutzer aus dem JWT Token extrahiert.
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    email: str | None = payload.get("sub")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_email(db=db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.get("/all", response_model=List[UserRead])
def read_all_users(db: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    """
    Ruft eine Liste aller Benutzer ab.
    Dies ist ein grundlegender Endpunkt, um potenzielle Partner für das Frontend bereitzustellen.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/")
async def read_users_root():
    """
    A placeholder endpoint to confirm the users router is working.
    """
    return {"message": "Users router is active."}

@router.get("/discover", response_model=UserRead)
def discover_compatible_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Gibt einen zufälligen kompatiblen Benutzer zurück, basierend auf dem Sternzeichen des eingeloggten Benutzers.
    Erfordert Authentifizierung via Bearer Token.
    """
    from models import ZodiacSign
    
    compatible_user = crud.get_compatible_user(db=db, current_user_id=current_user.id)
    
    if compatible_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kein kompatibler Benutzer gefunden."
        )
    
    # Hole den Namen des Sternzeichens
    zodiac_sign_name = None
    if compatible_user.zodiac_sign_id:
        zodiac_sign = db.get(ZodiacSign, compatible_user.zodiac_sign_id)
        if zodiac_sign:
            zodiac_sign_name = zodiac_sign.german_name
    
    # Erstelle UserRead mit Sternzeichen-Name
    user_read = UserRead(
        id=compatible_user.id,
        email=compatible_user.email,
        birth_date=compatible_user.birth_date,
        bio=compatible_user.bio,
        image_filename=compatible_user.image_filename,
        zodiac_sign_id=compatible_user.zodiac_sign_id,
        zodiac_sign_name=zodiac_sign_name
    )
    
    return user_read

@router.post("/like/{user_id}")
def like_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Like-olt einen Benutzer. Erstellt einen Match-Eintrag in der Datenbank.
    Erfordert Authentifizierung via Bearer Token.
    """
    # Prüfe ob der Benutzer existiert
    target_user = db.get(User, user_id)
    if target_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benutzer nicht gefunden."
        )
    
    # Prüfe ob der Benutzer sich nicht selbst liked
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Du kannst dich nicht selbst liken."
        )
    
    # Erstelle den Match-Eintrag
    match = crud.create_match(
        db=db,
        user_id_from=current_user.id,
        user_id_to=user_id,
        is_like=True
    )
    
    return {"message": "Benutzer erfolgreich geliked.", "match_id": match.id}

@router.get("/likes", response_model=List[UserRead])
def get_users_who_liked_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Gibt eine Liste von Benutzern zurück, die den aktuellen Benutzer geliked haben.
    Erfordert Authentifizierung via Bearer Token.
    """
    from models import ZodiacSign
    
    users_who_liked = crud.get_users_who_liked_me(db=db, current_user_id=current_user.id)
    
    # Konvertiere zu UserRead mit Sternzeichen-Name
    result = []
    for user in users_who_liked:
        zodiac_sign_name = None
        if user.zodiac_sign_id:
            zodiac_sign = db.get(ZodiacSign, user.zodiac_sign_id)
            if zodiac_sign:
                zodiac_sign_name = zodiac_sign.german_name
        
        user_read = UserRead(
            id=user.id,
            email=user.email,
            birth_date=user.birth_date,
            bio=user.bio,
            image_filename=user.image_filename,
            zodiac_sign_id=user.zodiac_sign_id,
            zodiac_sign_name=zodiac_sign_name
        )
        result.append(user_read)
    
    return result
