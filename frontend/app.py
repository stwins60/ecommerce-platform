from flask import Flask, request, render_template, redirect, make_response
import os
from dotenv import load_dotenv
import requests
from flask_cors import CORS

load_dotenv()

REGISTER_URL = os.getenv('REGISTER_URL')
LOGIN_URL = os.getenv('LOGIN_URL')
PRODUCTS_URL = os.getenv('PRODUCTS_URL')

app = Flask(__name__)
CORS(app)

# @app.before_request
# def before_request():
#     if not request.is_secure:
#         return redirect(request.url.replace("http://", "https://"))

def load_products():
    BASE_URL = PRODUCTS_URL
    response = requests.get(BASE_URL+'/load_products')
    if response.status_code != 200:
        return "Failed to fetch product data"
    return response.json()
    

@app.route('/', methods=['GET', 'POST'])
def index():
    products=""
    if request.method == 'POST':
        products = ""
        username = request.form['login-username']
        password = request.form['login-password']
        
        if username == '' or password == '':
            return render_template('index.html', error='Please fill in all the fields')
        
        
        # Send the data to the login microservice
        response = requests.post(LOGIN_URL, json={'username': username, 'password': password})
        print(response.text)
        if response.status_code != 200:
            return render_template('index.html', error='An error occurred while logging in')
        if "Login successful" in response.text:
            return redirect('products')
        else:
            return render_template('index.html', error='invalid credentials. Please try again')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['register-username']
        password = request.form['register-password']
        
        if username == '' or password == '':
            return render_template('register.html', error='Please fill in all the fields')
        
        # Send the data to the login microservice
        response = requests.post(REGISTER_URL, json={'username': username, 'password': password})
        if response.status_code != 200:
            return render_template('register.html', error='An error occurred while registering')
        
        redirect_url = request.args.get('next', '/')
        return redirect(redirect_url)
        
    return render_template('register.html')

@app.route('/products', methods=['GET'])
def products():
    load_products()
    product_response = requests.get(PRODUCTS_URL)
    products = product_response.json()['products']
    return make_response(
        render_template('products.html', products=products),
        200
    )

@app.route('/logout', methods=['GET'])
def logout():
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)