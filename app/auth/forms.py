from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already in use. Please choose a different one.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already in use. Please choose a different one.')

class PreferencesForm(FlaskForm):
    teacher_type = StringField('Teacher Type', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired()])
    school_name = StringField('School Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Save Preferences')

class ScheduleForm(FlaskForm):
    schedule_data = TextAreaField('Schedule Data', validators=[DataRequired()])
    submit = SubmitField('Save Schedule')

class StudentListForm(FlaskForm):
    student_list = TextAreaField('Student List', validators=[DataRequired()])
    submit = SubmitField('Save Student List')

class HolidayListForm(FlaskForm):
    holiday_list = TextAreaField('Holiday List', validators=[DataRequired()])
    submit = SubmitField('Save Holiday List')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Request Password Reset')

class VerifyCodeForm(FlaskForm):
    code = StringField('Verification Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify Code')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')
