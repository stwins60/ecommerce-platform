# Flask Login Microservice

## Features

- **User Registration**: Users can register by providing a username and password.
- **User Authentication**: Registered users can log in to access the page.
- **User Logout**: Users can log out of the application.
## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Session
- Flask-CORS
- Werkzeug

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/stwins60/ecommerce-platform.git
   cd ecommerce-platform/login-microservice
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
    - **REGISTER**: `/api/v1/register` (POST)
    - **LOGIN**: `/api/v1/login` (POST)
    - **LOGOUT**: `/api/v1/logout` (GET)
    