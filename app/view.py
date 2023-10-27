from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from app import db
from app.models import User
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, request, jsonify, g
from sqlalchemy.exc import IntegrityError
from middlewares import token_required
from datetime import datetime, timedelta
from functools import wraps

app = Blueprint('view', __name__)

#getAllUserData
@app.route('/', methods=['GET'])
@token_required
def index():
    try:
        users = User.query.all()
        if users:
            user_data = []
            for user in users:
                user_info = {
                    'userName': user.userName,
                    'password': user.password,
                    'birthday': user.birthday,
                    'create_time': user.create_time,
                    'last_login': user.last_login
                }
                user_data.append(user_info)

            return jsonify({'users': user_data})
        else:
            response = {'error': 'No users found'}
            return jsonify(response)
    except SQLAlchemyError as e:
        response = {'error': 'Database error: ' + str(e)}
        return jsonify(response)
    except:
        pass


# register
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        username = data.get('userName')
        password = data.get('password')
        birthday = data.get('birthday')

        existing_user = User.query.filter_by(userName=username).first()
        if existing_user:
            response = {'error': 'User with this username already exists!'}
            return jsonify(response)

        new_user = User(userName=username, password=password, birthday=birthday)
        db.session.add(new_user)
        db.session.commit()
        response = {'message': 'User added successfully!'}

        return jsonify(response), 201
    except IntegrityError as e:
        db.session.rollback()
        response = {'error': 'Database integrity error: ' + str(e)}
        return jsonify(response)
    except SQLAlchemyError as e:
        db.session.rollback()
        response = {'error': 'Database error: ' + str(e)}
        return jsonify(response)

# update profile
@app.route('/update', methods=['PUT'])
@token_required
def update_user():
    try:
        data = request.get_json()
        user_to_update = g.current_user
        new_username = data.get('newUsername')
        new_password = data.get('newPassword')
        new_birthday = data.get('newBirthday')

        if not user_to_update:
            response = {'error': 'User not found!'}
            return jsonify(response), 404
        
        user_to_update.userName = new_username
        user_to_update.password = new_password
        user_to_update.birthday = new_birthday
        db.session.commit()

        return 'User updated successfully!'
    except IntegrityError as e:
        db.session.rollback()
        response = {'error': 'Database integrity error: ' + str(e)}
        return jsonify(response), 500
    except SQLAlchemyError as e:
        db.session.rollback()
        response = {'error': 'Database error: ' + str(e)}
        return jsonify(response), 500


# login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('userName')
    password = data.get('password')

    user = User.query.filter_by(userName=username, password=password).first()

    if user:
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        token = create_access_token(identity=user.userName, expires_delta=timedelta(hours=1))
        
        return jsonify({'token': token, 'type': 'Bearer', 'status': 'success', 'exp': expiration_time})
    else:
        return jsonify({'error': 'Invalid credentials', 'status': 'failure'}), 401

#logout
@app.route('/logout', methods=['POST'])
@token_required
@jwt_required()
def logout():
    try:
        user_id = get_jwt_identity()

        return jsonify({'message': 'User logged out successfully'})
    except Exception as e:
        print(f"Error during logout: {str(e)}")
        return jsonify({'error': 'An error occurred during logout'})