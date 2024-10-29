from pydantic import AwareDatetime, BaseModel, NaiveDatetime


class UserOut(BaseModel):
    username: str
    email: str
    created_at: AwareDatetime | NaiveDatetime | None
