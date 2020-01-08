from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
Base = declarative_base()

class Users(Base):
   __tablename__ = 'users'
   id = Column(Integer, primary_key=True)
   username = Column(String)
   password = Column(String)
   email= Column(String)
   is_admin = Column(Integer)
db = input("Enter database name to be created: ")
engine = create_engine('sqlite:///' + db + '.db', echo = True)
meta = MetaData() # Describe User Table
usersTable = Table(
   'users', meta,
   Column('id', Integer, primary_key = True),
   Column('username', String),
   Column('password', String),
   Column('email', String),
   Column('is_admin', Integer),
)

meta.create_all(engine)
print("Database " + db + " successfully created and users table inserted successfully.")

