import os
from flask import Blueprint

template_dir = os.path.join(os.path.dirname(__file__), '../templates/main')
#create the blueprint for main
main_bp = Blueprint('main', __name__,template_folder=template_dir, url_prefix='/')

#Import routes so they are registred with the blueprints
from app.main import routes 