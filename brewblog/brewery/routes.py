from flask import render_template, flash, redirect, url_for
import sqlalchemy as sa
from brewblog import db
from brewblog.brewery import bp
from brewblog.brewery.forms import BrewerySearchForm
from brewblog.models import Brewery, City


@bp.route('/breweries')
def breweries():
  form = BrewerySearchForm()
  query = sa.select(City).order_by(City.state_id, City.name)
  locations = db.session.scalars(query).all()
  data = []
  for location in locations:
    if db.session.scalar(sa.select(Brewery).where(Brewery.city_id == location.id)):
      data.append({
          "city": location.name,
          "state": location.state_id,
          "breweries": db.session.scalars(
             sa.select(Brewery).where(Brewery.city_id == location.id).order_by(Brewery.name)).all()
      })
 
  return render_template(
    'pages/breweries.html', 
    areas=data,
    form=form,
    placeholder='Search for a Brewery',
    endpoint='/breweries/search')

@bp.route('/breweries/search', methods=['GET'])
def search_breweries():
  form = BrewerySearchForm()
  if not form.validate():
     return redirect(url_for('brewery.breweries'))
  breweries, total = Brewery.search(form.search_term.data)
  response={
    "count": total,
    "data": breweries
  }
  return render_template(
    'pages/search_breweries.html', 
    results=response, 
    search_term=form.search_term.data,
    form=form,
    placeholder='Search for a Brewery',
    endpoint='/breweries/search')

@bp.route('/breweries/<int:brewery_id>')
def show_brewery(brewery_id):
  query = sa.select(Brewery).where(Brewery.id == brewery_id)
  brewery = db.session.scalar(query)
  if brewery is None:
      flash(f'Brewery with id {brewery_id} not found.')
      return redirect(url_for('main.index'))
  
  brewery = brewery.serialize()
 
  return render_template('pages/show_brewery.html', brewery=brewery)
