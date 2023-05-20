from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, email_validator


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    nameofproperty = StringField('Address', validators=[DataRequired()])
    rentpaid = StringField('Rent', validators=[DataRequired()])
    amenitiesnearby = SelectField('Amenities', choices=[('Excellent'), ('Good'), ('Average'), ('Poor')], validators=[DataRequired()])
    landlordagent = SelectField('Responsiveness of Agent/Landlord', choices=[('Excellent'), ('Good'), ('Average'), ('Poor')], validators=[DataRequired()])
    transport = SelectField('Public Transport Options Nearby', choices=[('Excellent'), ('Good'), ('Average'), ('Poor')], validators=[DataRequired()])
    security = SelectField('Security', choices=[('Excellent'), ('Good'), ('Average'), ('Poor')], validators=[DataRequired()])
    deposit = BooleanField('Deposit Return - Tick if Received Deposit', validators=[DataRequired()])
    comments = TextAreaField('Comments', validators=[DataRequired()])
    submit = SubmitField('Submit Review')



