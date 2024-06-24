from app import db
from datetime import datetime, timezone

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, index=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy=True)
    products = db.relationship('Product', backref='category', lazy=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(db.DateTime, default=datetime.now)

    def category_to_dict(self):
        if self.parent_id is not None:
            return {
                'id' : self.id,
                'title' : self.title,
                'description' : self.description,
                'parent_id' : self.parent_id,
                'parent' : {
                    'id' : self.parent.id,
                    'title' : self.parent.title
                },
                'created_date' : self.created_date,
                'updated_date' : self.updated_date
            }
        else: 
            return {
                'id' : self.id,
                'title' : self.title,
                'description' : self.description,
                'parent_id' : self.parent_id,
                'created_date' : self.created_date,
                'updated_date' : self.updated_date
            } 

    def __repr__(self):
        return f'<Category {self.title}>'
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, index=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(db.DateTime, default=datetime.now)

    def product_to_dict(self):
        if self.parent_id is not None:
            return {
                'id' : self.id,
                'name' : self.name,
                'description' : self.description,
                'color' : self.color,
                'category_id' : self.category_id,
                'category' : {
                    'id' : self.category.id,
                    'title' : self.category.title
                },
                'created_date' : self.created_date,
                'updated_date' : self.updated_date
            }