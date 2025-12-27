from fastapi import APIRouter

# English comments are used in the code as requested.
# This router will handle authentication-related endpoints like login, logout, and register.
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.get("/")
async def read_auth_root():
    """
    A placeholder endpoint to confirm the auth router is working.
    """
    return {"message": "Authentication router is active."}
