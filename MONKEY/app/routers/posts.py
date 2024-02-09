from fastapi import APIRouter

router = APIRouter()


@router.get("/posts/", tags=["posts"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/posts/me", tags=["posts"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/posts/{username}", tags=["posts"])
async def read_user(username: str):
    return {"username": username}
