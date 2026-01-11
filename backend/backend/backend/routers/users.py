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
    compatible_user = crud.get_compatible_user(db=db, current_user_id=current_user.id)
    
    if compatible_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kein kompatibler Benutzer gefunden."
        )
    
    return compatible_user
