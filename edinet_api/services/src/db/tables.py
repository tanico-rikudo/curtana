import datetime
import os

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Double, DATE, func
from sqlalchemy.orm import declarative_base
from edinet_logging import EdinetLogger

logger = EdinetLogger.get_loggger()
Base = declarative_base()


class BuyBackHeadline(Base):
    id = Column(Integer, primary_key=True)
    edinet_code = Column(String(length=16))
    doc_id = Column(String(length=16))
    filer_name = Column(String(length=256))
    doc_type_code = Column(String(length=256))
    submit_datetime = Column(DateTime)
    xbrl_flag = Column(Boolean)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, onupdate=datetime.datetime.now)
    __tablename__ = 'buyback_headline'

    def get_dict(self):
        # Note: __dict__  is not allowed
        return {
            "id": self.id,
            "edinet_code": self.edinet_code,
            "doc_id": self.doc_id,
            "filer_name": self.filer_name,
            "doc_type_code": self.doc_type_code,
            "submit_datetime": self.submit_datetime,
            "xbrl_flag": self.xbrl_flag,
            "created_on": self.created_on,
            "updated_on": self.updated_on
        }


class BuyBackDetail(Base):
    id = Column(Integer, primary_key=True)
    doc_id = Column(String(length=16))
    acquition_type = Column(String(length=256))
    buy_date = Column(DATE)
    buy_qty = Column(Double)
    buy_notional = Column(Double)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, onupdate=datetime.datetime.now)
    __tablename__ = 'buyback_detail'

    def get_dict(self):
        return {
            "id": self.id,
            "doc_id": self.doc_id,
            "buy_date": self.buy_date,
            "buy_qty": self.buy_qty,
            "buy_notional": self.buy_notional,
            "created_on": self.created_on,
            "updated_on": self.updated_on
        }

