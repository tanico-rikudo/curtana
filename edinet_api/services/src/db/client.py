import os
import sys
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from .tables import BuyBackHeadline, BuyBackDetail
from edinet_logging import EdinetLogger
logger = EdinetLogger.get_loggger()

class DBclient:
    def __init__(self):
        self.DATABASE = 'postgresql'
        self.USER = 'user'
        self.PASSWORD = 'pass'
        self.HOST = 'postgresql'
        self.PORT = '5432'
        self.DB_NAME = 'docker'
        self.CONNECT_STR = f'{self.DATABASE}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB_NAME}'

    def init_session(self):
        engine = sqlalchemy.create_engine(self.CONNECT_STR, echo=False)
        session_factory = sessionmaker(bind=engine,
                                       autocommit=False,
                                       autoflush=True)
        session = scoped_session(session_factory)
        return session

    def end_session(self, session):
        session.remove()

    def get_headline_data(self):
        session = self.init_session()
        ret = []

        try:
            query_results = session.query(BuyBackHeadline).order_by(BuyBackHeadline.id).all()
            ret = [ target.get_dict() for  target in query_results]
            logger.info("[DONE] Executed headline data")
        except Exception as e:
            logger.warning(f"[Failure] Cannot execute sql:{e}",exc_info=True)
        finally:
            self.end_session(session)
        return ret

    def insert_data(self, buyback_objects):
        session = self.init_session()
        try:
            session.bulk_save_objects(buyback_objects)
            session.commit()
            logger.info(f"[DONE] Inserted bulk data. Cnt={len(buyback_objects)}")
        except Exception as e:
            logger.warning(f"[Failure] Cannot execute sql:{e}",exc_info=True)
        finally:
            self.end_session(session)

    def get_detail_data(self):
        session = self.init_session()
        ret = []
        try:
            query_result = session.query(BuyBackDetail).order_by(BuyBackDetail.id).all()
            ret = [ target.get_dict() for  target in query_result]
            logger.info("[DONE Executed detail data")
        except Exception as e:
            logger.warning(f"[Failure] Cannot execute sql:{e}", exc_info=True)
        finally:
            self.end_session(session)
        return ret


