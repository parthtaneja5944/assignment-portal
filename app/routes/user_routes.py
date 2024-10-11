from flask import Blueprint, request, jsonify
from app import users_collection, assignments_collection, bcrypt
from app.utils import hash_password, check_password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register_user():
    """
    This function lets new users sign up. 
    They send their username and password, and if the username isn’t taken, 
    we hash the password and save their info in the database.
    If everything goes well, we return a success message.
    If the username is already in use, we let them know.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')

        if users_collection.find_one({'username': username}):
            return jsonify({'message': 'User already exists'}), 400

        hashed_password = hash_password(password)
        users_collection.insert_one({'username': username, 'password': hashed_password, 'role': role})
        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'Error registering user: {str(e)}'}), 500



@user_bp.route('/login', methods=['POST'])
def login_user():
    """
    This function is for users to log in.
    They provide their username and password, and if they match what's in the database,
    we create a JWT token that lasts for 1 hour. 
    If the login fails, we send back an error message.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = users_collection.find_one({'username': username})
        if user and check_password(user['password'], password):
            token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
            return jsonify({'token': token}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'message': f'Error logging in: {str(e)}'}), 500



@user_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_assignment():
    """
    This function lets logged-in users upload assignments. 
    They send the assignment details, and we store it in the database with a 'pending' status.
    If anything goes wrong, we send back an error message.
    """
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        assignment = {
            'userId': current_user,
            'task': data['task'],
            'admin': data['admin'],
            'status': 'pending'
        }
        assignments_collection.insert_one(assignment)
        return jsonify({'message': 'Assignment uploaded successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'Error uploading assignment: {str(e)}'}), 500



@user_bp.route('/admins', methods=['GET'])
def get_admins():
    """
    This function returns a list of all admins in the system.
    We fetch their usernames and return them as a JSON list.
    If there's an error during fetching, we let the caller know.
    """
    try:
        admins = users_collection.find({'role': 'admin'}, {'username': 1, '_id': 0})
        return jsonify(list(admins)), 200

    except Exception as e:
        return jsonify({'message': f'Error fetching admins: {str(e)}'}), 500
