import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from .models import User, Preferences, Schedule, Holiday, Student
from app.auth import auth_bp
from datetime import datetime, timedelta
from twilio.rest import Client

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
        return redirect(url_for('auth.schedule'))
    return render_template('preferences.html')

# Route for schedule
@auth_bp.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'POST':
        schedule_data = request.get_json()
        for day, hours in schedule_data.items():
            for hour in hours:
                new_schedule_entry = Schedule(
                    day_of_week=day,
                    start_time=datetime.strptime(hour, "%H:%M").time(),
                    end_time=(datetime.strptime(hour, "%H:%M") + timedelta(hours=1)).time(),
                    user_id=current_user.id
                )
                db.session.add(new_schedule_entry)
        db.session.commit()
        return redirect(url_for('auth.students'))
    return render_template('calendar.html')

# Route for student lists
@auth_bp.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    if request.method == 'POST':
        if 'studentFile' in request.files:
            student_file = request.files['studentFile']
            import pandas as pd
            df = pd.read_excel(student_file)
            for _, row in df.iterrows():
                student = Student(name=row['Name'], age=row.get('Age'), user_id=current_user.id)
                db.session.add(student)
        else:
            student_data = request.form.get('studentList')
            if student_data:
                students = student_data.split(',')
                for student_name in students:
                    student = Student(name=student_name.strip(), user_id=current_user.id)
                    db.session.add(student)
        db.session.commit()
        return redirect(url_for('auth.holidays'))
    return render_template('students.html')

# Route for holidays
@auth_bp.route('/holidays', methods=['GET', 'POST'])
@login_required
def holidays():
    if request.method == 'POST':
        holiday_data = request.form.get('holidayList')
        if holiday_data:
            holidays = holiday_data.split(',')
            for holiday_name in holidays:
                holiday = Holiday(name=holiday_name.strip(), user_id=current_user.id)
                db.session.add(holiday)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('holidays.html')

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
    return redirect(url_for('main.home'))

# Route for password reset request
@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            import random
            verification_code = random.randint(100000, 999999)
            session['verification_code'] = verification_code
            session['user_email'] = email

            client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")
            client.messages.create(
                body=f'Your verification code is {verification_code}',
                from_='+1234567890',
                to='+1987654321'
            )
            flash('A verification code has been sent to your email.', 'info')
            return redirect(url_for('auth.verify_code'))
        flash('Invalid email address.', 'danger')
    return render_template('reset_password.html')

# Route for verification code
@auth_bp.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
        entered_code = request.form.get('code')
        if int(entered_code) == session.get('verification_code'):
            flash('Code verified. You may now reset your password.', 'success')
            return redirect(url_for('auth.reset_password_form'))
        else:
            flash('Invalid verification code.', 'danger')
    return render_template('verify_code.html')

# Route for resetting password
@auth_bp.route('/reset_password_form', methods=['GET', 'POST'])
def reset_password_form():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password == confirm_password:
            user = User.query.filter_by(email=session.get('user_email')).first()
            if user:
                user.set_password(new_password)
                db.session.commit()
                flash('Your password has been updated. You may now log in.', 'success')
                return redirect(url_for('auth.login'))
        else:
            flash('Passwords do not match.', 'danger')
    return render_template('reset_password_form.html')
