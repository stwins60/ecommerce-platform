from flask import Flask, session, jsonify, make_response, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS
import secrets
import os
import requests

app = Flask(__name__)
CORS(app)

# @app.before_request
# def before_request():
#     if not request.is_secure:
#         return redirect(request.url.replace("http://", "https://"))

# Ensure the model directory exists
base_dir = os.path.abspath(os.path.dirname(__file__))
model_dir = os.path.join(base_dir, '..', 'model')  # Adjust the path to ensure it points to the shared model directory
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(model_dir, "login.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Secret key for sessions
app.secret_key = secrets.token_urlsafe(16)

# Configure session to use the same SQLAlchemy database
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_PERMANENT'] = False

# Initialize Flask-Session
session_extension = Session(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

@app.route('/api/v1/product/load_products', methods=['GET'])
def load_products():
    # Fetch the product data from the external API
    response = requests.get('https://dummyjson.com/products')
    
    if response.status_code != 200:
        return make_response(jsonify({'error': 'Failed to fetch product data'}), 500)
    
    products_data = response.json()['products']
    
    # Add each product to the database
    for product_data in products_data:
        product = Product(
            name=product_data['title'],  # Mapping title to name
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['stock']
        )
        db.session.add(product)
    
    db.session.commit()

    return make_response(jsonify({'message': 'Products loaded successfully'}), 201)

@app.route('/api/v1/product', methods=['GET'])
def get_product():
    return make_response(jsonify({
            'products': [
                {
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'quantity': product.quantity
                } for product in Product.query.all()
            ]
        }), 200)
    # if 'username' in session:
    #     print(session['username'])
    #     username = session['username']
    #     return make_response(jsonify({
    #         'products': [
    #             {
    #                 'name': product.name,
    #                 'description': product.description,
    #                 'price': product.price,
    #                 'quantity': product.quantity
    #             } for product in Product.query.all()
    #         ]
    #     }), 200)
    # else:
    #     return make_response(jsonify({'error': 'Unauthorized access, please log in first.'}), 401)
    
@app.route('/api/v1/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    if 'username' in session:
        username = session['username']
        product = Product.query.get(product_id)
        if product:
            return make_response(jsonify({
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'quantity': product.quantity
            }), 200)
        else:
            return make_response(jsonify({'error': 'Product not found'}), 404)
    else:
        return make_response(jsonify({'error': 'Unauthorized access, please log in first.'}), 401)
    
@app.route('/api/v1/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if 'username' in session:
        username = session['username']
        product = Product.query.get(product_id)
        if product:
            data = request.get_json()
            if not data:
                return make_response(jsonify({'error': 'No data provided'}), 400)
            
            if 'name' in data:
                product.name = data['name']
            if 'description' in data:
                product.description = data['description']
            if 'price' in data:
                product.price = data['price']
            if 'quantity' in data:
                product.quantity = data['quantity']
            
            db.session.commit()
            return make_response(jsonify({'message': 'Product updated successfully'}), 200)
        else:
            return make_response(jsonify({'error': 'Product not found'}), 404)
    else:
        return make_response(jsonify({'error': 'Unauthorized access, please log in first.'}), 401)
    
@app.route('/api/v1/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'username' in session:
        username = session['username']
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return make_response(jsonify({'message': 'Product deleted successfully'}), 200)
        else:
            return make_response(jsonify({'error': 'Product not found'}), 404)
    else:
        return make_response(jsonify({'error': 'Unauthorized access, please log in first.'}), 401)
    
@app.route('/api/v1/product', methods=['POST'])
def add_product():
    if 'username' in session:
        username = session['username']
        data = request.get_json()
        if not data or not data.get('name') or not data.get('description') or not data.get('price') or not data.get('quantity'):
            return make_response(jsonify({'error': 'Name, description, price, and quantity required'}), 400)
        
        product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            quantity=data['quantity']
        )
        db.session.add(product)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Product added successfully'}), 201)
    else:
        return make_response(jsonify({'error': 'Unauthorized access, please log in first.'}), 401)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5004)
