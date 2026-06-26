from flask import Blueprint, request, jsonify
from models.order_model import *
from utils.auth import token_required, role_required

order_bp = Blueprint('order', __name__)


@order_bp.route('/api/orders', methods=['GET'])
@role_required('admin')
def list_orders():
    orders = get_all_orders()
    return jsonify(orders)


@order_bp.route('/api/orders/<int:order_id>', methods=['GET'])
@token_required
def get_order(order_id):
    order = get_order_by_id(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order)


@order_bp.route('/api/orders/buyer/<int:buyer_id>', methods=['GET'])
@token_required
def buyer_orders(buyer_id):
    if request.user['role'] == 'buyer' and request.user['user_id'] != buyer_id:
        return jsonify({'error': 'Access forbidden'}), 403
    from models.buyer_model import get_buyer_orders
    orders = get_buyer_orders(buyer_id)
    return jsonify(orders)


@order_bp.route('/api/orders/artisan/<int:artisan_id>', methods=['GET'])
@token_required
def artisan_orders(artisan_id):
    if request.user['role'] == 'artisan' and request.user['user_id'] != artisan_id:
        return jsonify({'error': 'Access forbidden'}), 403
    orders = get_orders_by_artisan(artisan_id)
    return jsonify(orders)


@order_bp.route('/api/orders', methods=['POST'])
@role_required('buyer')
def place_order():
    data = request.get_json()
    if not data or not data.get('product_id') or not data.get('quantity'):
        return jsonify({'error': 'Product ID and quantity are required'}), 400
    data['buyer_id'] = request.user['user_id']
    order_id, error = create_order(data)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'message': 'Order placed successfully', 'id': order_id}), 201


@order_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])
@role_required('admin')
def remove_order(order_id):
    delete_order(order_id)
    return jsonify({'message': 'Order deleted'})
