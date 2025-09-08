from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User, db

auth_bp = Blueprint(\'auth_bp\', __name__)

@auth_bp.route(\'/register\', methods=[\'POST\'])
def register():
    data = request.get_json()
    email = data.get(\'email\')
    password = data.get(\'password\')
    name = data.get(\'name\')

    if not email or not password:
        return jsonify({\'message\': \'Email and password are required\'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({\'message\': \'User already exists\'}), 409

    new_user = User(email=email, name=name)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({\'message\': \'User registered successfully\', \'user\': new_user.to_dict()}), 201

@auth_bp.route(\'/login\', methods=[\'POST\'])
def login():
    data = request.get_json()
    email = data.get(\'email\')
    password = data.get(\'password\')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, user=user.to_dict()), 200
    else:
        return jsonify({\'message\': \'Invalid credentials\'}), 401

@auth_bp.route(\'/protected\', methods=[\'GET\'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.email), 200


