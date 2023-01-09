from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, Length, Email, DataRequired, ValidationError
from gis.models import User


# Registration form with validations support
class RegisterForm(FlaskForm):

    # functions to validate the username and email to be unique
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('User already exists!')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('E-mail already registered!')

    username = StringField(label='Username', validators=[Length(min=2, max=50), DataRequired()])
    first_name = StringField(label='First Name', validators=[Length(min=2, max=50), DataRequired()])
    last_name = StringField(label='Last Name', validators=[Length(min=2, max=50), DataRequired()])
    email = StringField(label='E-Mail', validators=[Email(), DataRequired()])
    affiliation = StringField(label='Current affiliation', validators=[Length(max=100), DataRequired()])
    passwd = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    confirm_passwd = PasswordField(label='Confirm password', validators=[EqualTo('passwd'), DataRequired()])
    submit = SubmitField(label='Create Account')
