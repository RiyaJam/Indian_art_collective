from flask import Blueprint, request, jsonify
from models.artisan_model import *
from utils.auth import token_required, role_required

artisan_bp = Blueprint('artisan', __name__)


@artisan_bp.route('/api/artisans', methods=['GET'])
def list_artisans():
    artisans = get_all_artisans()
    return jsonify(artisans)


@artisan_bp.route('/api/artisans/<int:artisan_id>', methods=['GET'])
def get_artisan(artisan_id):
    artisan = get_artisan_by_id(artisan_id)
    if not artisan:
        return jsonify({'error': 'Artisan not found'}), 404
    return jsonify(artisan)


@artisan_bp.route('/api/artisans/<int:artisan_id>/stats', methods=['GET'])
@token_required
def artisan_stats(artisan_id):
    if request.user['role'] == 'artisan' and request.user['user_id'] != artisan_id:
        return jsonify({'error': 'Access forbidden'}), 403
    stats = get_artisan_stats(artisan_id)
    return jsonify(stats)


@artisan_bp.route('/api/artisans/<int:artisan_id>/schemes', methods=['GET'])
@token_required
def artisan_schemes(artisan_id):
    if request.user['role'] == 'artisan' and request.user['user_id'] != artisan_id:
        return jsonify({'error': 'Access forbidden'}), 403
    schemes = get_artisan_schemes(artisan_id)
    return jsonify(schemes)


@artisan_bp.route('/api/artisans/<int:artisan_id>/exhibitions', methods=['GET'])
@token_required
def artisan_exhibitions(artisan_id):
    if request.user['role'] == 'artisan' and request.user['user_id'] != artisan_id:
        return jsonify({'error': 'Access forbidden'}), 403
    exhibitions = get_artisan_exhibitions(artisan_id)
    return jsonify(exhibitions)


@artisan_bp.route('/api/artisans/<int:artisan_id>', methods=['PUT'])
@token_required
def edit_artisan(artisan_id):
    if request.user['role'] == 'artisan' and request.user['user_id'] != artisan_id:
        return jsonify({'error': 'Access forbidden'}), 403
    data = request.get_json()
    update_artisan(artisan_id, data)
    return jsonify({'message': 'Artisan updated successfully'})


@artisan_bp.route('/api/artisans/<int:artisan_id>', methods=['DELETE'])
@role_required('admin')
def remove_artisan(artisan_id):
    delete_artisan(artisan_id)
    return jsonify({'message': 'Artisan deleted successfully'})
