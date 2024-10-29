from pydantic import AwareDatetime, BaseModel, NaiveDatetime


class AccountOut(BaseModel):
    id: int
    id_user: int
    balance: float
    created_at: AwareDatetime | NaiveDatetime
