from flask_restful import Resource, reqparse
from models.reader import ReaderModel


class Reader(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Every reader must have a name.')

    @staticmethod
    def get(id):
        reader = ReaderModel.find_by_id(id)
        if reader:
            return reader.json()
        return {'message': 'Reader not found.'}, 404

    @staticmethod
    def delete(id):
        reader = ReaderModel.find_by_id(id)
        if reader:
            reader.delete_from_db()
        return {'message': 'Reader deleted successfully.'}

    @staticmethod
    def put(id):
        reader = ReaderModel.find_by_id(id)

        if reader:
            data = Reader.parser.parse_args()
            reader.name = data['name']
            try:
                reader.save_to_db()
            except:
                return {'message': 'An error occurred updating the reader.'}, 500
            return reader.json()
        return {'message': 'Reader doesn\'t exist.'}, 400


class ReaderList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Every reader must have an author.')

    @staticmethod
    def get():
        return {'readers': [book.json() for book in ReaderModel.query.all()]}

    @staticmethod
    def post():
        data = Reader.parser.parse_args()
        if ReaderModel.find_by_name(**data):
            return {"message": "A reader with name '{}' already exists.".format(data['name'])}, 400

        reader = ReaderModel(**data)

        try:
            reader.save_to_db()
        except:
            return {'message': 'An error occurred inserting the reader.'}, 500
        return reader.json(), 201
