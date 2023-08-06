import os
from datetime import datetime as dt

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime

from raspi_logger.util import config

Base = declarative_base()


class RawData(Base):
    __tablename__ = 'raw_data'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    created=Column(DateTime, default=dt.now)
    raw_dump = Column(String, nullable=False)
    uploaded = Column(Boolean, default=False)


def connect(path):
    engine = create_engine(path)
    SessionCls = sessionmaker(bind=engine)

    return SessionCls()


def append_data(data, conf=None, path=None):
    # get config
    if conf is None:
        conf = config()

    # create the correct connection path
    p = os.path.join(conf.get('loggerPath'), 'rawDataLogger.db')
    if path is None:
        path = 'sqlite:///%s' % p
    
    # if the db file does not exist, a call of create_all is needed
    if not os.path.exists(p):
        session = connect(path)
        Base.metadata.create_all(session.bind)
    else:
        # file was initialized before
        session = connect(path)

    # append the data
    if not isinstance(data, list):
        data = [data]
    
    try:
        session.add_all([RawData(raw_dump=record) for record in data])
        session.commit()
    except Exception as e:
        session.rollback()
        
        # TODO, some kind of logs would be necessary here
        print(str(e))
    
    return data
    



