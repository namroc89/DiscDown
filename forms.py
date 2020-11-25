from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email, Length, InputRequired, URL


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])


class RegisterForm(FlaskForm):
    """For to register a new user"""
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=6)])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])


class EditUser(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=6)])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    location = StringField('Location', validators=[Length(max=20)])
    bio = TextAreaField('Bio', validators=[Length(max=200)])
    fav_course = StringField('Favorite Course', validators=[Length(max=20)])
    avatar = StringField('Avatar Image')
