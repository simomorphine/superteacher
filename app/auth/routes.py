from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from .models import User
from app.auth import auth_bp
from datetime import datetime

# Route for login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

# Route for logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

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
        flash('Your account has been created. You can now log in!', 'success')
        return redirect(url_for('auth.preferences'))
    return render_template('register.html', form=form)

@login_required
@auth_bp.route('/preferences', methods=["GET","POST"])
def preferences():
    return render_template("preferences.html")

@auth_bp.route("/save_preferences", methods=["POST"])
def save_preferences():
    pass

# Route for password reset request
@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    # Implement password reset functionality here
    pass
