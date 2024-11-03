import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db, mail
from app.auth.forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from .models import User, Preferences, Schedule, Holiday, Student
from app.auth import auth_bp
from datetime import datetime, timedelta, timezone
from flask_mail import Message
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Route for Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

# Route for registration
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing_user:
            flash('User with that email or username already exists.', 'danger')
            return render_template('register.html', form=form)
        user = User(email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created. Please complete your profile.', 'success')
        return redirect(url_for('auth.basic_preferences'))
    return render_template('register.html', form=form)

# Route for basic preferences
@auth_bp.route('/preferences/basic', methods=['GET', 'POST'])
@login_required
def basic_preferences():
    if request.method == 'POST':
        preferences_data = request.form.to_dict()
        preferences = Preferences.query.filter_by(user_id=current_user.id).first()
        if not preferences:
            preferences = Preferences(user_id=current_user.id, **preferences_data)
            db.session.add(preferences)
        else:
            for key, value in preferences_data.items():
                setattr(preferences, key, value)
        db.session.commit()
        flash('Basic preferences updated successfully.', 'success')
        return redirect(url_for('auth.schedule_preferences'))
    return render_template('preferences.html')

# Route for schedule preferences
@auth_bp.route('/preferences/schedule', methods=['GET', 'POST'])
@login_required
def schedule_preferences():
    if request.method == 'POST':
        schedule_data = request.form.to_dict()
        schedule = Schedule.query.filter_by(user_id=current_user.id).first()
        if not schedule:
            schedule = Schedule(user_id=current_user.id, **schedule_data)
            db.session.add(schedule)
        else:
            for key, value in schedule_data.items():
                setattr(schedule, key, value)
        db.session.commit()
        flash('Schedule updated successfully.', 'success')
        return redirect(url_for('auth.student_preferences'))
    return render_template('preferences_schedule.html')

# Route for student preferences
@auth_bp.route('/preferences/students', methods=['GET', 'POST'])
@login_required
def student_preferences():
    if request.method == 'POST':
        student_data = request.form.to_dict()
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            student = Student(user_id=current_user.id, **student_data)
            db.session.add(student)
        else:
            for key, value in student_data.items():
                setattr(student, key, value)
        db.session.commit()
        flash('Student information updated successfully.', 'success')
        return redirect(url_for('auth.holiday_preferences'))
    return render_template('preferences_students.html')

# Route for holiday preferences
@auth_bp.route('/preferences/holidays', methods=['GET', 'POST'])
@login_required
def holiday_preferences():
    if request.method == 'POST':
        holiday_data = request.form.to_dict()
        holiday = Holiday.query.filter_by(user_id=current_user.id).first()
        if not holiday:
            holiday = Holiday(user_id=current_user.id, **holiday_data)
            db.session.add(holiday)
        else:
            for key, value in holiday_data.items():
                setattr(holiday, key, value)
        db.session.commit()
        flash('Holiday preferences updated successfully.', 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('preferences_holidays.html')


# Route for forgot password
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            now = datetime.now(timezone.utc)
            if user.last_password_reset_request and now - user.last_password_reset_request < timedelta(minutes=15):
                flash('You can only request a password reset once every 15 minutes.', 'warning')
            else:
                reset_token = user.get_reset_password_token()
                send_reset_email(user.email, reset_token)
                user.last_password_reset_request = now
                db.session.commit()
                flash('An email with instructions to reset your password has been sent.', 'info')
                return redirect(url_for('auth.login'))
        else:
            flash('If an account exists with the provided email, you will receive password reset instructions.', 'info')
    return render_template('forgot_password.html', form=form)

def send_reset_email(to_email, token):
    subject = "Password Reset Request"
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    body = f"To reset your password, visit the following link: {reset_url}\n\nIf you did not make this request, please ignore this email."

    msg = Message(subject, recipients=[to_email], body=body)
    try:
        mail.send(msg)
        logger.info(f"Password reset email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send password reset email to {to_email}: {e}")
        flash('There was an error sending the email. Please try again later.', 'danger')

# Route for reset password
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been reset. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)