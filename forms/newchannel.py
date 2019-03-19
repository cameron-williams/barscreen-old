from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

class NewchannelForm(FlaskForm):
    channel_name = StringField("Channel Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"rows": 4})
    channel_img = FileField("Channel Image", [validators.regexp(u'^[^/\\]\.jpg$')])
    submit = SubmitField("Submit")
