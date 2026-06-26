from flask import Blueprint, request, jsonify
from models.exhibition_model import *
from utils.auth import token_required, role_required

exhibition_bp = Blueprint('exhibition', __name__)


@exhibition_bp.route('/api/exhibitions', methods=['GET'])
def list_exhibitions():
    exhibitions = get_all_exhibitions()
    return jsonify(exhibitions)


@exhibition_bp.route('/api/exhibitions/<int:exhibition_id>', methods=['GET'])
def get_exhibition(exhibition_id):
    exhibition = get_exhibition_by_id(exhibition_id)
    if not exhibition:
        return jsonify({'error': 'Exhibition not found'}), 404
    artisans = get_exhibition_artisans(exhibition_id)
    exhibition['artisans'] = artisans
    return jsonify(exhibition)


@exhibition_bp.route('/api/exhibitions', methods=['POST'])
@role_required('admin')
def add_exhibition():
    data = request.get_json()
    required = ['exhibition_name', 'location', 'start_date', 'end_date']
    if not all(data.get(f) for f in required):
        return jsonify({'error': 'All fields are required'}), 400
    exhibition_id = create_exhibition(data)
    return jsonify({'message': 'Exhibition created', 'id': exhibition_id}), 201


@exhibition_bp.route('/api/exhibitions/<int:exhibition_id>', methods=['PUT'])
@role_required('admin')
def edit_exhibition(exhibition_id):
    data = request.get_json()
    update_exhibition(exhibition_id, data)
    return jsonify({'message': 'Exhibition updated'})


@exhibition_bp.route('/api/exhibitions/<int:exhibition_id>', methods=['DELETE'])
@role_required('admin')
def remove_exhibition(exhibition_id):
    delete_exhibition(exhibition_id)
    return jsonify({'message': 'Exhibition deleted'})


@exhibition_bp.route('/api/exhibitions/<int:exhibition_id>/assign', methods=['POST'])
@role_required('admin')
def assign_artisan(exhibition_id):
    data = request.get_json()
    assign_artisan_to_exhibition(data['artisan_id'], exhibition_id)
    return jsonify({'message': 'Artisan assigned to exhibition'})


@exhibition_bp.route('/api/exhibitions/<int:exhibition_id>/remove-artisan', methods=['POST'])
@role_required('admin')
def unassign_artisan(exhibition_id):
    data = request.get_json()
    remove_artisan_from_exhibition(data['artisan_id'], exhibition_id)
    return jsonify({'message': 'Artisan removed from exhibition'})
