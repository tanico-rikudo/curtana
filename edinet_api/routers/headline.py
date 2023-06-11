import datetime
from enum import Enum

from fastapi import APIRouter,Query
# from schemas import headline as headline_schema
from crud import headline as headline_crud

router = APIRouter()
today = datetime.datetime.now().strftime("%Y%m%d")

class ActionName(str, Enum):
    fetch = "fetch"

class HeadlineDocType(str, Enum):
    buyback = "buyback"
    amend_buyback = "amend_buyback"


@router.get("/headlines")
async def get_headlines():
    data = await headline_crud.get_headline()
    return data


@router.get("/headlines/{action}")
async def headline_action(
        action: ActionName,
        doc_type: HeadlineDocType,
        date: str = Query(
            default=today, min_length=8, max_length=8, regex="[0-9]{8}"
        ),

    ):
    if action == ActionName.fetch:
        await headline_crud.update_headline(date=date,doc_type=doc_type )
    return None
