from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

import models

from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError


# Creating an instance of the Blueprint class (Flask version of a controller)
# param 1: Name of the Blueprint
# param 2: The name for importing this Blueprint into another file
dog = Blueprint('dogs', 'dog')


"""
curl 'http://localhost:5000/api/v1/dogs/'
"""
@dog.route('/', methods=['GET'])
@login_required
def get_all_dogs():
    # if not current_user.email.endswith('edu'):
    #     return jsonify(data={}, status={"code": 403, "message": "Not authorized"})

    try:
        # db_dogs = models.Dog.select()
        # dogs = []
        
        # for dog in db_dogs:
        #     print(dog)
        #     print(model_to_dict(dog))
        #     dogs.append(model_to_dict(dog))

        dogs = [model_to_dict(dog) for dog in current_user.dogs]
        
        print(dogs)
        return jsonify(data=dogs, status={'code': 200, 'message': 'Success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resource'})


"""
Invalid Request:
curl -X POST \
    -H 'Content-Type: application/json' \
    -d '{"test":"test"}' \
    'http://localhost:5000/api/v1/dogs/'
Valid Request:    
curl -X POST \
    -H 'Content-Type: application/json' \
    -d '{"name": "Sidney", "owner": "Phils Mom", "breed": "Lab"}' \
    'http://localhost:5000/api/v1/dogs/'
"""
@dog.route('/', methods=['POST'])
def create_dog():
    payload = request.get_json()
    print(payload)

    try:
        dog = models.Dog.create(name=payload['name'], owner=current_user.id, breed=payload['breed'])

        print(dog.__dict__)

        return jsonify(data=model_to_dict(dog), status={'code': 201, 'message': 'Success'})
    except IntegrityError:
        print('Invalid Schema was sent')

        return jsonify(data={}, status={'code': 401, 'message': 'Invalid dog schema'})

# Show route
@dog.route('/<id>', methods=["GET"])
def get_one_dog(id):
    # getting the dog from the ID parameter
    dog = models.Dog.get_by_id(id)
    # printing the dog that we got and coverting it to a dictionary
    print(dog.__dict__)
    # return JSON object of the dog and a status code of 200 since we are successful
    return jsonify(data=model_to_dict(dog), status={"code": 200, "message": "successful dog"})

# Update route
@dog.route('/<id>', methods=["PUT"])
def update_dog(id):
    # storing the data from the request body
    payload = request.get_json()
    # the first step of updating the found dog with new data
    query = models.Dog.update(**payload).where(models.Dog.id == id)
    # execute the query
    query.execute()
    # return the updated dog and status code of 200 for success!!!
    return jsonify(data=model_to_dict(models.Dog.get_by_id(id)), status={"code": 200, "message": "successfully updated dog"})


# Delete route
@dog.route('/<id>', methods=["DELETE"])
def delete_dog(id):
    # find the dog to delete
    query = models.Dog.delete().where(models.Dog.id == id)
    # actually delete the dog
    query.execute()
    # return a response of success if the dog is deleted
    return jsonify(data="dog successfully deleted", status={"status": 200, "message": "dog successfully deleted"})