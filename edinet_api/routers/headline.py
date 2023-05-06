from fastapi import APIRouter
# from schemas import headline as headline_schema
from crud import headline as headline_crud

router = APIRouter()


@router.get("/headlines")
async def list_tasks():
    pass


@router.get("/headlines/{action}")
async def headline_action(action: str, date: int):
    if action == "fetch":
        await headline_crud.update_headline(date=date)
    return None
