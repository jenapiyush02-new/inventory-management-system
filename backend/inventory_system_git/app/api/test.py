from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "username": current_user.username,
        "role": current_user.role,
    }