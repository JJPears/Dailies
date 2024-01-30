from flask import request, jsonify
from app import app
from models import User
from database import db

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_json()), 200

@app.route('/user', methods=['POST'])
def create_user():
    user_data = request.get_json()
    pass

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    if not user_data:
        return jsonify({'error': 'No data provided'}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    user.update(user_data)

    db.session.commit()

    return jsonify(user.to_json()), 201