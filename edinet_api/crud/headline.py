from services.execute import edinet_master
from edinet_logging import EdinetLogger
logger = EdinetLogger.get_loggger()


async def update_headline(date,doc_type) -> None:
    return edinet_master.update_headline(date=date,doc_type=doc_type)

async def get_headline(date=None) -> None:
    result = edinet_master.get_headlines(date=date)
    return result
