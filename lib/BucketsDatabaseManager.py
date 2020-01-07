'''
Created on Jan 2, 2020
@author: amitvinx
@file  : BucketsDatabaseManager.py
'''

import os
import re
import pprint
import sqlalchemy

from Logger import *
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean
from sqlalchemy import create_engine


class BucketsDatabaseManager(object):
    '''
    BucketsDatabaseManager
    '''

    # Constructor
    def __init__(self):
        Debug("BucketsDatabaseManager Constructor called...")

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
        usersTable = Table(
           'users', meta,
           Column('id', Integer, primary_key = True),
           Column('name', String),
           Column('email', String),
           Column('unix_id', String),
           Column('unix_id', String),
           Column('is_admin', Boolean),
           Column('password', String),
        )

        # Describe Buckets Table
        bucketsTable = Table(
           'buckets', meta,
           Column('id', Integer, primary_key = True),
           Column('name', String),
           Column('status', String),
           Column('owner', Integer),
        )
        meta.create_all(engine)
        Debug("Database " + dbName + " successfully created and tables users and buckets inserted successfully.")





