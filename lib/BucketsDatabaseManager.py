'''
Created on Jan 2, 2020
@author: amitvinx
@file  : BucketsDatabaseManager.py
'''

import os
import re
import pprint
import sqlalchemy
import getpass
import json

from Logger import *
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Buckets(Base):
   __tablename__ = 'buckets'
   id = Column(Integer, primary_key=True)
   name   = Column(String)
   status = Column(String)
   owner  = Column(String)

class Users(Base):
   __tablename__ = 'users'
   id = Column(Integer, primary_key=True)
   username = Column(String)
   password = Column(String)
   email= Column(String)
   is_admin = Column(Integer)

class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class BucketsDatabaseManager(metaclass = Singleton):
    '''
    BucketsDatabaseManager
    '''

    # Constructor
    def __init__(self):
        Debug("BucketsDatabaseManager Constructor called...")
        self._user = getpass.getuser()
        if(not os.path.isdir(os.environ['EWAS_ROOT'] + '/.sessions/')):
            try:
                os.mkdir(os.environ['EWAS_ROOT'] + '/.sessions/')
            except:
                Critical("Error while constructing sessions manager. Please contact EWAS Administratrator...")
        self._jsonFile = os.environ['EWAS_ROOT'] + '/.sessions/.' + self._user + '_db'
        self._jsonData = {}
        self._selectedDatabase = None
        if(os.path.isfile(self._jsonFile)):
            self._Read_Database_JSON()
            self._selectedDatabase = self._jsonData['selected_database']
            self._engine = create_engine('sqlite:///' + self._selectedDatabase, echo = False)
            self._base = declarative_base()
            self._session = sessionmaker(bind = self._engine)()


    def _Read_Database_JSON(self):
        with open(self._jsonFile) as jsonFile:
            try:
                self._jsonData = json.load(jsonFile)
            except:
                Warn("Looks like " + self._jsonFile + " is empty. Ignoring...")

    def Select_Database(self, dbFile):
        self._jsonData['selected_database'] = dbFile
        with open(self._jsonFile, 'w') as jsonFile:
            try:
                json.dump(self._jsonData, jsonFile)
            except:
                Warn("Could not write to " + self._jsonFile)
        self._engine  = create_engine('sqlite:///' + dbFile, echo = False)
        self._base    = declarative_base()
        self._session = sessionmaker(bind = self._engine)()
        self._selectedDatabase = dbFile

    def Selected_Database(self):
        if('selected_database' in self._jsonData):
            return self._jsonData['selected_database']
        else:
            Warn("Nothing is selected as of now. Please use select_database command to select current database")
            return "None"

    def Get_Bucket_Information(self, bucketName):
        if(not self._selectedDatabase):
            Error("Nothing is selected as of now. Please use select_database command to select current database")
            return
        result = self._session.query(Buckets).filter(Buckets.name == bucketName).first()
        if(not result):
            return 'UNASSIGNED', 'UNASSIGNED'
        else:
            return result.status, result.owner

    def Assign_Bucket(self, bucketName, bucketOwner):
        if(not self._selectedDatabase):
            Error("Nothing is selected as of now. Please use select_database command to select current database")
            return 1
        result = self._session.query(Buckets).filter(Buckets.name == bucketName).first()
        if(not result):
            # Insert
            try:
                self._session.add(Buckets(name=bucketName, status="Open", owner=bucketOwner))
                return self._session.commit()
            except SQLAlchemyError as e:
                Error("BucketsDatabaseManager ERROR occured. " + str(e))
                self._session.rollback()
                return 1
        else:
            # Update
            try:
                result.owner = bucketOwner
                self._session.flush()
                return self._session.commit()
            except SQLAlchemyError as e:
                Error("BucketsDatabaseManager ERROR occured. " + str(e))
                self._session.rollback()
                return 1

    def Create_Database(self, dbName=None):
        '''
        Create a new database
        '''
        if(dbName == None):
            Critical("Please specify a valid database name. Exiting...")
        else:
            if(not(bool(re.search('\.db$', dbName)))):
                dbName = dbName + '.db'
            Debug("Database Name = " + dbName)
        # if(os.path.isfile(os.environ['EWAS_ROOT'] + '/db/' + dbName)):
        if(os.path.isfile(dbName)):
            Critical("Database " + dbName + ' already exists. Can not create the database with the same name. Please provide a different name...')

        engine = create_engine('sqlite:///' + dbName, echo = True)
        meta = MetaData()
        # Describe User Table
        # TODO: Later move everything to one database
        usersTable = Table(
           'users', meta,
           Column('id', Integer, primary_key = True, autoincrement = True),
           Column('username', String),
           Column('email', String),
           Column('is_admin', Integer),
           Column('password', String),
        )

        # Describe Buckets Table
        bucketsTable = Table(
           'buckets', meta,
           Column('id', Integer, primary_key = True, autoincrement = True),
           Column('name', String),
           Column('status', String),
           Column('owner', String),
        )
        meta.create_all(engine)
        Debug("Database " + dbName + " successfully created and tables users and buckets inserted successfully.")

    def Add_Bucket(self, dbName=None):
        '''
        Create a new database
        '''




