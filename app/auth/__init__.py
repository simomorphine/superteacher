from flask import Blueprint

#create the blueprint for main
auth_bp = Blueprint('auth', __name__,template_folder='templates/auth', url_prefix='/auth')

#Import routes so they are registred with the blueprints
from app.auth import routes 