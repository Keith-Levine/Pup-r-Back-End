import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict


# Creating an instance of the Blueprint class (Flask version of a controller)
# param 1: Name of the Blueprint
# param 2: The name for importing this Blueprint into another file
user = Blueprint('users', 'user')


"""
curl -X POST \
    -H 'Content-Type: application/json' \
    -d '{"username": "Sidney2", "email": "sidneydog+2@gmail.com", "password": "donotsteal"}' \
    'http://localhost:5000/api/v1/users/register'
"""
@user.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    print(payload)

    payload['email'] = payload['email'].lower()

    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={'code': '401', 'message': 'Email already exists'})

    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])

        user = models.User.create(**payload)
        user_dict = model_to_dict(user)
        print(user_dict)

        del user_dict['password']

        return jsonify(data=user_dict, status={'code': 201, 'message': 'user created'})


"""
curl -X POST \
    -H 'Content-Type: application/json' \
    -d '{"username": "Sidney2", "email": "sidneydog+2@gmail.com", "password": "donotsteal"}' \
    'http://localhost:5000/api/v1/users/login'
"""
@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()

    print(payload)

    """
    - Try and find the user by email.
        - IF THE EMAIL EXISTS
            - Check the passwords b/w DB and Request
                - IF THEY MATCH
                    - login user
                - ELSE
                    - Send incorrect password message
        - ELSE
            - Send incorrect email message
    """
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)

        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)

            return jsonify(data=user_dict, status={'code': 200, 'message': 'Login successful'})

        else:
            return jsonify(data={}, status={'code': 401, 'message': 'Password incorrect'})
    
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Email does not exist'})

@user.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return jsonify(data={}, status={"code": 200, "message": "successful logout"})