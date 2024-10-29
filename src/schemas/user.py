from pydantic import AwareDatetime, BaseModel


class UserIn(BaseModel):
    username: str
    email: str
    password: str
