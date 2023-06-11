from services.execute import edinet_master
from edinet_logging import EdinetLogger
logger = EdinetLogger.get_loggger()

async def get_detail(date=None) -> None:
    result = edinet_master.get_detail(date=date)
    return result
