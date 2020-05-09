from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be empty")
    parser.add_argument("store_id", type=int, required=True, help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return {"item": item.json()}, 200
        else:
            return {"item": None}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {"message": f"Item with name {name} already exists"}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500  # internal server error
        return {"item": item.json()}, 201

    @jwt_required()
    def put(self, name):
        item = ItemModel.find_item_by_name(name)
        data = Item.parser.parse_args()
        price = data['price']
        store_id = data['store_id']
        if item:
            item.price = price
        else:
            item = ItemModel(name, price, store_id)
        item.save_to_db()
        return {"item": item.json()}, 200

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}, 200


class Items(Resource):
    @jwt_required()
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}, 200
