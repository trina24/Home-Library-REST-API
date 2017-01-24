from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.book import BookModel

class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('author',
                        type=str,
                        required=False)
    parser.add_argument('title',
                        type=str,
                        required=False)

    def get(self, id):
        book = BookModel.find_by_id(id)
        if book:
            return book.json()
        return {'message': 'Book not found.'}, 404

    def delete(self, id):
        book = BookModel.find_by_id(id)
        if (book):
            book.delete_from_db()
        return {'message' : 'Book deleted successfully.'}

    def put(self, id):
        book = BookModel.find_by_id(id)

        if book:
            data = Book.parser.parse_args()
            if data.get('author'):
                book.author = data['author']
            if data.get('title'):
                book.title = data['title']
            try:
                book.save_to_db()
            except:
                return {'message': 'An error occurred updating the book.'}, 500
            return book.json()
        return {'message': 'Book doesn\'t exist.'}, 400


class BookList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('author',
                        type=str,
                        required=True,
                        help='Every book must have an author.')
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help='Every book must have a title.')
    def get(self):
        return {'books': [book.json() for book in BookModel.query.all()]}

    def post(self):
        data = Book.parser.parse_args()
        if BookModel.find_by_info(**data):
            return {"message": "A book with title '{}' written by {} already exists.".format(data['title'], data['author'])}, 400

        book = BookModel(**data)

        try:
            book.save_to_db()
        except:
            return {'message': 'An error occurred inserting the book.'}, 500
        return book.json(), 201