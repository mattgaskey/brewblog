from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class DrinkerForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )

    def __init__(self, *args, **kwargs):
        super(DrinkerForm, self).__init__(*args, **kwargs)
