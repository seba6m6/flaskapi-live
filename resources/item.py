from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='price is required')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='item needs to belong to some store')
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"item" : "not found"}


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"item": "item with this name already exists"}
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "an error occurred while inserting an item"}, 500
        return item.json(), 201
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item has been deleted !'}
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()

class Items(Resource):
    def get(self,):
        return [item.json() for item in ItemModel.query.all()]
