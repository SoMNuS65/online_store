from app import db, app
from app.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'User' : User}

if __name__ == '__main__':
    """
    Main Auth Application
    python server.py
    """
    app.run(host='localhost', port=5012)