from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, EqualTo


class CreatePassword(FlaskForm):
    token = HiddenField("Submit Token", validators=[DataRequired()])
    password = PasswordField("Password",
                             validators=[DataRequired(), EqualTo(fieldname='confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Submit")
