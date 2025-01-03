from flask import render_template, request, flash, redirect, url_for, current_app
import sqlalchemy as sa
from brewblog import db
from brewblog.drinker import bp
from brewblog.drinker.forms import DrinkerForm
from brewblog.models import Drinker

@bp.route('/drinkers')
def drinkers():
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
     drinkers=data)

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

  return render_template('forms/edit_drinker.html', form=form, drinker=drinker)

@bp.route('/drinkers/<int:drinker_id>/edit', methods=['POST'])
def edit_drinker_submission(drinker_id):
  form = DrinkerForm()
  drinker = db.session.scalar(sa.select(Drinker).where(Drinker.id == drinker_id))

  if form.validate_on_submit():
      try:
          drinker.name = form.name.data

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
          new_drinker = Drinker(
              name=form.name.data
          )
          db.session.add(new_drinker)
          db.session.flush()

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
