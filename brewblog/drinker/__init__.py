from flask import Blueprint

bp = Blueprint('drinker', __name__)

from brewblog.drinker import routes, forms