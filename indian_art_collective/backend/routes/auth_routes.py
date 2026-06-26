from flask import Blueprint, request, jsonify
from models.artisan_model import get_artisan_by_email, create_artisan
from models.buyer_model import get_buyer_by_email, create_buyer
from utils.auth import check_password, generate_token
from db import get_cursor

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth/login/admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    cur = get_cursor()
    cur.execute("SELECT * FROM ADMIN WHERE Username=%s", (data['username'],))
    admin = cur.fetchone()
    if not admin or not check_password(data['password'], admin['Password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = generate_token(admin['Admin_ID'], 'admin', admin['Username'])
    return jsonify({'token': token, 'role': 'admin', 'name': admin['Username'], 'id': admin['Admin_ID']})


@auth_bp.route('/api/auth/login/artisan', methods=['POST'])
def login_artisan():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    artisan = get_artisan_by_email(data['email'])
    if not artisan or not check_password(data['password'], artisan['Password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = generate_token(artisan['Artisan_ID'], 'artisan', artisan['Name'])
    return jsonify({'token': token, 'role': 'artisan', 'name': artisan['Name'], 'id': artisan['Artisan_ID']})


@auth_bp.route('/api/auth/login/buyer', methods=['POST'])
def login_buyer():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    buyer = get_buyer_by_email(data['email'])
    if not buyer or not check_password(data['password'], buyer['Password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = generate_token(buyer['Buyer_ID'], 'buyer', buyer['Name'])
    return jsonify({'token': token, 'role': 'buyer', 'name': buyer['Name'], 'id': buyer['Buyer_ID']})


@auth_bp.route('/api/auth/register/artisan', methods=['POST'])
def register_artisan():
    data = request.get_json()
    required = ['name', 'email', 'password']
    if not all(data.get(f) for f in required):
        return jsonify({'error': 'Name, email and password are required'}), 400
    existing = get_artisan_by_email(data['email'])
    if existing:
        return jsonify({'error': 'Email already registered'}), 409
    artisan_id = create_artisan(data)
    return jsonify({'message': 'Artisan registered successfully', 'id': artisan_id}), 201


@auth_bp.route('/api/auth/register/buyer', methods=['POST'])
def register_buyer():
    data = request.get_json()
    required = ['name', 'email', 'password']
    if not all(data.get(f) for f in required):
        return jsonify({'error': 'Name, email and password are required'}), 400
    existing = get_buyer_by_email(data['email'])
    if existing:
        return jsonify({'error': 'Email already registered'}), 409
    buyer_id = create_buyer(data)
    return jsonify({'message': 'Buyer registered successfully', 'id': buyer_id}), 201
