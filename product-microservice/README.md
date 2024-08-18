# Flask Product Microservice

## Features

- **Load Products**: The microservice loads products from a JSON file.
- **Get Products**: The microservice provides an endpoint to retrieve all products.
- **Get Product by ID**: The microservice provides an endpoint to retrieve a product by ID.
- **Add Product**: The microservice provides an endpoint to add a new product.
- **Update Product**: The microservice provides an endpoint to update an existing product.
- **Delete Product**: The microservice provides an endpoint to delete a product by ID.
## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Session
- Flask-CORS
- Requests

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/stwins60/ecommerce-platform.git
   cd ecommerce-platform/product-microservice
   ```
2.  Create a virtual environment:
    - For Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    - For macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the dependencies:**
    -  For Windows:
        ```bash
        pip install -r requirements.txt
        ```
    -  For macOS/Linux:
          ```bash
            pip3 install -r requirements.txt
            ```
4.  **Run the application:**
    -  For Windows:
        ```bash
        set FLASK_APP=app.py
        flask run
        ```
    -  For macOS/Linux:
        ```bash
        export FLASK_APP=app.py
        flask run
        ```
5.  **Access the application:**
    Open a web browser and go to `http://127.0.0.1:5003/` to view the application.
    - **Load Products**: `/api/v1/products/load_products` (POST)
    - **Get Products**: `/api/v1/products` (GET)
    - **Get Product by ID**: `/api/v1/products/<product_id>` (GET)
    - **Add Product**: `/api/v1/products` (POST)
    - **Update Product**: `/api/v1/products/<product_id>` (PUT)
    - **Delete Product**: `/api/v1/products/<product_id>` (DELETE)

