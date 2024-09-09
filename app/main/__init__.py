from flask import Blueprint

#create the blueprint for main
main_bp = Blueprint('main', __name__,template_folder="templates", url_prefix='/')

#Import routes so they are registred with the blueprints
from app.main import routes 