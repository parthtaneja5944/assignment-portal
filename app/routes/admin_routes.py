from flask import Blueprint, jsonify, request
from app import assignments_collection
from app.utils import get_user_role
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

admin_bp = Blueprint('admin', __name__)


def convert_objectid_to_string(assignments):
    return [{**assignment, '_id': str(assignment['_id'])} for assignment in assignments]


@admin_bp.route('/assignments', methods=['GET'])
@jwt_required()
def view_assignments():
    """
    This function allows an admin to view all pending assignments assigned to them.
    It first checks if the user has admin rights and then fetches 
    assignments from the database that are still pending.
    If successful, it returns the assignments; otherwise, it returns an error message.
    """
    try:
        current_user = get_jwt_identity()
        role = get_user_role(current_user)
        if role != 'admin':
            return jsonify({'message': 'Access denied'}), 403

        assignments = assignments_collection.find({
            'admin': current_user,
            'status': 'pending'
        })
        assignments = list(assignments)
        assignments = convert_objectid_to_string(assignments)
        return jsonify(assignments), 200

    except Exception as e:
        return jsonify({'message': f'Error fetching assignments: {str(e)}'}), 500



@admin_bp.route('/assignments/<assignment_id>/<action>', methods=['POST'])
@jwt_required()
def handle_assignment(assignment_id, action):
    """
    This function allows an admin to accept or reject an assignment.
    It verifies if the user is an admin, checks if the assignment exists, 
    and then updates its status based on the provided action (accept or reject).
    It returns a success message or an error message as needed.
    """
    try:
        current_user = get_jwt_identity()
        role = get_user_role(current_user)
        if role != 'admin':
            return jsonify({'message': 'Access denied'}), 403

        assignment = assignments_collection.find_one({'_id': ObjectId(assignment_id), 'admin': current_user})
        if not assignment:
            return jsonify({'message': 'Assignment not found'}), 404

        if action == 'accept':
            assignments_collection.update_one({'_id': ObjectId(assignment_id)}, {'$set': {'status': 'accepted'}})
            return jsonify({'message': 'Assignment accepted'}), 200
        elif action == 'reject':
            assignments_collection.update_one({'_id': ObjectId(assignment_id)}, {'$set': {'status': 'rejected'}})
            return jsonify({'message': 'Assignment rejected'}), 200
        return jsonify({'message': 'Invalid action'}), 400

    except Exception as e:
        return jsonify({'message': f'Error handling assignment: {str(e)}'}), 500
