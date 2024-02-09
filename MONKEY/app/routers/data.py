from fastapi import APIRouter

router = APIRouter()


@router.get("/datasets/", tags=["datasets"])
async def read_users():
    return ["fakeddit"]
