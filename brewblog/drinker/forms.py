from flask import request
from wtforms import StringField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import sqlalchemy as sa
from brewblog import db
from brewblog.models import State

class DrinkerForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[]
    )

    def __init__(self, *args, **kwargs):
        super(DrinkerForm, self).__init__(*args, **kwargs)
        states = db.session.scalars(sa.select(State).order_by(State.name)).all()
        self.state.choices = [(state.id, state.id) for state in states]

class DrinkerSearchForm(FlaskForm):
    search_term = StringField(
        'search_term', validators=[DataRequired()]
    )

    def __init__(self, *args, **kwargs):
      if 'formdata' not in kwargs:
        kwargs['formdata'] = request.args
      if 'meta' not in kwargs:
        kwargs['meta'] = {'csrf': False}
      super(DrinkerSearchForm, self).__init__(*args, **kwargs)
