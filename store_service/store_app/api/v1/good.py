from flask import request, url_for
from store_app import app, db
from store_app.models import Good, Category
from store_app.api.v1.helper import send_error, send_result
import json


# Categories API
@app.route('/api/v1/goods/<id>', methods=['GET'])
def get_goods(id):
    good = Good.query.filter_by(id=id).first()
    if good is None:
        return send_error(code = 404, message='The requested good is missing!')
    data = good.serialize_good()
    return send_result(data=data)

@app.route('/api/v1/goods', methods=['GET'])
def get_goods_list():
    page = request.args.get('page', 1, type=int)
    items = Good.query.paginate(page=page, per_page=app.config["CATEGORIES_PER_PAGE"], error_out=False)
    serialized_items = [item.serialize_good() for item in items]
    good_count = Good.query.count()
    next_page = url_for('get_goods_list', page=items.next_num) if items.has_next else None
    prev_page = url_for('get_goods_list', page=items.prev_num) if items.has_prev else None
    data = {
        'good_count' : good_count,
        'items' : serialized_items,
        'next_page' : next_page,
        'prev_page' : prev_page
    }
    return send_result(data=data)

@app.route('/api/v1/goods', methods=['POST'])
def create_good():
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
    if title == '' or Good.query.filter_by(title=title).first() is not None:
        return send_error(message='Empty or invalid title parameter!')
    description = json_body.get('description')
    category_id = json_body.get('category_id')
    price = json_body.get('price')

    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return send_error(message="Missing category!")
    good = Good(title=title, description=description, category=category, price=price)
    db.session.add(good)
    db.session.commit()
    data = good.serialize_good()
    return send_result(message='Good has been created successfully!', data=data)

@app.route('/api/v1/goods/<id>', methods=['DELETE'])
def delete_good(id):
    good = Good.query.filter_by(id=id).first()
    if good is None:
        return send_error(code = 400, message='Missing categories cannot be removed!')
    db.session.delete(good)
    db.session.commit()
    return send_result(message='Good has been removed successfully!')

@app.route('/api/v1/goods/<id>', methods=['PATCH'])
def update_good(id):
    try:
        json_req = request.get_json()
    except Exception:
        return send_error(message='incorrect json format', code=400)
    
    good = Good.query.filter_by(id=id).first()
    if good is None:
        return send_error(code = 400, message='Missing categories cannot be updated!')
    
    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    title = json_body.get('title')
    description = json_body.get('description')
    price = json_body.get('price')
    category_id = json_body.get('category_id')
    if title != good.title and title is not None:
        if Good.query.filter_by(title=title).first is not None:
            return send_error(message='Missing title or already used!')
        good.title = title

    current_category = Category.query.filter_by(id=category_id).first()
    if good.category_id != current_category.id and current_category is not None:
        good.category = current_category

    if good.description != description and price is not None:
        good.description = description
    
    if good.price != price and price is not None:
        good.price = price

    db.session.commit()
    return send_result(message='Good has been updated successfully!')
        