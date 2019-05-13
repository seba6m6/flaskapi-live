from flask import (
    Flask
)
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, Items
from resources.store import Store, StoreList


app = Flask(__name__)
app.secret_key = 'sebas'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token has expired'
    }), 401




api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5999,debug=True)


