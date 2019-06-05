from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired


class DashNewPromoForm(FlaskForm):
    promo_name = StringField("Promo Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"rows": 4})
    promo_file = FileField("Channel File", validators=[DataRequired()])
    submit = SubmitField("Submit")
