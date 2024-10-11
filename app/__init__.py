from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from config import Config

bcrypt = Bcrypt()

client = MongoClient(Config.MONGO_URI)
db = client['assignment_portal']
users_collection = db['users']
assignments_collection = db['assignments']

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt = JWTManager(app)
    bcrypt.init_app(app)

    from app.routes.user_routes import user_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    return app
