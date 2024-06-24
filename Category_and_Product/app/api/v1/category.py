from flask import Blueprint, request, url_for
from app.api.helper import send_error, send_result, json_parse
from app.models import Category
from app.gateway import authorization_require
from app import db, app
from datetime import datetime

api_category = Blueprint('category', __name__)

"""

"""
@api_category.route('/categories', methods=['POST'])
@authorization_require()
def create_category():
    try:
        json_req = request.get_json()
    except:
        return send_error(message='Incorrect json format!')
    
    if json_req is None:
        return send_error("Check your json object!")
    
    json_body = json_parse(json_req)

    title = json_body.get('title')
    description = json_body.get('description')
    parent_id = json_body.get('parent_id')

    if title is None or title=="":
        return send_error('Empty title!')
    if description is None or description=="":
        return send_error('Empty description')

    category = Category.query.filter_by(title=title).first()
    if category is not None:
        return send_error('Please try to use different title for category!')
    
    if parent_id is not None and Category.query.filter_by(id=parent_id).first() is None:
        return send_error(message='Incorrect category for being parent!')

    category = Category(title=title, description=description, parent_id=parent_id)
    db.session.add(category)
    db.session.commit()

    data = category.category_to_dict()
    return send_result(data=data, message='Category is created successfully!', code=201)

"""

"""
@api_category.route('/categories/<id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if category is None:
        return send_error(message='This category is missing!', code=404)

    data = category.category_to_dict()
    return send_result(data=data)


"""

"""
@api_category.route('/categories', methods=['GET'])
def get_categories():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.paginate(page=page, per_page=app.config["CATEGORIES_PER_PAGE"], error_out=False)
    serialized_categories = [category.category_to_dict() for category in categories]
    categories_count = Category.query.count()
    next_page = url_for('category.get_categories', page=categories.next_num) if categories.has_next else None
    prev_page = url_for('category.get_categories', page=categories.prev_num) if categories.has_prev else None
    data = {
        'categories_count' : categories_count,
        'items' : serialized_categories,
        'next_page' : next_page,
        'prev_page' : prev_page
    }
    return send_result(data=data)


"""

"""
@api_category.route('/categories/<id>', methods=['DELETE'])
@authorization_require()
def delete_categories(id):
    category = Category.query.get(id)
    if category is None:
        return send_error(message='This category is missing!')
    db.session.delete(category)
    db.session.commit()
    return send_result(message=f"Category '{category.title}' has been deleted successfully")
    

"""

"""
@api_category.route('/categories/<id>', methods=['PATCH'])
@authorization_require()
def update_categories(id):
    category = Category.query.get(id)
    if category is None:
        return send_error(message='This category is missing!')
    
    try:
        json_req = request.get_json()
    except:
        return send_error(message='Incorrect json format!')
    
    if json_req is None:
        return send_error("Check your json object!")
    
    json_body = json_parse(json_req)
    
    title = json_body.get('title')
    description = json_body.get('description')
    parent_id = json_body.get('parent_id')

    if Category.query.filter_by(title=title).first():
        return send_error(message='Title has been used!')
    if Category.query.filter_by(parent_id=parent_id).first() is None:
        return send_error(message='This Category is missing!')

    flag = False
    if title is not None and title != category.title:
        category.title = title
        flag = True
    if description is not None and description != category.description:
        category.description = description
        flag = True
    if parent_id is not None and parent_id != category.parent_id:
        category.parent_id = parent_id
        flag = True
    if flag == True:
        category.updated_date = datetime.now()

    db.session.commit()

    return send_result(message=f"Category has been updated successfully")
    