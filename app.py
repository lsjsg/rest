import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from utils import authenticate, identity
from resources.UserRegister import UserRegister
from resources.Item import Item, Items
from resources.store import Store, Stores
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "test"
api = Api(app)
jwt = JWT(app, authenticate, identity)
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Stores, "/stores")
api.add_resource(UserRegister, "/register")
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
