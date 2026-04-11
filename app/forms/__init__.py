"""
MZB_ Forms - WTForms for validation
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20)])
    stage = SelectField('Stage', choices=[
        ('ideation', 'Ideation'),
        ('mvp', 'MVP'),
        ('growth', 'Growth'),
        ('live', 'Live')
    ], validators=[DataRequired()])
    support_needed = SelectField('Support Needed', choices=[
        ('', 'No support needed'),
        ('code_review', 'Code Review'),
        ('ui_help', 'UI/UX Help'),
        ('debugging', 'Debugging'),
        ('scaling', 'Scaling Advice'),
        ('collaboration', 'Collaboration')
    ], validators=[Optional()])
    submit = SubmitField('Create Project')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Post Comment')