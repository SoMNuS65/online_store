from store_app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, index=True)
    description = db.Column(db.String(256), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    goods = db.relationship('Good', backref='category', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Category : {self.title}>'
    
    def serialize_category(self):
        data = {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'parent' : self.parent_id,
            'subcategory' : self.children
        }
        return data
    
class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, index=True)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self) -> str:
        return f'<Category : {self.title}>'
    
    def serialize_good(self):
        data = {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'price' : self.price,
            'category_id' : self.category_id
        }
        return data