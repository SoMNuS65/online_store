from store_app import app, db
from store_app.models import Category, Good

@app.shell_context_processor
def make_shell_context():
    return {'app' : app, 'db' : db, 'Category' : Category, "Good" : Good}

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)