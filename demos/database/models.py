from sqlalchemy.sql import func

from demos.database.app import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    # optional
    def __repr__(self):
        return f'Note <id={self.id}, body={self.body}, created_at={self.created_at}>'


