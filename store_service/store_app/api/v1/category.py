from flask import request, url_for
from store_app import app, db
from store_app.models import Category
from store_app.api.v1.helper import send_error, send_result
import json


# Categories API
@app.route('/api/v1/good_categories/<id>', methods=['GET'])
def get_good_categories(id):
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return send_error(code = 404, message='The requested category is missing!')
    data = category.serialize_category()
    return send_result(data=data)

@app.route('/api/v1/good_categories', methods=['GET'])
def get_good_categories_list():
    page = request.args.get('page', 1, type=int)
    items = Category.query.paginate(page=page, per_page=app.config["CATEGORIES_PER_PAGE"], error_out=False)
    serialized_items = [item.serialize_category() for item in items]
    categories_count = Category.query.count()
    next_page = url_for('get_good_categories_list', page=items.next_num) if items.has_next else None
    prev_page = url_for('get_good_categories_list', page=items.prev_num) if items.has_prev else None
    data = {
        'categories_count' : categories_count,
        'items' : serialized_items,
        'next_page' : next_page,
        'prev_page' : prev_page
    }
    return send_result(data=data)

@app.route('/api/v1/good_categories', methods=['POST'])
def create_good_category():
    try:
        json_req = request.get_json()
    except Exception:
        return send_error(message='incorrect json format', code=400)
    
    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    title = json_body.get('title')
    if title is None or title == '':
        return send_error(message='Empty title parameter!')
    description = json_body.get('description')
    parent = json_body.get('parent')

    category = Category(title=title, description=description, parent=parent)
    db.session.add(category)
    db.session.commit()
    data = category.serialize_category()
    return send_result(message='Category has been created successfully!', data=data)

@app.route('/api/v1/good_categories/<id>', methods=['DELETE'])
def delete_good_categories(id):
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return send_error(code = 400, message='Missing categories cannot be removed!')
    db.session.delete(category)
    db.session.commit()
    return send_result(message='Category has been removed successfully!')

@app.route('/api/v1/good_categories/<id>', methods=['PATCH'])
def update_good_categories(id):
    try:
        json_req = request.get_json()
    except Exception:
        return send_error(message='incorrect json format', code=400)
    
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return send_error(code = 400, message='Missing categories cannot be updated!')
    
    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    title = json_body.get('title')
    description = json_body.get('description')
    parent = json_body.get('parent')
    if title != category.title and title is not None:
        if Category.query.filter_by(title=title).first is not None:
            return send_error(message='Missing title or already used!')
        category.title = title

    if category.description != description and parent is not None:
        category.description = description
    
    if category.parent != parent and parent is not None:
        category.parent = parent

    db.session.commit()
    return send_result(message='Category has been updated successfully!')
        

    
    
    
    
    