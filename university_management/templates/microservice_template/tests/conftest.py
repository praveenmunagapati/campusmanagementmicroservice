import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask application for testing."""
    app = Flask(__name__)
    app.config.from_object('config.TestingConfig')
    
    # Initialize extensions
    db = SQLAlchemy()
    migrate = Migrate()
    jwt = JWTManager()
    cache = Cache()
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    cache.init_app(app)
    limiter.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
    yield app
    
    # Clean up
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='session')
def db(app):
    """Provide the database session."""
    return app.extensions['sqlalchemy'].db

@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    
    db.session = session
    
    yield session
    
    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a CLI runner for the app."""
    return app.test_cli_runner()

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
def mock_cache(app):
    """Mock the cache for testing."""
    cache = Cache()
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    return cache

@pytest.fixture
def mock_limiter(app):
    """Mock the rate limiter for testing."""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    return limiter 