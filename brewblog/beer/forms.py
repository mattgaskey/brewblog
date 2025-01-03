from flask_login import current_user
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
import sqlalchemy as sa
from brewblog import db
from brewblog.models import Beer, Brewery, Style

class BeerForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    description = StringField(
        'description', validators=[DataRequired()]
    )
    brewery_id = SelectField(
        'brewery_id', validators=[DataRequired()],
        choices=[]
    )
    style_id = SelectField(
        'style_id', validators=[DataRequired()],
        choices=[]
    )

    def __init__(self, *args, **kwargs):
        super(BeerForm, self).__init__(*args, **kwargs)
        breweries = db.session.scalars(sa.select(Brewery).order_by(Brewery.name)).all()
        self.brewery_id.choices = [(brewery.id, brewery.name) for brewery in breweries] if breweries else [('', 'No brewery available')]
        styles = db.session.scalars(sa.select(Style).order_by(Style.name)).all()
        self.style_id.choices = [(style.id, style.name) for style in styles] if styles else [('', 'No style available')]

    def create_beer(self):
        beer = Beer(
            name=self.name.data,
            description=self.description.data,
            brewery_id=self.brewery_id.data,
            style_id=self.style_id.data,
            drinker_id=current_user.id
        )
        db.session.add(beer)
        db.session.commit()
        return beer