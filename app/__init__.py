from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Set the login view

    # Register Blueprints
    from app.main import main_bp  # Import the Blueprint
    app.register_blueprint(main_bp)
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.evaluations import eval_bp

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
