from fastapi import APIRouter

from src.schemas.user import UserIn
from src.views.user import UserOut
from src.services.user import UserService

router = APIRouter(prefix="/users")

service = UserService()


@router.post("/", response_model=UserOut)
async def createUser(userData: UserIn):
    return await service.create(userData)
