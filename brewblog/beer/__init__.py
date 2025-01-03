from flask import Blueprint

bp = Blueprint('beer', __name__)

from brewblog.beer import forms