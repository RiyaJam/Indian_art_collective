import os
from flask import current_app
from werkzeug.utils import secure_filename
import uuid


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return f"/static/uploads/{filename}"
    return None


def paginate(query_result, page, per_page=12):
    total = len(query_result)
    start = (page - 1) * per_page
    end = start + per_page
    items = query_result[start:end]
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }


def success_response(data=None, message='Success', status=200):
    resp = {'success': True, 'message': message}
    if data is not None:
        resp['data'] = data
    return resp, status


def error_response(message='An error occurred', status=400):
    return {'success': False, 'error': message}, status
