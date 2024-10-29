from typing import Annotated
from fastapi import APIRouter, Depends

from src.security import login_required
from src.schemas.transaction import TransactionIn
from src.services.transaction import TransactionService
from src.views.transaction import TransactionOut

router = APIRouter(prefix="/transactions")

service = TransactionService()


@router.get("/{id}", response_model=TransactionOut)
async def read_transaction(
    id: int,
    user_id: Annotated[int, Depends(login_required)],
):
    return await service.read_by_id(id, user_id)


@router.post("/deposit/", response_model=TransactionOut)
async def create_deposit(
    transactionData: TransactionIn,
    user_id: Annotated[int, Depends(login_required)],
):
    return await service.create(transactionData, user_id, "Deposit")


@router.get("/", response_model=list[TransactionOut])
async def read_all_transactions(
    account_id: int,
    user_id: Annotated[int, Depends(login_required)],
    limit: int,
    skip: int = 0,
):
    return await service.read_all(account_id, user_id, limit, skip)


@router.post("/withdraw", response_model=TransactionOut)
async def create_withdraw(
    transactionData: TransactionIn,
    user_id: Annotated[int, Depends(login_required)],
):
    return await service.create(transactionData, user_id, "Withdraw")
