from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class Users(Base):
   __tablename__ = 'users'
   id = Column(Integer, primary_key=True)
   username = Column(String)
   password = Column(String)

class NewUsers(Base):
   __tablename__ = 'new_users'
   id = Column(Integer, primary_key=True)
   username = Column(String)
   password = Column(String)

session = sessionmaker(bind = engine)()

result = session.query(NewUsers).all()

for row in result:
    print("Id       = " + str(row.id))
    print("Username = " + row.username)
    print("Password = " + row.password)
    print("------------------------------")

print("Adding one more record")
myUser = NewUsers(username = 'TEST', password = 'TESTP')
session.add(myUser)
session.commit()

result = session.query(NewUsers).filter(NewUsers.id == 2)

print("Querying after adding abhalera")
for row in result:
    print("Id       = " + str(row.id))
    print("Username = " + row.username)
    print("Password = " + row.password)
    print("------------------------------")



