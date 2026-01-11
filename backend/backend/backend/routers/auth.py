from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta, date

from database import get_session
from models import UserCreate, UserRead, Token
from crud import get_user_by_email, create_user
from security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# English comments are used in the code as requested.
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_new_user(*, session: Session = Depends(get_session), user_in: UserCreate):
    """
    Create a new user.
    Validates that birth_date is provided, not in the future, and user is at least 18 years old.
    """
    # Validate that birth_date is provided
    if not user_in.birth_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Birth date is required.",
        )
    
    # Validate that birth_date is not in the future
    today = date.today()
    if user_in.birth_date > today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Birth date cannot be in the future.",
        )
    
    # Validate minimum age (18 years)
    age = today.year - user_in.birth_date.year - ((today.month, today.day) < (user_in.birth_date.month, user_in.birth_date.day))
    if age < 18:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must be at least 18 years old to register.",
        )
    
    user = get_user_by_email(db=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists in the system.",
        )
    
    new_user = create_user(db=session, user=user_in)
    return new_user

@router.post("/login", response_model=Token)
def login_for_access_token(
    *,
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = get_user_by_email(db=session, email=form_data.username) # OAuth2 form uses 'username' field for email
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    """
    Placeholder for logout. In a stateless token-based auth,
    the client just needs to delete the token.
    """
    return {"message": "Logout successful. Please delete your token."}
