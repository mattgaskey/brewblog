from flask import Blueprint

bp = Blueprint('brewery', __name__)

from brewblog.brewery import routes, forms