import datetime

import pytest
from jinja2.utils import generate_lorem_ipsum
from loguru import logger
from sqlalchemy import and_
from sqlalchemy.schema import Table, CreateTable

from demos.database.app import create_app, db as sql_db
from demos.database.models import Note

NUM = 1000


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app


@pytest.fixture(scope='session')
def db(app):
    with app.app_context():  # 需要在app上下文下中, sql_db才生效, 而且这样Note.query才会生效
        yield sql_db


@pytest.fixture(autouse=True)  # 每个用例跑之前都先要建表, 插入一些数据
def prepare_data(db):
    db.drop_all()
    db.create_all()
    now = datetime.datetime.now()
    for i in range(NUM, 0, -1):
        note = Note(body=generate_lorem_ipsum(1, False, 3, 4), created_at=now - datetime.timedelta(seconds=i))
        db.session.add(note)
    db.session.commit()
    assert Note.query.count() == NUM
    logger.info('prepare data success')


def test_show_create_table():
    assert isinstance(Note.__table__, Table)
    logger.info(CreateTable(Note.__table__))


def test_add(db):
    create_at = datetime.datetime(1991, 12, 10, 11, 30, 12)
    note1 = Note(body='remember yangkai', created_at=create_at)
    note2 = Note(body='remember huoxinping')
    db.session.add(note1)
    db.session.add(note2)
    assert note1.id is None
    assert note1.created_at == create_at
    assert note1.body == 'remember yangkai'
    assert note2.created_at is None
    db.session.commit()
    assert isinstance(note1.id, int)
    assert note1.id == NUM + 1
    assert note2.id - note1.id == 1
    assert note1.created_at == create_at
    assert Note.query.count() == NUM + 2


def test_add_same(db):
    create_at = datetime.datetime(1991, 12, 10, 11, 30, 12)
    logger.info(Note.query.get(1).body)
    note = Note(body='remember wuyi', created_at=create_at)
    db.session.add(note)
    assert note.id is None
    assert Note.query.count() == NUM + 1
    assert note.id is not None  # 查过一次id就会有值(上一行的count), 这是sqlalchemy的特性
    Note.query.get(NUM + 1).body == 'remember wuyi'
    Note.query.get(NUM + 1).id is None
    db.session.commit()
    assert Note.query.count() == NUM + 1
    assert note.id == NUM + 1
    assert Note.query.get(note.id).body == 'remember wuyi'
    logger.info(note)


def test_query(db):
    note1 = Note.query.first()
    logger.info(note1)

    notes = Note.query.all()
    assert notes[0] is note1
    assert isinstance(notes, list)
    assert len(notes) == NUM

    note2 = Note(body='remember yangkai', created_at=datetime.datetime.now())
    db.session.add(note2)
    db.session.commit()
    note_yang = Note.query.filter_by(body='remember yangkai').one()
    assert note_yang is note2


def test_update(db):
    note = Note(body='remember yangkai', created_at=datetime.datetime.now())
    db.session.add(note)

    note.body = 'remember wuyi'
    # db.session.add(note)  # 该行可以省略, 对note属性的变更也会影响到session中的存储的note(它们本就是同一个对象)
    query_note_before_commit = Note.query.filter(Note.body.like('%emember wuy%')).one()

    db.session.commit()

    query_note = Note.query.filter(Note.body.like('%emember wuy%')).one()
    assert query_note is note and query_note_before_commit is note


def test_delete(db):
    assert Note.query.filter(and_(Note.id < 100, Note.id >= 50)).count() == 50

    note1 = Note.query.get(50)
    assert note1.id == 50
    db.session.delete(note1)
    db.session.commit()

    assert Note.query.filter(and_(Note.id < 100, Note.id >= 50)).count() == 49
