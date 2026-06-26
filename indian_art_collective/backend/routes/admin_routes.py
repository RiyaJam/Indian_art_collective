from flask import Blueprint, request, jsonify, make_response
from db import get_cursor
from models.scheme_model import *
from models.artisan_model import get_all_artisans, create_artisan
from models.buyer_model import get_all_buyers
from utils.auth import role_required
import csv
import io

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/api/admin/dashboard', methods=['GET'])
@role_required('admin')
def dashboard():
    cur = get_cursor()
    cur.execute("SELECT COUNT(*) as total FROM ARTISANS")
    artisans = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM BUYER")
    buyers = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM PRODUCT")
    products = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM ORDERS")
    orders = cur.fetchone()['total']
    cur.execute("SELECT COALESCE(SUM(Total_Amount),0) as revenue FROM ORDERS")
    revenue = float(cur.fetchone()['revenue'])
    cur.execute("SELECT COUNT(*) as total FROM EXHIBITION WHERE End_Date >= CURDATE()")
    active_exhibitions = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM GOVERNMENT_SCHEMES")
    schemes = cur.fetchone()['total']

    # Monthly revenue for chart (last 6 months)
    cur.execute("""
        SELECT DATE_FORMAT(Order_Date, '%Y-%m') as month,
               SUM(Total_Amount) as revenue,
               COUNT(*) as orders
        FROM ORDERS
        WHERE Order_Date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY month ORDER BY month
    """)
    monthly = cur.fetchall()

    # Top products
    cur.execute("""
        SELECT p.Product_Name, SUM(o.Quantity) as sold, SUM(o.Total_Amount) as revenue
        FROM ORDERS o JOIN PRODUCT p ON o.Product_ID=p.Product_ID
        GROUP BY p.Product_ID ORDER BY sold DESC LIMIT 5
    """)
    top_products = cur.fetchall()

    # State-wise artisans
    cur.execute("SELECT State, COUNT(*) as count FROM ARTISANS GROUP BY State ORDER BY count DESC")
    state_dist = cur.fetchall()

    return jsonify({
        'artisans': artisans,
        'buyers': buyers,
        'products': products,
        'orders': orders,
        'revenue': revenue,
        'active_exhibitions': active_exhibitions,
        'schemes': schemes,
        'monthly_data': monthly,
        'top_products': top_products,
        'state_distribution': state_dist
    })


@admin_bp.route('/api/admin/crafts', methods=['GET'])
def list_crafts():
    cur = get_cursor()
    cur.execute("SELECT * FROM CRAFT")
    return jsonify(cur.fetchall())


@admin_bp.route('/api/admin/crafts', methods=['POST'])
@role_required('admin')
def add_craft():
    data = request.get_json()
    cur = get_cursor()
    from db import commit
    cur.execute("""
        INSERT INTO CRAFT (Craft_Name, Category, Region, Description)
        VALUES (%s,%s,%s,%s)
    """, (data['craft_name'], data.get('category'), data.get('region'), data.get('description')))
    commit()
    return jsonify({'message': 'Craft added', 'id': cur.lastrowid}), 201


@admin_bp.route('/api/admin/crafts/<int:craft_id>', methods=['PUT'])
@role_required('admin')
def edit_craft(craft_id):
    data = request.get_json()
    cur = get_cursor()
    from db import commit
    cur.execute("""
        UPDATE CRAFT SET Craft_Name=%s, Category=%s, Region=%s, Description=%s
        WHERE Craft_ID=%s
    """, (data['craft_name'], data.get('category'), data.get('region'), data.get('description'), craft_id))
    commit()
    return jsonify({'message': 'Craft updated'})


@admin_bp.route('/api/admin/crafts/<int:craft_id>', methods=['DELETE'])
@role_required('admin')
def remove_craft(craft_id):
    cur = get_cursor()
    from db import commit
    cur.execute("DELETE FROM CRAFT WHERE Craft_ID=%s", (craft_id,))
    commit()
    return jsonify({'message': 'Craft deleted'})


# Scheme management
@admin_bp.route('/api/schemes', methods=['GET'])
def list_schemes():
    return jsonify(get_all_schemes())


@admin_bp.route('/api/schemes/<int:scheme_id>', methods=['GET'])
def get_scheme(scheme_id):
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        return jsonify({'error': 'Scheme not found'}), 404
    return jsonify(scheme)


@admin_bp.route('/api/schemes', methods=['POST'])
@role_required('admin')
def add_scheme():
    data = request.get_json()
    if not data.get('scheme_name'):
        return jsonify({'error': 'Scheme name required'}), 400
    scheme_id = create_scheme(data)
    return jsonify({'message': 'Scheme created', 'id': scheme_id}), 201


@admin_bp.route('/api/schemes/<int:scheme_id>', methods=['PUT'])
@role_required('admin')
def edit_scheme(scheme_id):
    data = request.get_json()
    update_scheme(scheme_id, data)
    return jsonify({'message': 'Scheme updated'})


@admin_bp.route('/api/schemes/<int:scheme_id>', methods=['DELETE'])
@role_required('admin')
def remove_scheme(scheme_id):
    delete_scheme(scheme_id)
    return jsonify({'message': 'Scheme deleted'})


@admin_bp.route('/api/schemes/<int:scheme_id>/enroll', methods=['POST'])
@role_required('admin')
def enroll(scheme_id):
    data = request.get_json()
    enroll_artisan(data['artisan_id'], scheme_id)
    return jsonify({'message': 'Artisan enrolled in scheme'})


@admin_bp.route('/api/schemes/<int:scheme_id>/unenroll', methods=['POST'])
@role_required('admin')
def unenroll(scheme_id):
    data = request.get_json()
    unenroll_artisan(data['artisan_id'], scheme_id)
    return jsonify({'message': 'Artisan unenrolled from scheme'})


# Export
@admin_bp.route('/api/admin/export/artisans', methods=['GET'])
@role_required('admin')
def export_artisans():
    artisans = get_all_artisans()
    si = io.StringIO()
    writer = csv.DictWriter(si, fieldnames=artisans[0].keys() if artisans else [])
    writer.writeheader()
    writer.writerows(artisans)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=artisans.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@admin_bp.route('/api/admin/export/orders', methods=['GET'])
@role_required('admin')
def export_orders():
    cur = get_cursor()
    cur.execute("""
        SELECT o.Order_ID, o.Order_Date, o.Quantity, o.Total_Amount,
               b.Name as Buyer, p.Product_Name, a.Name as Artisan
        FROM ORDERS o
        LEFT JOIN BUYER b ON o.Buyer_ID=b.Buyer_ID
        LEFT JOIN PRODUCT p ON o.Product_ID=p.Product_ID
        LEFT JOIN ARTISANS a ON p.Artisan_ID=a.Artisan_ID
        ORDER BY o.Order_Date DESC
    """)
    orders = cur.fetchall()
    si = io.StringIO()
    writer = csv.DictWriter(si, fieldnames=orders[0].keys() if orders else [])
    writer.writeheader()
    writer.writerows(orders)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=orders.csv"
    output.headers["Content-type"] = "text/csv"
    return output
