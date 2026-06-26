from flask import Blueprint, request, jsonify
from models.product_model import *
from utils.auth import token_required, role_required
from utils.helpers import save_uploaded_file

product_bp = Blueprint('product', __name__)


@product_bp.route('/api/products', methods=['GET'])
def list_products():
    filters = {
        'search': request.args.get('search'),
        'min_price': request.args.get('min_price'),
        'max_price': request.args.get('max_price'),
        'category': request.args.get('category'),
        'region': request.args.get('region'),
        'skill_level': request.args.get('skill_level'),
        'sort': request.args.get('sort', 'latest')
    }
    products = get_all_products(filters)
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 12))
    total = len(products)
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify({
        'items': products[start:end],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    })


@product_bp.route('/api/products/featured', methods=['GET'])
def featured_products():
    products = get_featured_products(6)
    return jsonify(products)


@product_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product)


@product_bp.route('/api/products/artisan/<int:artisan_id>', methods=['GET'])
def artisan_products(artisan_id):
    products = get_products_by_artisan(artisan_id)
    return jsonify(products)


@product_bp.route('/api/products', methods=['POST'])
@role_required('artisan', 'admin')
def add_product():
    # Handle multipart form data for image upload
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = request.form.to_dict()
        image_url = None
        if 'image' in request.files:
            image_url = save_uploaded_file(request.files['image'])
        if image_url:
            data['image_url'] = image_url
    else:
        data = request.get_json()

    if request.user['role'] == 'artisan':
        data['artisan_id'] = request.user['user_id']

    required = ['product_name', 'price', 'artisan_id']
    if not all(data.get(f) for f in required):
        return jsonify({'error': 'Product name, price, and artisan_id are required'}), 400

    product_id = create_product(data)
    return jsonify({'message': 'Product created', 'id': product_id}), 201


@product_bp.route('/api/products/<int:product_id>', methods=['PUT'])
@token_required
def edit_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    if request.user['role'] == 'artisan' and product['Artisan_ID'] != request.user['user_id']:
        return jsonify({'error': 'Access forbidden'}), 403

    if request.content_type and 'multipart/form-data' in request.content_type:
        data = request.form.to_dict()
        if 'image' in request.files:
            image_url = save_uploaded_file(request.files['image'])
            if image_url:
                data['image_url'] = image_url
        if not data.get('image_url'):
            data['image_url'] = product['Image_URL']
    else:
        data = request.get_json()
        if not data.get('image_url'):
            data['image_url'] = product['Image_URL']

    update_product(product_id, data)
    return jsonify({'message': 'Product updated'})


@product_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
@token_required
def remove_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    if request.user['role'] == 'artisan' and product['Artisan_ID'] != request.user['user_id']:
        return jsonify({'error': 'Access forbidden'}), 403
    delete_product(product_id)
    return jsonify({'message': 'Product deleted'})
