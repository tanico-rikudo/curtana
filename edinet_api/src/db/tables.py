from sqlalchemy import Column, Integer, String, DateTime, Boolean, Double, DATE
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BuyBackHeadline(Base):
    id = Column(Integer, primary_key=True)
    edinet_code = Column(String(length=16))
    doc_id = Column(String(length=16))
    filename = Column(String(length=256))
    doc_type_code = Column(String(length=256))
    submit_datetime = Column(DateTime)
    xbrl_flag = Column(Boolean)
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    __tablename__ = 'buyback_headline'

    def __dict__(self):
        return {
            "id": self.id,
            "edinet_code": self.edinet_code,
            "doc_id": self.doc_id,
            "filename": self.filename,
            "doc_type_code": self.doc_type_code,
            "submit_datetime": self.submit_datetime,
            "xbrl_flag": self.xbrl_flag,
            "insert_date": self.insert_date,
            "update_date": self.update_date
        }

    def migrate(self,id, edinet_code,doc_id,filename,doc_type_code,submit_datetime,xbrl_flag,insert_date,update_date):
        self.id =id
        self.edinet_code=edinet_code
        self.doc_id=doc_id
        self.filename=filename
        self.doc_type_code=doc_type_code
        self.submit_datetime=submit_datetime
        self.xbrl_flag=xbrl_flag
        self.insert_date=insert_date
        self.update_date=update_date


class BuyBackDetail(Base):
    id = Column(Integer, primary_key=True)
    doc_id = Column(String(length=16))
    filename = Column(String(length=256))
    buy_date = Column(DATE)
    buy_qty = Column(Double)
    buy_notional = Column(Boolean)
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    __tablename__ = 'buyback_detail'

    def __dict__(self):
        return {
            "id": self.id,
            "doc_id": self.doc_id,
            "filename": self.filename,
            "buy_date": self.buy_date,
            "buy_qty": self.buy_qty,
            "buy_notional": self.buy_notional,
            "insert_date": self.insert_date,
            "update_date": self.update_date
        }
