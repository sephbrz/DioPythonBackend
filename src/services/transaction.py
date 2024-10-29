from databases.interfaces import Record

from src.exceptions import TransactionsNotFoundError, BusinessError
from src.database import database
from src.models.transaction import transactionTable
from src.schemas.transaction import TransactionIn
from src.services.account import AccountService

service = AccountService()


class TransactionService:
    async def create(
        self, transaction: TransactionIn, user_id: int, transactionType: str
    ) -> int:
        account = await service.read(transaction.id_account, user_id)

        if transactionType == "Withdraw":
            balance = float(account.balance) - transaction.amount
            if balance < 0:
                raise BusinessError("Operation not carried out due to lack of balance")
        else:
            balance = float(account.balance) + transaction.amount

        await service.update(transaction.id_account, balance)

        command = transactionTable.insert().values(
            type=transactionType,
            amount=transaction.amount,
            id_account=transaction.id_account,
        )
        transaction_id = await database.execute(command)
        query = transactionTable.select().where(transactionTable.c.id == transaction_id)
        return await database.fetch_one(query)

    async def read_by_id(self, id: int, user_id: int) -> Record:
        query = transactionTable.select().where(transactionTable.c.id == id)
        result = await database.fetch_one(query)
        account = await service.read(result.id_account, user_id)
        return result

    async def read_all(
        self, account_id: int, user_id: int, limit: int, skip: int = 0
    ) -> list[Record]:
        account = await service.read(account_id, user_id)

        query = (
            transactionTable.select()
            .where(transactionTable.c.id_account == account_id)
            .limit(limit)
            .offset(skip)
        )

        result = await database.fetch_all(query)

        if result:
            return result
        else:
            raise TransactionsNotFoundError
