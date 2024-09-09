from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Register Blueprints
    from app.routes import main_bp  # Import the Blueprint
    app.register_blueprint(main_bp)

    return app
