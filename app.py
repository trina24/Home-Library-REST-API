from flask import Flask
from flask_restplus import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.book import Book, BookList
from resources.reader import Reader, ReaderList
from resources.loan import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lvxewobqvpmoud:f31c7378a38a83305e9486a9f2d877bca298f0a5ca556724ff053861992016c6@ec2-54-247-120-169.eu-west-1.compute.amazonaws.com:5432/d875dtqr9j9ru'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'oceanAvenue04'
api = Api(app)

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
