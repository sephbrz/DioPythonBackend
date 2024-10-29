from src.database import database
from src.models.account import accountTable
from src.schemas.account import AccountIn
from src.exceptions import AccountNotFoundError, AuthorizationError


class AccountService:
    async def create(self, account: AccountIn, user_id: int) -> int:
        command = accountTable.insert().values(
            id_user=user_id,
            balance=account.balance,
        )
        account_id = await database.execute(command)
        query = accountTable.select().where(accountTable.c.id == account_id)
        return await database.fetch_one(query)

    async def read(self, account_id: int, user_id: int) -> int:
        query = accountTable.select().where(accountTable.c.id == account_id)
        account = await database.fetch_one(query)

        if not account:
            raise AccountNotFoundError

        if account.id_user == user_id:
            return account
        else:
            raise AuthorizationError("User is not authorized to access this account")

    async def update(self, account_id: int, balance: float) -> int:
        command = (
            accountTable.update()
            .where(accountTable.c.id == account_id)
            .values(balance=balance)
        )
        return await database.execute(command)
