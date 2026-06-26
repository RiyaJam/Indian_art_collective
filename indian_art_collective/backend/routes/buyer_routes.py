from flask import Blueprint, request, jsonify
from models.buyer_model import *
from utils.auth import token_required, role_required

buyer_bp = Blueprint('buyer', __name__)


@buyer_bp.route('/api/buyers', methods=['GET'])
@role_required('admin')
def list_buyers():
    buyers = get_all_buyers()
    return jsonify(buyers)


@buyer_bp.route('/api/buyers/<int:buyer_id>', methods=['GET'])
@token_required
def get_buyer(buyer_id):
    if request.user['role'] == 'buyer' and request.user['user_id'] != buyer_id:
        return jsonify({'error': 'Access forbidden'}), 403
    buyer = get_buyer_by_id(buyer_id)
    if not buyer:
        return jsonify({'error': 'Buyer not found'}), 404
    return jsonify(buyer)


@buyer_bp.route('/api/buyers/<int:buyer_id>', methods=['PUT'])
@token_required
def edit_buyer(buyer_id):
    if request.user['role'] == 'buyer' and request.user['user_id'] != buyer_id:
        return jsonify({'error': 'Access forbidden'}), 403
    data = request.get_json()
    update_buyer(buyer_id, data)
    return jsonify({'message': 'Profile updated'})


@buyer_bp.route('/api/buyers/<int:buyer_id>', methods=['DELETE'])
@role_required('admin')
def remove_buyer(buyer_id):
    delete_buyer(buyer_id)
    return jsonify({'message': 'Buyer deleted'})
