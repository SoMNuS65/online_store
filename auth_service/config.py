import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'product_and_category.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = 'Secret_key'

    # MAIL CONFIG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'ramazanshaykudinov@gmail.com'
    MAIL_PASSWORD = "xmwtoygcfwmkuwhm"