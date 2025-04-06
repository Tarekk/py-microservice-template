from fastapi import APIRouter

from api.deps import CurrentUser

router = APIRouter()


@router.get("")
async def health_check():
    return {"Hello": "World"}


@router.get("/auth")
async def health_check_auth(api_key: CurrentUser):
    return {"Hello": "World"}
