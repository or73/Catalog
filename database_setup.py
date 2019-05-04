# --------------- Database
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy import create_engine
import datetime
# --------------- Password
from passlib.apps import custom_app_context as pwd_context
import random
import string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

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
                      Column('_category_id', Integer, ForeignKey('category._id')),
                      Column('_item_id', Integer, ForeignKey('item._id')))
user_category = Table('user_category', Base.metadata,
                      Column('_user_id', Integer, ForeignKey('user._id')),
                      Column('_category_id', Integer, ForeignKey('category._id')))


# -------------- Tables Declaration  --------------
class Category(Base):
    """
    Category table
    """
    __tablename__ = 'category'

    _id = Column(Integer, Sequence('user_id_sequence'), primary_key=True)
    name = Column(String(20), nullable=False, index=True)
    description = Column(String(250))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    items = relationship('Item', secondary=item_category, backref=backref('items_category', lazy='dynamic'))
    users = relationship('User', secondary=user_category, backref=backref('users_category', lazy='dynamic'))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            '_id': self._id,
            'name': self.name,
            'description': self.description,
            'created': self.created
        }


class Item(Base):
    """
    Item table
    """
    __tablename__ = 'item'

    _id = Column(Integer, Sequence('user_id_sequence'), primary_key=True)
    name = Column(String(20), nullable=False, index=True)
    description = Column(String(250))
    price = Column(String(10))
    created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            '_id': self._id,
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

    _id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(32), index=True)
    password = Column(String(64), nullable=False)
    picture = Column(String)
    email = Column(String, index=True)
    profile = Column(Boolean, nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            '_id': self._id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'picture': self.picture,
            'profile': self.profile,
            'created': self.created
        }

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY,
                       expires_in=expiration)
        return s.dumps({'id': self._id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)

        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid token, but expired
            return None
        except BadSignature:
            # Invalid token
            return None

        user_id = data['id']
        return user_id


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
