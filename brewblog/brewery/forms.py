from flask import request
from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class BrewerySearchForm(FlaskForm):
    search_term = StringField(
        'search_term',
        validators=[DataRequired()]
    )

    def __init__(self, *args, **kwargs):
      if 'formdata' not in kwargs:
        kwargs['formdata'] = request.args
      if 'meta' not in kwargs:
        kwargs['meta'] = {'csrf': False}
      super(BrewerySearchForm, self).__init__(*args, **kwargs)