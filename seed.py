from brewblog import create_app, db
from brewblog.models import Style

def seed_styles():
  styles = [
    'Pale Ale',
    'IPA',
    'Wheat',
    'Amber',
    'Red',
    'Porter',
    'Stout',
    'Sour',
    'Pilsner'
  ]
  if not Style.query.first():
    for name in styles:
      new_style = Style(name=name)
      db.session.add(new_style)
  
  db.session.commit()

if __name__ == '__main__':
  app = create_app()
  with app.app_context():
    seed_styles()
