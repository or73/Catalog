from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
"""
Bind the engine to the metadata of the Base class so that the
    declaratives can be accessed through a DBSession instance
"""
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

"""
A DBSession() instance establishes all conversations with the database
    and represents a 'staging zone' for all the objects loaded into the
    database session object. Any change made against the objects in the
    session won't be persisted into the database until you call
    session.commit(). If you're not happy about the changes, you can
    revert all of them back to the last commit by calling session.rollback()
"""
session = DBSession()

# ---------------- Creating dummy Categories
print('Created dummy Categories')
Category1 = Category(name='Cat1', description='Cat1 description')
Category2 = Category(name='Cat2', description='Cat2 description')
Category3 = Category(name='Cat3', description='Cat3 description')

print('Adding dummy categories...')
session.add(Category1)
session.add(Category2)
session.add(Category3)

# session.commit()
print('Categories stored in DB')

# ---------------- Creating dummy Items
print('Creating dummy items...')
Item1 = Item(name='Item1', description='Item1 description', price='111')
Item2 = Item(name='Item2', description='Item2 description', price='222')
Item3 = Item(name='Item3', description='Item3 description', price='333')
Item4 = Item(name='Item4', description='Item4 description', price='444')
Item5 = Item(name='Item5', description='Item5 description', price='555')
Item6 = Item(name='Item6', description='Item6 description', price='666')
Item7 = Item(name='Item7', description='Item7 description', price='777')

print('Adding dummy Items...')
session.add(Item1)
session.add(Item2)
session.add(Item3)
session.add(Item4)
session.add(Item5)
session.add(Item6)
session.add(Item7)

session.commit()
print('Items stored in DB')


# ---------------- Creating dummy users
print('Creating dummy users...')
User1 = User(username='user1', email='user1@email.com', password='user1pwd', picture='user1 some picture path', profile=1)

User2 = User(username='user2', email='user2@email.com', password='user2pwd', picture='user2 some picture path', profile=0)

User3 = User(username='user3', email='user3@email.com', password='user3pwd', picture='user3 some picture path', profile=0)
print('Adding dummy users...')
session.add(User1)
session.add(User2)
session.add(User3)

session.commit()
print('Users stored in DB')


# ---------------- Generating Associations

# Category1 Items
Category1.users.append(User1)   # Associate User1 with Category1
Category1.items.append(Item1)   # Associate Item1 with Category1
Category1.items.append(Item4)   # Associate Item4 with Category1
Category1.items.append(Item7)   # Associate Item7 with Category1
Category1.items.append(Item3)   # Associate Item3 with Category1

# Category2 Items
Category2.users.append(User2)   # Associate User2 with Category2
Category2.items.append(Item2)   # Associate Item2 with Category2
Category2.items.append(Item5)   # Associate Item5 with Category2
Category2.items.append(Item7)   # Associate Item7 with Category2

# Category3 Items
Category3.users.append(User3)   # Associate User3 with Category3
Category3.items.append(Item3)   # Associate Item3 with Category3
Category3.items.append(Item6)   # Associate Item6 with Category3


session.commit()
