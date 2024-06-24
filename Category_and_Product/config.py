import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'product_and_category.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = 'Secret_key'

    # PAGINATION CONFIG
    CATEGORIES_PER_PAGE = 3
    PRODUCTS_PER_PAGE = 3