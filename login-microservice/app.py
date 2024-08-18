from flask import Flask, request, jsonify, make_response, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from functools import wraps
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

# @app.before_request
# def before_request():
#     if not request.is_secure:
#         return redirect(request.url.replace("http://", "https://"))

# Ensure the model directory exists outside the login folder
base_dir = os.path.abspath(os.path.dirname(__file__))
model_dir = os.path.join(base_dir, '..', 'model')
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(model_dir, "login.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Secret key for sessions
app.secret_key = secrets.token_urlsafe(16)

# Configure session to use the SQLAlchemy database
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_PERMANENT'] = False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Increase length for hashed passwords

    def __repr__(self):
        return '<User %r>' % self.username
    
class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' not in session:
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)
        return f(*args, **kwargs)
    
    return wrap

@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    if not data or not data.get('username') or not data.get('password'):
        return make_response(jsonify({'error': 'Username and password required'}), 400)

    if User.query.filter_by(username=data['username']).first():
        return make_response(jsonify({'error': 'User already exists'}), 400)

    hashed_password = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return make_response(jsonify({'message': 'User created successfully'}), 201)

@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    if not data or not data.get('username') or not data.get('password'):
        return make_response(jsonify({'error': 'Username and password required'}), 400)

    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return make_response(jsonify({'error': 'Invalid credentials'}), 401)

    session['username'] = user.username
    return make_response(jsonify({'message': 'Login successful'}), 200)

@app.route('/api/v1/logout', methods=['POST'])
@is_logged_in
def logout():
    session.pop('username', None)
    return make_response(jsonify({'message': 'Logout successful'}), 200)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Initialize Flask-Session after the database tables are created
        # Session(app)
    app.run(debug=True, host='0.0.0.0', port=5003)
