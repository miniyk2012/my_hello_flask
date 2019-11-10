import pytest
from loguru import logger
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///testalchemy.db', echo=False)  # 相对路径
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


student_teacher_table = Table('student_teacher', Base.metadata,
                              Column('student_id', ForeignKey('student.id'), primary_key=True),
                              Column('teacher_id', ForeignKey('teacher.id'), primary_key=True)
                              )


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), index=True)
    teachers = relationship('Teacher',
                            secondary=student_teacher_table,
                            back_populates='students')


class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    name = Column(String(70), index=True)
    students = relationship('Student',
                            secondary=student_teacher_table,
                            back_populates='teachers')


print('重建表')
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


def test_many2many():
    t1 = Teacher(name='Bruce')
    t2 = Teacher(name='Sean')
    t3 = Teacher(name='Grey')
    t4 = Teacher(name='Jenny')
    s1 = Student(name='Mike')
    s2 = Student(name='David')
    s3 = Student(name='Kitty')
    s4 = Student(name='Peter')

    session: Session = Session()
    session.add_all([t1, t2, t3, t4, s1, s2, s3, s4])
    session.commit()

    s1.teachers = [t3, t4]
    s2.teachers = [t2]
    s3.teachers = [t4]

    assert len(t1.students) == 0
    assert len(t2.students) == 1
    assert len(t3.students) == 1
    assert len(t4.students) == 2

    print(session.query(student_teacher_table).all())
    assert len(session.query(student_teacher_table).all()) == 4
    assert len(session.query(student_teacher_table).filter(student_teacher_table.c.teacher_id == 4).all()) == 2

    s1.teachers.remove(t4)

    assert len(s1.teachers) == 1
    assert len(t4.students) == 1

    assert len(session.query(student_teacher_table).all()) == 3
    assert len(session.query(student_teacher_table).filter(student_teacher_table.c.teacher_id == 4).all()) == 1

    session.rollback()
    assert len(session.query(student_teacher_table).all()) == 0
    assert len(t1.students) == 0
    assert len(t2.students) == 0
    assert len(t3.students) == 0
    assert len(t4.students) == 0
    assert len(s1.teachers) == 0
    assert len(s2.teachers) == 0
    assert len(s3.teachers) == 0
    assert len(s4.teachers) == 0

