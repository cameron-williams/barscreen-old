from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class CreatePassword(FlaskForm):
    token = HiddenField("Submit Token", validators=[DataRequired()])
    password = PasswordField("New Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
