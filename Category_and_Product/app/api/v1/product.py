from flask import Blueprint, request, url_for
from app.api.helper import send_error, send_result, json_parse
from app.models import Category, Product
from app.gateway import authorization_require
from app import db, app
from datetime import datetime

api_products = Blueprint('product', __name__)

"""

"""
@api_products.route('/products', methods=['POST'])
@authorization_require()
def create_product():
    try:
        json_req = request.get_json()
    except:
        return send_error(message='Incorrect json format!')
    
    if json_req is None:
        return send_error("Check your json object!")
    
    json_body = json_parse(json_req)

    name = json_body.get('name')
    description = json_body.get('description')
    category_id = json_body.get('category_id')
    color = json_body.get('color')
    price = json_body.get('price')

    items = [name, description, category_id, color, price]
    for item in items:
        if item is None or item=="":
            return send_error('Empty value!')
    
    product = Product.query.filter_by(name=name).first()
    if product is not None:
        return send_error('Please try to use different title for product!')
    
    if Category.query.filter_by(id=category_id).first() is None:
        return send_error('Incorrect category. Category is missing!')
    
    product = Product(name=name, description=description, category_id=category_id, color=color, price=price)
    db.session.add(product)
    db.session.commit()

    data = product.product_to_dict()
    return send_result(data=data, message='Product is created successfully!', code=201)


"""

"""
@api_products.route('/products/<id>', methods=['GET'])
@authorization_require()
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return send_error(message='This product is missing!', code=404)

    data = product.product_to_dict()
    return send_result(data=data)

"""

"""
@api_products.route('/products', methods=['GET'])
@authorization_require()
def get_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=app.config["PRODUCTS_PER_PAGE"], error_out=False)
    serialized_products = [product.product_to_dict() for product in products]
    products_count = Product.query.count()
    next_page = url_for('product.get_products', page=products.next_num) if products.has_next else None
    prev_page = url_for('product.get_products', page=products.prev_num) if products.has_prev else None
    data = {
        'products_count' : products_count,
        'items' : serialized_products,
        'next_page' : next_page,
        'prev_page' : prev_page
    }
    return send_result(data=data)

"""

"""
@api_products.route('/products/<id>', methods=['DELETE'])
@authorization_require()
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        return send_error(message='This product is missing!')
    db.session.delete(product)
    db.session.commit()
    return send_result(message=f"Product '{product.name}' has been deleted successfully")
   

"""

"""
@api_products.route('/products/<id>', methods=['PATCH'])
@authorization_require()
def update_product(id):
    product = Product.query.get(id)
    if product is None:
        return send_error(message='This product is missing!')
    
    try:
        json_req = request.get_json()
    except:
        return send_error(message='Incorrect json format!')
    
    if json_req is None:
        return send_error("Check your json object!")
    
    json_body = json_parse(json_req)
    
    name = json_body.get('name')
    description = json_body.get('description')
    category_id = json_body.get('category_id')
    color = json_body.get('color')
    price = json_body.get('price')

    if Product.query.filter_by(name=name).first():
        return send_error(message='Name has been used!')
    if Category.query.filter_by(category_id=category_id).first() is None:
        return send_error(message='This category is missing!')

    flag = False
    if name is not None and name != product.name:
        product.name = name
        flag = True
    if description is not None and description != product.description:
        product.description = description
        flag = True
    if category_id is not None and category_id != product.category_id:
        product.category_id = category_id
        flag = True
    if color is not None and color != product.color:
        product.color = color
        flag = True
    if price is not None and price != product.price:
        product.price = price
        flag = True
    if flag == True:
        product.updated_date = datetime.now()

    db.session.commit()

    return send_result(message=f"Category has been updated successfully")
    