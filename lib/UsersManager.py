'''
Created on Jan 2, 2020
@author: amitvinx
@file  : UsersManager.py
'''

import os
import re
import pprint
import sqlalchemy

from Logger import *
from SettingsManager import *
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

class UsersManager(metaclass=Singleton):
    '''
    UsersManager
    '''

    # Constructor
    def __init__(self):
        Debug("UsersManager Constructor called...")
        # dbName = os.environ['EWAS_ROOT'] + '/db/users.db'
        dbName = SettingsManager().Get_Default_Database()
        if(not dbName):
            Critical("No database selected as of now. Please use select_database command to select current database")
        self._engine = create_engine('sqlite:///' + dbName, echo = False)
        self._session = sessionmaker(bind = self._engine)()

    def Add_User(self, username=None, password=None, email=None, is_admin=0):
        '''
        Add a new user
        '''
        if(username == None):
            Critical("Please specify a valid username. Exiting...")
        if(password == None):
            Critical("Please specify a valid password. Exiting...")
        if(email == None):
            Critical("Please specify a valid password. Exiting...")
        if(is_admin == None):
            Critical("Please specify a valid is_admin. Exiting...")
        try:
            self._session.add(Users(username=username, password=password, email=email, is_admin=is_admin))
            return self._session.commit()
        except SQLAlchemyError as e:
            Error("UsersManager ERROR occured. " + str(e))
            self._session.rollback()
            return 1

    def Remove_User(self, username=None):
        '''
        Remove a new user
        '''
        if(username == None):
            Critical("Please specify a valid username. Exiting...")
        try:
            self._session.delete(self._session.query(Users).filter(Users.username==username).one())
            return self._session.commit()
        except SQLAlchemyError as e:
            Error("UsersManager ERROR occured. " + str(e))
            self._session.rollback()
            return 1
        except:
            self._session.rollback()
            return 1


    def Login(self):
        import getpass
        import hashlib
        '''
        Login
        #TODO: Make this work for both GUI and command-line
        '''
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        password = hashlib.md5(str(password).encode('utf-8')).hexdigest()

        result = self._session.query(Users).filter(Users.username == username).first()
        if(not result):
            Critical("No user found with username = " + username)
            return 0
        else:
            if (password == result.password):
                Info("User '" + username + "' successfully logged in...")
                return bool(result.is_admin > 0)
            else:
                Critical("Username and password are not matching. Please contact your EWAS Administratrator...")
                return 0

    def IsAdmin(self, user):
        username = user
        Debug("Checking if user = " + username + " is an ADMINISTRATOR...")
        result = self._session.query(Users).filter(Users.username == username).first()
        if(not result):
            Critical("No user found with username = " + user)
            return False
        else:
            if(result.is_admin > 0):
                Debug("You are an ADMINISTRATOR")
                return True
            else:
                Debug("You are an not an ADMINISTRATOR")
                return False




