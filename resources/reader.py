from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.reader import ReaderModel

class Reader(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Every reader must have a name.')

    def get(self, id):
        reader = ReaderModel.find_by_id(id)
        if reader:
            return reader.json()
        return {'message': 'Reader not found.'}, 404

    def delete(self, id):
        reader = ReaderModel.find_by_id(id)
        if (reader):
            reader.delete_from_db()
        return {'message' : 'Reader deleted successfully.'}

    def put(self, id):
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
    def get(self):
        return {'readers': [book.json() for book in ReaderModel.query.all()]}

    def post(self):
        data = Reader.parser.parse_args()
        if ReaderModel.find_by_name(**data):
            return {"message": "A reader with name '{}' already exists.".format(data['name'])}, 400

        reader = ReaderModel(**data)

        try:
            reader.save_to_db()
        except:
            return {'message': 'An error occurred inserting the reader.'}, 500
        return reader.json(), 201