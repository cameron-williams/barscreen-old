from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "Email"})
    message = TextAreaField("Message", validators=[DataRequired()], render_kw={"placeholder": "Message", "rows": 4})
    submit = SubmitField("Send")
