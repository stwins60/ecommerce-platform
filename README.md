# eCommerce Platform

This is a scalable eCommerce platform built using Flask microservices architecture. Each service is designed to handle a specific part of the eCommerce process, such as user authentication, product management, and order processing.

## Microservices

The platform is composed of the following microservices:
1. [Login Microservice](login-microservice/README.md): Handles user registration, authentication, and logout.
2. [Product Microservice](product-microservice/README.md): Manages product information, including loading, retrieving, adding, updating, and deleting products.
3. [Frontend Microservice](frontend/README.md): Provides a web interface for users to interact with the platform.

Each microservice is designed to be independent and can be deployed separately, allowing for scalability and flexibility in managing the platform.

## Features
1. **User Registration**: Users can register by providing a username and password.
2. **User Authentication**: Registered users can log in to access the platform.
3. **User Logout**: Users can log out of the platform.
4. **Load Products**: The product microservice loads products from a JSON file.
5. **Get Products**: The product microservice provides an endpoint to retrieve all products.
6. **Get Product by ID**: The product microservice provides an endpoint to retrieve a product by ID.
7. **Add Product**: The product microservice provides an endpoint to add a new product.
8. **Update Product**: The product microservice provides an endpoint to update an existing product.
9. **Delete Product**: The product microservice provides an endpoint to delete a product by ID.
10. **Web Interface**: The frontend microservice provides a web interface for users to interact with the platform.

## Requirements
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Session
- Flask-CORS
- Werkzeug
- Requests

## Installation
Follow the installation instructions for each microservice to set up the platform on your local machine.

## Usage
1. Start the login microservice to handle user registration, authentication, and logout.
2. Start the product microservice to manage product information.
3. The frontend microservice will require the login and product microservices to be running to provide a complete eCommerce platform experience.

## License
This project is licensed under Open Source License.
