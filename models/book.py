from db import db


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    title = db.Column(db.String(120))

    def __init__(self, author, title):
        self.author = author
        self.title = title

    def json(self):
        return {'id': self.id, 'author': self.author, 'title': self.title}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_info(cls, author, title):
        return cls.query.filter_by(author=author, title=title).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
