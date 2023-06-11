from fastapi import APIRouter
# from schemas import headline as headline_schema
from crud import headline as headline_crud

router = APIRouter()


@router.get("/details")
async def get_details():
    data = await headline_crud.get_headline()
    return data