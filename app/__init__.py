from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)  # Ensure Migrate is initialized after db

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Set the login view
    mail.init_app(app)

    # Register Blueprints
    from app.main import main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.evaluations import eval_bp
    app.register_blueprint(eval_bp, url_prefix='/evaluations')

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.auth.models import User  # Import User inside the function to avoid circular imports
    return User.query.get(int(user_id))
