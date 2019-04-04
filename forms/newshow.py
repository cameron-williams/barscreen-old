from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,  SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class NewShowForm(FlaskForm):
    show_name = StringField("Show Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"rows": 4})
    lookback = IntegerField("Look Back", validators=[DataRequired()])
    order = SelectField("Order", choices=[('recent', 'Most Recent'), ('random', 'Random')])
    submit = SubmitField("Submit")
