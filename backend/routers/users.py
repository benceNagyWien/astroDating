from fastapi import APIRouter

# English comments are used in the code as requested.
# This router will handle user interaction endpoints like discover, swipe, and matches.
router = APIRouter(
    prefix="/users",
    tags=["Users & Matching"],
)

@router.get("/")
async def read_users_root():
    """
    A placeholder endpoint to confirm the users router is working.
    """
    return {"message": "Users router is active."}
