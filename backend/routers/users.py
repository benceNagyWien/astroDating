from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from typing import List

from database import get_session
from models import UserRead, User, ZodiacSign, Match # Added Match import
from security import decode_access_token
import crud

# This router handles user interaction endpoints like discover, swipe, and matches.
router = APIRouter(prefix="/users", tags=["Users & Matching"])

# Security scheme for authorization
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
) -> User:
    """Dependency to get the current user from a JWT token."""
    token = credentials.credentials
    payload = decode_access_token(token)
    email: str | None = payload.get("sub")
    
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    user = crud.get_user_by_email(db=db, email=email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user

# --- Helper function to reduce code duplication and fix N+1 query problem ---
def _convert_users_to_user_read_list(db: Session, users: List[User]) -> List[UserRead]:
    """
    Efficiently converts a list of User objects to a list of UserRead objects,
    avoiding N+1 queries for zodiac signs.
    """
    if not users:
        return []

    sign_ids = {user.zodiac_sign_id for user in users if user.zodiac_sign_id}
    
    if not sign_ids: # Handle case where no users have a zodiac sign
        return [UserRead(**user.model_dump()) for user in users]

    signs = db.exec(select(ZodiacSign).where(ZodiacSign.id.in_(sign_ids))).all() # type: ignore
    signs_map = {sign.id: sign.german_name for sign in signs}
    
    user_read_list = []
    for user in users:
        user_read_list.append(
            UserRead(
                **user.model_dump(),
                zodiac_sign_name=signs_map.get(user.zodiac_sign_id)
            )
        )
    return user_read_list

# --- API Endpoints ---

@router.get("/all", response_model=List[UserRead])
def read_all_users(db: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    """Retrieves a list of all users."""
    users = crud.get_users(db, skip=skip, limit=limit)
    return _convert_users_to_user_read_list(db, users)

@router.get("/discover", response_model=UserRead)
def discover_compatible_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    """Returns a random, compatible user for the current user to swipe on."""
    compatible_user = crud.get_compatible_user(db=db, current_user=current_user)
    
    if compatible_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No compatible users found at the moment.")
    
    return _convert_users_to_user_read_list(db, [compatible_user])[0]

@router.post("/swipe/{user_id}/{is_like}")
def swipe_user(
    user_id: int,
    is_like: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Records a swipe (like or dislike) on another user."""
    # Assert that the current user has an ID for type safety
    assert current_user.id is not None
    
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot swipe on yourself.")
    
    target_user = db.get(User, user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User to swipe on not found.")
    
    match = crud.create_match(db=db, user_id_from=current_user.id, user_id_to=user_id, is_like=is_like)
    
    if is_like:
        reverse_match = db.exec(
            select(Match).where(
                Match.user_id_from == user_id, 
                Match.user_id_to == current_user.id, 
                Match.is_like == True
            )
        ).first()
        if reverse_match:
            return {"message": "It's a mutual match!", "match_id": match.id}
            
    return {"message": "Swipe recorded successfully.", "match_id": match.id}

@router.get("/likes", response_model=List[UserRead])
def get_users_who_liked_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    """Returns a list of users who have liked the current user."""
    assert current_user.id is not None
    users = crud.get_users_who_liked_me(db=db, current_user_id=current_user.id)
    return _convert_users_to_user_read_list(db, users)

@router.get("/my-likes", response_model=List[UserRead])
def get_users_i_liked(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    """Returns a list of users that the current user has liked."""
    assert current_user.id is not None
    users = crud.get_users_i_liked(db=db, current_user_id=current_user.id)
    return _convert_users_to_user_read_list(db, users)
