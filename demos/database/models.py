from sqlalchemy.sql import func

from demos.database.app import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # optional
    def __repr__(self):
        return f'Note <id={self.id}, body={self.body}, created_at={self.created_at}>'


# one to many
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    phone = db.Column(db.String(32), unique=True)
    articles = db.relationship('Article')

    # optional
    def __repr__(self):
        return f'Author <id={self.id}, name={self.name}, phone={self.phone}>'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    # optional
    def __repr__(self):
        return f'Article <id={self.id}, title={self.title}, body={self.body}, author_id={self.author_id}>'


# one to many + bidirectional relationship
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    writer = db.relationship('Writer', back_populates='books')

    # optional
    def __repr__(self):
        return f'Book <id={self.id}, title={self.title}>'


class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    books = db.relationship('Book', back_populates='writer')

    # optional
    def __repr__(self):
        return f'Writer <id={self.id}, name={self.name}>'


# many to one
class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship('City')  # scalar

    # optional
    def __repr__(self):
        return f'Citizen <id={self.id}, name={self.name}>'


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    # optional
    def __repr__(self):
        return f'City <id={self.id}, name={self.name}>'
