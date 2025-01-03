from typing import List
import sqlalchemy as sa
import sqlalchemy.orm as so
from brewblog import db
from brewblog.search import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
  @classmethod
  def get_searchable_fields(cls):
    return getattr(cls, '__searchable__', [])
  
  @classmethod
  def search(cls, expression):
    ids, total = query_index(cls.__tablename__.lower(), expression)
    if total == 0:
      return {}, 0
    when = []
    for i in range(len(ids)):
      when.append((ids[i], i))
    query = sa.select(cls).where(cls.id.in_(ids)).order_by(
      db.case(*when, value=cls.id))
    return db.session.scalars(query), total
  
  @classmethod
  def before_commit(cls, session):
    session._changes = {
      'add': list(session.new),
      'update': list(session.dirty),
      'delete': list(session.deleted)
    }

  @classmethod
  def after_commit(cls, session):
    for obj in session._changes['add']:
      if isinstance(obj, SearchableMixin):
        add_to_index(obj.__tablename__.lower(), obj)
    for obj in session._changes['update']:
      if isinstance(obj, SearchableMixin):
        add_to_index(obj.__tablename__.lower(), obj)
    for obj in session._changes['delete']:
      if isinstance(obj, SearchableMixin):
        remove_from_index(obj.__tablename__.lower(), obj)
    session._changes = None

  @classmethod
  def reindex(cls):
    for obj in db.session.scalars(sa.select(cls)):
      add_to_index(cls.__tablename__.lower(), obj)
  
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class Brewery(SearchableMixin, db.Model):
    __tablename__ = 'Brewery'
    __searchable__ = ['name']

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(120))
    phone: so.Mapped[str] = so.mapped_column(sa.String(120))
    website_link: so.Mapped[str] = so.mapped_column(sa.String(120))
    city_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('City.id'))
    city_ref: so.Mapped['City'] = so.relationship('City', back_populates='breweries')
    beers: so.Mapped[List['Beer']] = so.relationship('Beer', back_populates='brewery')
    
    @property
    def city(self):
      return self.city_ref.name
    
    @property
    def state(self):
      return self.city_ref.state_id

    def __repr__(self) -> str:
      return f'<Brewery {self.name}>'
    
    def add_beer(self, beer):
      self.beers.append(beer)
    
    def get_beers(self):
      return list(db.session.scalars(sa.select(Beer).filter(Beer.brewery_id == self.id)))

    def get_beers_count(self):
      return len(self.get_beers())
    
    def serialize(self):
      return {
        "id": self.id,
        "name": self.name,
        "address": self.address,
        "city": self.city,
        "state": self.state,
        "phone": self.phone,
        "website_link": self.website_link,
        "beers": [{
            "beer_id": beer.id,
            "beer_name": beer.name,
            "beer_style": beer.style,
            "beer_description": beer.description,
        } for beer in self.get_beers()],
        "beers_count": self.get_beers_count()
    }

class Beer(SearchableMixin, db.Model):
    __tablename__ = 'Beer'
    __searchable__ = ['name']

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(500))
    brewery_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Brewery.id'))
    style: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Style.id'))
    
    brewery: so.Mapped['Brewery'] = so.relationship('Brewery', back_populates='beers')

    def __repr__(self) -> str:
      return f'<Beer {self.name}>'

    def serialize(self):
      return {
        "id": self.id,
        "name": self.name,
        "style": self.style,
        "description": self.description
      }

class Drinker(db.Model):
    __tablename__ = 'Drinker'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    city_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('City.id'))
    
    def __repr__(self) -> str:
      return f'<Drinker {self.id}>'
    
    def serialize(self):
      return {
        "id": self.id,
        "name": self.name,
        "city": self.city_id
      }

class State(db.Model):
    __tablename__ = 'State'

    id: so.Mapped[str] = so.mapped_column(sa.String(2), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    
    cities: so.WriteOnlyMapped['City'] = so.relationship(
        back_populates='state', passive_deletes=True)
    
    def __repr__(self) -> str:
      return f'<State {self.id}>'

class City(db.Model):
    __tablename__ = 'City'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    state_id: so.Mapped[str] = so.mapped_column(sa.String(2), sa.ForeignKey('State.id'))
    
    state: so.Mapped['State'] = so.relationship('State', back_populates='cities')
    breweries: so.WriteOnlyMapped['Brewery'] = so.relationship('Brewery', back_populates='city_ref')

    def __repr__(self) -> str:
      return f'<City {self.name}, {self.state_id}>'
    
class Style(db.Model):
    __tablename__ = 'Style'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    
    def __repr__(self) -> str:
      return f'<Style {self.name}>'
