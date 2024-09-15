import os
from flask import Blueprint

#template_dir = os.path.join(os.path.dirname(__file__), '../templates/auth')
#create the blueprint for main
auth_bp = Blueprint('auth', __name__,template_folder="templates", url_prefix='/auth')

#Import routes so they are registred with the blueprints
from app.auth import routes 