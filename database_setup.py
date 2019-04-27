from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy import create_engine

import datetime

Base = declarative_base()

# -------------- Many-to-May Relationship tables --------------
""" 
Many to Many Relationship adds an association table between two classes. The association 
    table is indicated by the secondary argument to relationship(). Usually, the Table 
    uses the MetaData object associated with the declarative base class, so that the 
    ForeignKey directives can locate the remote tables with which to link.
For a bidirectional relationship, both sides of the relationship contain a collection. 
    Specify using relationship.back_populates, and for each relationship() specify the 
    common association table.
Child will get a parent attribute with many-to-one semantics.
Alternatively, the 'backref' option may be used on a single relationship() instead of 
    using 'back_populates'
"""
item_category = Table('item_category', Base.metadata,
                      Column('category_id', Integer, ForeignKey('category.id')),
                      Column('item_id', Integer, ForeignKey('item.id')))
user_category = Table('user_category', Base.metadata,
                      Column('user_id', Integer, ForeignKey('user.id')),
                      Column('category_id', Integer, ForeignKey('category.id')))


# -------------- Tables Declaration  --------------
class Category(Base):
    """
    Category table
    """
    __tablename__ = 'category'

    id = Column(Integer, Sequence('user_id_sequence'), primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    items = relationship('Item', secondary=item_category, backref=backref('items_category', lazy='dynamic'))
    users = relationship('User', secondary=user_category, backref=backref('users_category', lazy='dynamic'))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created': self.created
        }


class Item(Base):
    """
    Item table
    """
    __tablename__ = 'item'

    id = Column(Integer, Sequence('user_id_sequence'), primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    # categories = relationship('Category', secondary=item_category, backref=backref('items', lazy='dynamic'))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'created': self.created
        }


class User(Base):
    """
    User table
    Firebird and Oracle require sequences to generate new primary key identifiers,
       and SQLAlchemy does not generate or assume these without being instructed.
       For that, you use the Sequence construct
    profile --> Boolean --> 0: user   1: Admin
    """
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    profile = Column(Boolean, nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    # categories = relationship('Category', secondary=user_category, backref=backref('category_users', lazy='dynamic'))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'profile': self.profile,
            'created': self.created
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
