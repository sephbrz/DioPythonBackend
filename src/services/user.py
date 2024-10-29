from src.database import database
from src.models.user import userTable
from src.schemas.user import UserIn
from src.security import get_password_hash
from src.exceptions import DatabaseError

import sqlite3


class UserService:
    async def create(self, user: UserIn) -> int:
        command = userTable.insert().values(
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password),
        )
        try:
            user_id = await database.execute(command)
        except sqlite3.IntegrityError as err:
            raise DatabaseError("Username or email is not unique")
        query = userTable.select().where(userTable.c.id == user_id)
        return await database.fetch_one(query)
