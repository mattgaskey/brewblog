from flask import render_template, request, flash, redirect, url_for, current_app, g
import sqlalchemy as sa
from brewblog import db
from brewblog.drinker import bp
from brewblog.drinker.forms import DrinkerForm, DrinkerSearchForm
from brewblog.models import Drinker, City

@bp.route('/drinkers')
def drinkers():
  form = DrinkerSearchForm()
  query = sa.Select(Drinker).order_by(Drinker.name)
  drinkers = db.session.scalars(query).all()
  data = []
  for drinker in drinkers:
    data.append({
        "id": drinker.id,
        "name": drinker.name,
    })
  return render_template(
     'pages/drinkers.html', 
     drinkers=data, 
     form=form, 
     placeholder='Search for an Drinker',
     endpoint='/drinkers/search')

@bp.route('/drinkers/search', methods=['GET'])
def search_drinkers():
  form = DrinkerSearchForm()
  if not form.validate():
     return redirect(url_for('drinker.drinkers'))
  drinkers, total = Drinker.search(form.search_term.data)
  response={
    "count": total,
    "data": drinkers
  }
  return render_template(
    'pages/search_drinkers.html', 
    results=response, 
    search_term=form.search_term.data,
    form=form, 
    placeholder='Search for an Drinker', 
    endpoint='/drinkers/search')

@bp.route('/drinkers/<int:drinker_id>')
def show_drinker(drinker_id):
  query = sa.select(Drinker).where(Drinker.id == drinker_id)
  drinker = db.session.scalar(query)
  if not drinker:
    flash('Drinker not found.')
    return redirect(url_for('main.index'))
  drinker = drinker.serialize()
  
  return render_template('pages/show_drinker.html', drinker=drinker)

@bp.route('/drinkers/<int:drinker_id>/edit', methods=['GET'])
def edit_drinker(drinker_id):
  form = DrinkerForm()
  drinker = db.session.scalar(sa.select(Drinker).where(Drinker.id == drinker_id))
  form.name.data = drinker.name
  form.city.data = drinker.city
  form.state.data = drinker.state
  form.phone.data = drinker.phone
  form.image_link.data = drinker.image_link
  form.facebook_link.data = drinker.facebook_link
  form.website_link.data = drinker.website_link
  form.seeking_venue.data = drinker.seeking_venue
  form.seeking_description.data = drinker.seeking_description
  form.genres.data = drinker.genre_ids
  form.not_before_date.data = drinker.available_start_date
  form.not_after_date.data = drinker.available_end_date
  form.not_before_time.data = drinker.available_start_time
  form.not_after_time.data = drinker.available_end_time

  return render_template('forms/edit_drinker.html', form=form, drinker=drinker)

@bp.route('/drinkers/<int:drinker_id>/edit', methods=['POST'])
def edit_drinker_submission(drinker_id):
  form = DrinkerForm()
  drinker = db.session.scalar(sa.select(Drinker).where(Drinker.id == drinker_id))

  if form.validate_on_submit():
      try:
          city_name = form.city.data
          state_id = form.state.data
          city = db.session.scalar(sa.select(City).where(City.name == city_name, City.state_id == state_id))
          if not city:
              city = City(name=city_name, state_id=state_id)
              db.session.add(city)
              db.session.commit()
          drinker.city_ref = city
          drinker.name = form.name.data
          drinker.phone = form.phone.data
          drinker.image_link = form.image_link.data
          drinker.facebook_link = form.facebook_link.data
          drinker.website_link = form.website_link.data
          drinker.seeking_venue = form.seeking_venue.data
          drinker.seeking_description = form.seeking_description.data
          drinker.available_start_date = form.not_before_date.data
          drinker.available_end_date = form.not_after_date.data
          drinker.available_start_time = form.not_before_time.data
          drinker.available_end_time = form.not_after_time.data
          drinker.clear_genres()

          for genre_id in form.genres.data:
              genre = db.session.scalar(sa.select(Genre).where(Genre.id == int(genre_id)))
              drinker.add_genre(genre)
          db.session.commit()
          flash('Drinker ' + request.form['name'] + ' was successfully updated!')
          current_app.logger.info(f"Drinker {drinker.name} successfully updated.")
      except Exception as e:
          db.session.rollback()
          flash('An error occurred. Drinker ' + request.form['name'] + ' could not be updated.')
          current_app.logger.error(f"Error occurred while updating drinker: {e}")
      finally:
          db.session.close()
  else:
      flash('An error occurred. Drinker ' + request.form['name'] + ' could not be updated due to validation errors.')
      return render_template('forms/edit_drinker.html', form=form, drinker=drinker)

  return redirect(url_for('drinker.show_drinker', drinker_id=drinker_id))

@bp.route('/drinkers/create', methods=['GET'])
def create_drinker_form():
  form = DrinkerForm()
  return render_template('forms/new_drinker.html', form=form)

@bp.route('/drinkers/create', methods=['POST'])
def create_drinker_submission():
  form = DrinkerForm(request.form)
  if form.validate_on_submit():
      try:
          city_name = form.city.data
          state_id = form.state.data
          city = db.session.scalar(sa.select(City).where(City.name == city_name, City.state_id == state_id))
          if not city:
              city = City(name=city_name, state_id=state_id)
              db.session.add(city)
              db.session.commit()
          new_drinker = Drinker(
              name=form.name.data,
              city_ref=city,
              phone=form.phone.data,
              image_link=form.image_link.data,
              facebook_link=form.facebook_link.data,
              website_link=form.website_link.data,
              seeking_venue=form.seeking_venue.data,
              seeking_description=form.seeking_description.data,
              available_start_date=form.not_before_date.data,
              available_end_date=form.not_after_date.data,
              available_start_time=form.not_before_time.data,
              available_end_time=form.not_after_time.data
          )
          db.session.add(new_drinker)
          db.session.flush()

          for genre_id in form.genres.data:
              genre = db.session.scalar(sa.select(Genre).where(Genre.id == int(genre_id)))
              new_drinker.add_genre(genre)
          db.session.commit()
          flash('Drinker ' + request.form['name'] + ' was successfully listed!')
          current_app.logger.info(f"Drinker {new_drinker.name} successfully created.")
      except Exception as e:
          db.session.rollback()
          flash(f'An error occurred. Drinker ' + request.form['name'] + ' could not be listed.')
          current_app.logger.error(f"Error occurred while creating drinker: {e}")
      finally:
          db.session.close()
          drinker_id = new_drinker.id
  else:
      flash('An error occurred. Drinker ' + request.form['name'] + ' could not be listed due to validation errors.')
      return render_template('forms/new_drinker.html', form=form)
  if drinker_id:
    return redirect(url_for('drinker.show_drinker', drinker_id=drinker_id))
  else:
    return redirect(url_for('main.index'))

@bp.route('/drinkers/<drinker_id>/delete', methods=['POST'])
def delete_drinker(drinker_id):
  if request.form.get('_method') == 'DELETE':
    drinker = db.session.scalar(sa.select(Drinker).where(Drinker.id == drinker_id))
    try:
      db.session.delete(drinker)
      db.session.commit()
      flash('Drinker ' + drinker.name + ' was successfully deleted!')
      current_app.logger.info(f"Drinker {drinker.name} successfully deleted.")
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Drinker ' + drinker.name + ' could not be deleted.')
      current_app.logger.error(f"Error occurred while deleting drinker: {e}")
    finally:
      db.session.close()
    return redirect(url_for('main.index'))
