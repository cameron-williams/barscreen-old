from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class CreatePassword(FlaskForm):
    token = HiddenField("Submit Token", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()],validators.EqualTo('confirm', message='Passwords must match'))
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Submit")
