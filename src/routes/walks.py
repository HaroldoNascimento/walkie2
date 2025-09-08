from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

walks_bp = Blueprint(\'walks_bp\', __name__)

# Simulação de um modelo Walk e suas operações
class Walk:
    def __init__(self, id, dog_id, owner_id, start_time, end_time, distance, duration, route_data=None):
        self.id = id
        self.dog_id = dog_id
        self.owner_id = owner_id
        self.start_time = start_time
        self.end_time = end_time
        self.distance = distance
        self.duration = duration
        self.route_data = route_data if route_data is not None else []

    def to_dict(self):
        return {
            \'id\': self.id,
            \'dog_id\': self.dog_id,
            \'owner_id\': self.owner_id,
            \'start_time\': self.start_time.isoformat(),
            \'end_time\': self.end_time.isoformat(),
            \'distance\': self.distance,
            \'duration\': self.duration,
            \'route_data\': self.route_data
        }

dummy_walks = []
walk_id_counter = 1

@walks_bp.route(\'/walks\', methods=[\'POST\'])
@jwt_required()
def start_walk():
    global walk_id_counter
    current_user_id = get_jwt_identity()
    data = request.get_json()
    dog_id = data.get(\'dog_id\')
    start_time = datetime.fromisoformat(data.get(\'start_time\'))

    if not dog_id or not start_time:
        return jsonify({\'message\': \'Dog ID and start time are required\'}), 400

    # Simula o início de um passeio, sem dados de rota ainda
    new_walk = Walk(walk_id_counter, dog_id, current_user_id, start_time, start_time, 0, 0)
    dummy_walks.append(new_walk)
    walk_id_counter += 1
    return jsonify({\'message\': \'Walk started successfully\', \'walk\': new_walk.to_dict()}), 201

@walks_bp.route(\'/walks/<int:walk_id>/end\', methods=[\'PUT\'])
@jwt_required()
def end_walk(walk_id):
    current_user_id = get_jwt_identity()
    walk = next((w for w in dummy_walks if w.id == walk_id and w.owner_id == current_user_id), None)
    if not walk:
        return jsonify({\'message\': \'Walk not found\'}), 404

    data = request.get_json()
    end_time = datetime.fromisoformat(data.get(\'end_time\'))
    distance = data.get(\'distance\')
    duration = data.get(\'duration\')
    route_data = data.get(\'route_data\', [])

    walk.end_time = end_time
    walk.distance = distance
    walk.duration = duration
    walk.route_data = route_data

    return jsonify({\'message\': \'Walk ended successfully\', \'walk\': walk.to_dict()}), 200

@walks_bp.route(\'/walks\', methods=[\'GET\'])
@jwt_required()
def get_walks():
    current_user_id = get_jwt_identity()
    user_walks = [walk.to_dict() for walk in dummy_walks if walk.owner_id == current_user_id]
    return jsonify(user_walks), 200

@walks_bp.route(\'/walks/<int:walk_id>\', methods=[\'GET\'])
@jwt_required()
def get_walk(walk_id):
    current_user_id = get_jwt_identity()
    walk = next((w for w in dummy_walks if w.id == walk_id and w.owner_id == current_user_id), None)
    if walk:
        return jsonify(walk.to_dict()), 200
    return jsonify({\'message\': \'Walk not found\'}), 404

@walks_bp.route(\'/walks/stats\', methods=[\'GET\'])
@jwt_required()
def get_walk_stats():
    current_user_id = get_jwt_identity()
    user_walks = [walk for walk in dummy_walks if walk.owner_id == current_user_id]

    total_distance = sum(w.distance for w in user_walks)
    total_duration = sum(w.duration for w in user_walks)
    num_walks = len(user_walks)

    return jsonify({
        \'total_distance\': total_distance,
        \'total_duration\': total_duration,
        \'num_walks\': num_walks
    }), 200


