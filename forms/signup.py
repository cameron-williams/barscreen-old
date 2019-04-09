from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SignupForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()], render_kw={"placeholder": "Frank"})
    last_name = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder": "Reynolds"})
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "mantis.toboggan@paddyspub.com"})
    phone = StringField("Phone", validators=[DataRequired()], render_kw={"placeholder": "267 750 9000"})
    company = StringField("Company", validators=[DataRequired()], render_kw={"placeholder": "Paddy's Pub"})
    submit = SubmitField("Submit")
