from pydantic import AwareDatetime, BaseModel, NaiveDatetime, PositiveFloat


class TransactionOut(BaseModel):
    id: int
    id_account: int
    type: str
    amount: PositiveFloat
    timestamp: AwareDatetime | NaiveDatetime | None
