from app import users_collection
from flask_bcrypt import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password).decode('utf-8')

def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

def get_user_role(username):
    user = users_collection.find_one({'username': username})
    return user['role'] if user else None
