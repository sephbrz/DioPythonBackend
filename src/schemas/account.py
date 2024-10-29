from pydantic import PositiveFloat, BaseModel


class AccountIn(BaseModel):
    balance: PositiveFloat
