from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import DevelopmentConfig  # Import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # Initialize Migrate

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load config from config.py

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import blueprints
    from .auth.routes import auth
    from .accounts.routes import accounts
    from .main.routes import main

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(accounts, url_prefix='/accounts')
    app.register_blueprint(main)

    return app
