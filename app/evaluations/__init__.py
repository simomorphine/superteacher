import os
from flask import Blueprint

template_dir = os.path.join(os.path.dirname(__file__), '../templates/evaluations')
#create the blueprint for main
eval_bp = Blueprint('eval', __name__,template_folder=template_dir, url_prefix='/eval')

#Import routes so they are registred with the blueprints
from app.evaluations import routes 