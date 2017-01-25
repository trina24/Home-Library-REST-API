from db import db
import datetime


class LoanModel(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship('BookModel')

    reader_id = db.Column(db.Integer, db.ForeignKey('readers.id'))
    reader = db.relationship('ReaderModel')

    def __init__(self, book_id, date_start, reader_id, **kwargs):
        self.book_id = book_id
        self.date_start = date_start
        self.date_end = kwargs.get('date_end')
        self.reader_id = reader_id

    def json(self):
        if self.date_end:
            date_end = datetime.date.isoformat(self.date_end)
        else:
            date_end = ''
        return {'id': self.id, 'date_start': datetime.date.isoformat(self.date_start), 'date_end': date_end,
                'book_id': self.book_id, 'reader_id': self.reader_id}

    @classmethod
    def find_by_id(cls, id, book_id):
        return cls.query.filter_by(id=id, book_id=book_id).first()

    @classmethod
    def loan_forbidden(cls, book_id, date_start):
        for loan in cls.query.filter_by(book_id=book_id).all():
            if loan.date_end is None or (loan.date_start < date_start < loan.date_end):
                return True

        return False

    @staticmethod
    def dates_invalid(loan=None, **kwargs):
        for key, value in kwargs.items():
            if value and value > datetime.date.today():
                return {'message': 'Invalid dates (start and end must be at latest today).'}
        date_start = kwargs.get('date_start')
        date_end = kwargs.get('date_end')
        if date_start and date_end:
            if date_start >= date_end:
                return {"message": "Start date must be before end date."}
            return None
        elif loan is None:
            return None
        elif (date_start and loan.date_end and date_start >= loan.date_end) or \
                (date_end and loan.date_start >= date_end):
            return {"message": "Start date must be before end date."}
        else:
            return None

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
