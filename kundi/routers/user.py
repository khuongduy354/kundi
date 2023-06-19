from fastapi import APIRouter, HTTPException, status
from firebase_admin import auth

from kundi.models.card import UserAuthPayload

router = APIRouter()


@router.post("/signup")
def signup_user(payload: UserAuthPayload):
    print(payload)
    try:
        user = auth.create_user(email=payload.email, password=payload.password,
                                display_name=payload.display_name, email_verified=True)
        return user
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
