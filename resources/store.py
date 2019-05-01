from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()

    def get(self, name):
        store = Store.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "such store does not exist"}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message" : "store already exists"}, 400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {"message": "problem while saving"}
        return store.json(), 201
    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
        return {"message":"store deleted"}
class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}