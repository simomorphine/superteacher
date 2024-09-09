from flask import Blueprint, render_template
from app.main import main_bp

@main_bp.route('/')
def home():
    return render_template("index.html")

