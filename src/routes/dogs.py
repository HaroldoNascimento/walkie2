from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db

dogs_bp = Blueprint(\'dogs_bp\', __name__)

# Simulação de um modelo Dog e suas operações
class Dog:
    def __init__(self, id, name, breed, age, owner_id):
        self.id = id
        self.name = name
        self.breed = breed
        self.age = age
        self.owner_id = owner_id

    def to_dict(self):
        return {
            \'id\': self.id,
            \'name\': self.name,
            \'breed\': self.breed,
            \'age\': self.age,
            \'owner_id\': self.owner_id
        }

dummy_dogs = []
dog_id_counter = 1

@dogs_bp.route(\'/dogs\', methods=[\'POST\'])
@jwt_required()
def add_dog():
    global dog_id_counter
    current_user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get(\'name\')
    breed = data.get(\'breed\')
    age = data.get(\'age\')

    if not name or not breed or not age:
        return jsonify({\'message\': \'Name, breed, and age are required\'}), 400

    new_dog = Dog(dog_id_counter, name, breed, age, current_user_id)
    dummy_dogs.append(new_dog)
    dog_id_counter += 1
    return jsonify({\'message\': \'Dog added successfully\', \'dog\': new_dog.to_dict()}), 201

@dogs_bp.route(\'/dogs\', methods=[\'GET\'])
@jwt_required()
def get_dogs():
    current_user_id = get_jwt_identity()
    user_dogs = [dog.to_dict() for dog in dummy_dogs if dog.owner_id == current_user_id]
    return jsonify(user_dogs), 200

@dogs_bp.route(\'/dogs/<int:dog_id>\', methods=[\'GET\'])
@jwt_required()
def get_dog(dog_id):
    current_user_id = get_jwt_identity()
    dog = next((dog for dog in dummy_dogs if dog.id == dog_id and dog.owner_id == current_user_id), None)
    if dog:
        return jsonify(dog.to_dict()), 200
    return jsonify({\'message\': \'Dog not found\'}), 404

@dogs_bp.route(\'/dogs/<int:dog_id>\', methods=[\'PUT\'])
@jwt_required()
def update_dog(dog_id):
    current_user_id = get_jwt_identity()
    dog = next((dog for dog in dummy_dogs if dog.id == dog_id and dog.owner_id == current_user_id), None)
    if not dog:
        return jsonify({\'message\': \'Dog not found\'}), 404

    data = request.get_json()
    dog.name = data.get(\'name\', dog.name)
    dog.breed = data.get(\'breed\', dog.breed)
    dog.age = data.get(\'age\', dog.age)

    return jsonify({\'message\': \'Dog updated successfully\', \'dog\': dog.to_dict()}), 200

@dogs_bp.route(\'/dogs/<int:dog_id>\', methods=[\'DELETE\'])
@jwt_required()
def delete_dog(dog_id):
    global dummy_dogs
    current_user_id = get_jwt_identity()
    initial_len = len(dummy_dogs)
    dummy_dogs = [dog for dog in dummy_dogs if not (dog.id == dog_id and dog.owner_id == current_user_id)]
    if len(dummy_dogs) < initial_len:
        return jsonify({\'message\': \'Dog deleted successfully\'}), 200
    return jsonify({\'message\': \'Dog not found\'}), 404


