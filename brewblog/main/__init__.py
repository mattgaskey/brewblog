from flask import Blueprint

bp = Blueprint('main', __name__)

from brewblog.main import routes