from auth_app import app, db
from auth_app.models import Validation, User

@app.shell_context_processor
def make_shell_context():
    return {'app' : app, 'db' : db, 'User' : User, 'Validation' : Validation}

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)