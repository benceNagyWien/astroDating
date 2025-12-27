from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.database import get_session
from backend.models import UserCreate, UserRead
from backend.crud import get_user_by_email, create_user

# English comments are used in the code as requested.
# This router will handle authentication-related endpoints like login, logout, and register.
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_new_user(*, session: Session = Depends(get_session), user_in: UserCreate):
    """
    Create a new user.
    """
    # Check if a user with this email already exists
    user = get_user_by_email(db=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists in the system.",
        )
    
    # Create the new user in the database
    new_user = create_user(db=session, user=user_in)
    return new_user
