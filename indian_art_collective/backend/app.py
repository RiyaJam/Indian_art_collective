import pymysql
pymysql.install_as_MySQLdb()
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from db import init_db

from routes.auth_routes import auth_bp
from routes.artisan_routes import artisan_bp
from routes.buyer_routes import buyer_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.admin_routes import admin_bp
from routes.exhibition_routes import exhibition_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)
    init_db(app)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(artisan_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(exhibition_bp)

    @app.route('/static/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/api/stats')
    def public_stats():
        from db import get_cursor
        cur = get_cursor()
        cur.execute("SELECT COUNT(*) as total FROM ARTISANS")
        artisans = cur.fetchone()['total']
        cur.execute("SELECT COUNT(*) as total FROM PRODUCT WHERE Stock_Quantity > 0")
        products = cur.fetchone()['total']
        cur.execute("SELECT COUNT(*) as total FROM ORDERS")
        orders = cur.fetchone()['total']
        cur.execute("SELECT COUNT(*) as total FROM BUYER")
        buyers = cur.fetchone()['total']
        return {'artisans': artisans, 'products': products, 'orders': orders, 'buyers': buyers}

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {'error': 'Internal server error'}, 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
