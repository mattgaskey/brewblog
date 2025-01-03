import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/db')
  ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL', 'http://search:9200')