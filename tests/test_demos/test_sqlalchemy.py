import pytest
from loguru import logger
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///testdata.db', echo=True)  # 相对路径
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


@pytest.fixture
def prepare_data():
    session = Session()
    user = User(name='yangkai', fullname='Thomas Young', nickname='kaibi')
    session.add(user)
    session.commit()


def test_query(prepare_data):
    session = Session()
    logger.info(session.query(User).filter_by(name='yangkai').one())


def test_func():
    from sqlalchemy.sql import func
    logger.info(func.now())
    logger.info(func.as_utc())
    logger.info(type(func.now()))
