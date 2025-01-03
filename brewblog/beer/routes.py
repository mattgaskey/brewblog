from flask import render_template, flash, redirect, url_for, current_app
import sqlalchemy as sa
from datetime import time
from brewblog import db
from brewblog.beer import bp
from brewblog.beer.forms import BeerForm
from brewblog.models import Brewery, Beer, Drinker

@bp.route('/beers')
def beers():
  query = db.session.scalars(sa.Select(Beer).join(Brewery).join(Drinker).order_by(Beer.name))
  data = []
  for beer in query:
    data.append({
      "brewery_id": beer.brewery_id,
      "brewery_name": beer.brewery.name,
      "drinker_id": beer.drinker_id,
      "drinker_name": beer.drinker.name,
    })
  return render_template('pages/beers.html', beers=data)

# @bp.route('/shows/create')
# def create_shows():
#   form = ShowForm()
#   return render_template('forms/new_show.html', form=form)

# @bp.route('/shows/create', methods=['POST'])
# def create_show_submission():
#   form = ShowForm()
#   if form.validate_on_submit():
#     try:
#       artist = db.session.scalar(sa.select(Artist).where(Artist.id == form.artist_id.data))
#       start_time = form.start_time.data

#       start_date = start_time.date()
#       start_time_only = start_time.time()

#       if artist.available_end_time == time(0, 0, 0):
#         artist_end_time = time(23, 59, 59)
#       else:
#         artist_end_time = artist.available_end_time

#       if (artist.available_start_date and start_date < artist.available_start_date) or \
#          (artist.available_end_date and start_date > artist.available_end_date) or \
#          (artist.available_start_time and start_time_only < artist.available_start_time) or \
#          (artist_end_time and start_time_only > artist_end_time):
#         flash(f'An error occurred. Show time is outside the artist\'s availability. Please check the artist\'s availability <a href="{url_for("artist.show_artist", artist_id=artist.id)}">here</a>.')
#         return redirect(url_for('show.create_shows'))
      
#       show = Show(
#         artist_id=form.artist_id.data,
#         venue_id=form.venue_id.data,
#         start_time=start_time
#       )
#       db.session.add(show)
#       db.session.commit()
#       flash('Show was successfully listed!')
#     except Exception as e:
#       db.session.rollback()
#       flash(f'An error occurred. Show could not be listed. {str(e)}')
#       current_app.logger.error(f"Error occurred while creating venue: {e}")
#     finally:
#       db.session.close()
#   else:
#     flash('An error occurred. Show could not be updated due to validation errors.')
#   return redirect(url_for('show.shows'))