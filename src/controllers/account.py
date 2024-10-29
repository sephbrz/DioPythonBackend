from fastapi import APIRouter, Depends

from src.schemas.account import AccountIn
from src.views.account import AccountOut
from src.services.account import AccountService
from src.security import login_required
from typing import Annotated

router = APIRouter(prefix="/accounts")

service = AccountService()


@router.get("/{id}", response_model=AccountOut)
async def read_account_by_id(
    id: int,
    user_id: Annotated[int, Depends(login_required)],
):
    return await service.read(id, user_id)


@router.post("/", response_model=AccountOut)
async def create_account(
    accountData: AccountIn,
    user_id: Annotated[int, Depends(login_required)],
):
    return await service.create(accountData, user_id)
