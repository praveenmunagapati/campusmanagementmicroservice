import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime, timedelta
import os

@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    
    # Initialize extensions
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)
    
    # Import and register blueprints
    from {service_name} import {service_name}_bp
    app.register_blueprint({service_name}_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Clean up
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def db(app):
    """Provide the database instance."""
    from flask_sqlalchemy import SQLAlchemy
    return SQLAlchemy(app)

@pytest.fixture
def auth_headers():
    """Generate authentication headers for testing."""
    def _auth_headers(token):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    return _auth_headers

@pytest.fixture
def test_user():
    """Create a test user."""
    return {
        'id': 1,
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    }

@pytest.fixture
def test_token(app, test_user):
    """Generate a test JWT token."""
    with app.app_context():
        from flask_jwt_extended import create_access_token
        return create_access_token(identity=test_user['id']) 