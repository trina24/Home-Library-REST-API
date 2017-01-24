from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.book import Book, BookList
from resources.reader import Reader, ReaderList
from resources.loan import Loan, LoanList, ReaderLoanList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'oceanAvenue04'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, '/register')
api.add_resource(Book, '/books/<int:id>')
api.add_resource(BookList, '/books')
api.add_resource(Reader, '/readers/<int:id>')
api.add_resource(ReaderList, '/readers')
api.add_resource(Loan, '/books/<int:book_id>/loans/<int:id>')
api.add_resource(LoanList, '/books/<int:book_id>/loans')
api.add_resource(ReaderLoanList, '/readers/<int:id>/loans')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)