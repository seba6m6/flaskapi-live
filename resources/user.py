from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type = str,
                        required=True,
                        help= "need a valid username")
    parser.add_argument("password",
                        type = str,
                        required=True,
                        help= "need a valid password")


    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"message": "Unfortunately this name is already taken"}, 400
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created"}, 201