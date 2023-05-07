from services.execute.edinet_master import *


async def fetch_headline(date) -> None:
    update_headline(date=date)
