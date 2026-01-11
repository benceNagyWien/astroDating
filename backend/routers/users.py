from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

import crud
from database import get_session
from models import UserRead


# English comments are used in the code as requested.
# This router will handle user interaction endpoints like discover, swipe, and matches.
router = APIRouter(
    prefix="/users",
    tags=["Users & Matching"],
)

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
