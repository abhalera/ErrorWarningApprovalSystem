#!/usr/bin/env python3
import re
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
Base = declarative_base()

dbName = input("Enter database name to be created: ")
if(not(bool(re.search('\.db$', dbName)))):
    dbName = dbName + '.db'
engine = create_engine('sqlite:///' + dbName, echo = True)
meta = MetaData() # Describe User Table

# Describe Buckets Table
bucketsTable = Table(
   'buckets', meta,
   Column('id', Integer, primary_key = True, autoincrement = True),
   Column('name', String),
   Column('status', String),
   Column('owner', String),
)
meta.create_all(engine)
print("Database " + dbName + " successfully created and buckets table inserted successfully.")

