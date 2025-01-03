from flask import Blueprint

bp = Blueprint('errors', __name__)

from brewblog.errors import handlers