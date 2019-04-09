from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired


class NewClipForm(FlaskForm):
    clip_name = StringField("Clip Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"rows": 4})
    clip_file = FileField("Channel File", validators=[DataRequired()])
    submit = SubmitField("Submit")
