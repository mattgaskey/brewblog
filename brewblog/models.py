from typing import List
import sqlalchemy as sa
import sqlalchemy.orm as so
from brewblog import db

class Brewery(db.Model):
    __tablename__ = 'Brewery'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(120))
    phone: so.Mapped[str] = so.mapped_column(sa.String(120))
    website_link: so.Mapped[str] = so.mapped_column(sa.String(120))
    city: so.Mapped[str] = so.mapped_column(sa.String(120))
    state: so.Mapped[str] = so.mapped_column(sa.String(120))

    beers: so.Mapped[List['Beer']] = so.relationship('Beer', back_populates='brewery')

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

class Beer(db.Model):
    __tablename__ = 'Beer'

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
    
    def __repr__(self) -> str:
      return f'<Drinker {self.id}>'
    
    def serialize(self):
      return {
        "id": self.id,
        "name": self.name
      }
    
class Style(db.Model):
    __tablename__ = 'Style'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    
    def __repr__(self) -> str:
      return f'<Style {self.name}>'
