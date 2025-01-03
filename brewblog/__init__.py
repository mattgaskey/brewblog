from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app, db)

  from brewblog.beer import bp as beer_bp
  app.register_blueprint(beer_bp)

  from brewblog.brewery import bp as brewery_bp
  app.register_blueprint(brewery_bp)

  from brewblog.drinker import bp as drinker_bp
  app.register_blueprint(drinker_bp)

  from brewblog.errors import bp as errors_bp
  app.register_blueprint(errors_bp)

  from brewblog.main import bp as main_bp
  app.register_blueprint(main_bp)

  return app

from brewblog import models