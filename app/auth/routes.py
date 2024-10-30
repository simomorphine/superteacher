import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.auth.forms import LoginForm, RegistrationForm, ForgotPasswordForm
from .models import User, Preferences, Schedule, Holiday, Student
from app.auth import auth_bp
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Route for Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)
# Route for registration
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created. Please complete your profile.', 'success')
        return redirect(url_for('auth.preferences'))
    return render_template('register.html', form=form)

# Route for preferences
@auth_bp.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    if request.method == 'POST':
        preferences_data = request.form.to_dict()
        preferences = Preferences(user_id=current_user.id, **preferences_data)
        db.session.add(preferences)
        db.session.commit()
        flash('Preferences updated successfully.', 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('preferences.html')

# Route for forgot password
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            reset_token = user.get_reset_password_token()
            send_reset_email(user.email, reset_token)
            flash('An email with instructions to reset your password has been sent.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('No account found with that email.', 'warning')
    return render_template('forgot_password.html', form=form)

def send_reset_email(to_email, token):
    api_key = os.getenv('ELASTIC_EMAIL_API_KEY')
    api_url = os.getenv('ELASTIC_EMAIL_API_URL')
    from_email = os.getenv('FROM_EMAIL')
    subject = "Password Reset Request"
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    body = f"To reset your password, visit the following link: {reset_url}\n\nIf you did not make this request, please ignore this email."

    payload = {
        "apikey": api_key,
        "from": from_email,
        "to": to_email,
        "subject": subject,
        "bodyText": body
    }

    response = requests.post(api_url, data=payload)
    if response.status_code != 200:
        flash('Failed to send email. Please try again later.', 'danger')