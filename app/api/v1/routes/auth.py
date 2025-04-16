from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core.config import ADMIN_PASSWORD, ADMIN_USERNAME
from app.core.security import create_access_token
from app.api.errors import unauthorized_access

router = APIRouter(prefix="/v1/auth", tags=["Auth"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != ADMIN_USERNAME or form_data.password != ADMIN_PASSWORD:
        raise unauthorized_access()

    token = create_access_token(
        {"sub": form_data.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}
