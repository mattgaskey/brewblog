import sqlalchemy as sa
import sqlalchemy.orm as so
from brewblog import create_app, db
from brewblog.models import Brewery, Beer, Drinker

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'sa': sa, 'so': so, 'Brewery': Brewery, 'Beer': Beer, 'Drinker': Drinker}