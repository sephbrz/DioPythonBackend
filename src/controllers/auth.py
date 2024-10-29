from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.views.auth import LoginOut
from src.security import authenticate_user

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginOut)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await authenticate_user(form_data.username, form_data.password)
