from pydantic import AwareDatetime, BaseModel, PositiveFloat


class TransactionIn(BaseModel):
    id_account: int
    amount: PositiveFloat
