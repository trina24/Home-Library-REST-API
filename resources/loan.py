from flask_restplus import Resource, reqparse
from flask_jwt import jwt_required
from models.loan import LoanModel
from models.reader import ReaderModel
from models.book import BookModel
from api import api
import datetime


class Loan(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date_start',
                        type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
                        required=False,
                        help='Loan must have start date with format YYYY-MM-DD.')
    parser.add_argument('date_end',
                        type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
                        required=False,
                        help='Date must have format YYYY-MM-DD.')
    parser.add_argument('reader_id',
                        type=int,
                        required=False)

    @staticmethod
    @api.doc(responses={
        200: 'Success',
        404: 'Loan not found'
    })
    def get(book_id, id):
        loan = LoanModel.find_by_id(id, book_id)
        if loan:
            return loan.json()
        return {"message": "Loan doesn't exist."}, 404

    @jwt_required()
    @api.doc(responses={
        200: 'Success',
        400: 'Invalid ID or loan date'
    })
    def put(self, book_id, id):
        loan = LoanModel.find_by_id(id, book_id)
        if loan is None:
            return {"message": "Loan doesn't exist."}, 400
        data = Loan.parser.parse_args()
        if data.get('reader_id'):
            if ReaderModel.find_by_id(data['reader_id']):
                loan.reader_id = data['reader_id']
            else:
                return {"message": "Reader doesn't exist."}, 400
        message = LoanModel.dates_invalid(loan, date_start=data.get('date_start'), date_end=data.get('date_end'))
        if message:
            return message, 400
        if data.get('date_start'):
            loan.date_start = data['date_start']
        if data.get('date_end'):
            loan.date_end = data['date_end']
        try:
            loan.save_to_db()
        except:
            return {'message': 'An error occurred updating the loan.'}, 500
        return loan.json()

    @jwt_required()
    def delete(self, book_id, id):
        loan = LoanModel.find_by_id(id, book_id)
        if loan:
            loan.delete_from_db()
        return {'message': 'Loan deleted successfully.'}


class LoanList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date_start',
                        type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
                        required=True,
                        help='Loan must have start date with format YYYY-MM-DD.')
    parser.add_argument('date_end',
                        type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
                        required=False,
                        help='Date must have format YYYY-MM-DD.')
    parser.add_argument('reader_id',
                        type=int,
                        required=True,
                        help='Loan must have a reader.')

    @staticmethod
    @api.doc(responses={
        200: 'Success',
        404: 'Book doesn\'t exist'
    })
    def get(book_id):
        if BookModel.find_by_id(book_id) is None:
            return {"message": "Book doesn't exist."}, 404
        return {'loans': [loan.json() for loan in LoanModel.query.filter_by(book_id=book_id).all()]}

    @jwt_required()
    @api.doc(responses={
        201: 'Loan created',
        400: 'Invalid ID or loan date'
    })
    def post(self, book_id):
        data = LoanList.parser.parse_args()
        if ReaderModel.find_by_id(data['reader_id']) is None:
            return {"message": "Reader doesn't exist."}, 400
        elif LoanModel.loan_forbidden(book_id, data['date_start']):
            return {"message": "Book is already lent."}, 400
        else:
            message = LoanModel.dates_invalid(date_start=data.get('date_start'), date_end=data.get('date_end'))
        if message:
            return message, 400
        loan = LoanModel(book_id, **data)
        loan.save_to_db()
        return loan.json(), 201


class ReaderLoanList(Resource):
    @staticmethod
    @api.doc(responses={
        200: 'Success',
        404: 'Reader doesn\' exist'
    })
    def get(id):
        if ReaderModel.find_by_id(id) is None:
            return {"message": "Reader doesn't exist."}, 404
        return {'loans': [loan.json() for loan in LoanModel.query.filter_by(reader_id=id).all()]}
