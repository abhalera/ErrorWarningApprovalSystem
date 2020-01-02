'''
Created on Jan 2, 2020
@author: amitvinx
@file  : BucketsDatabaseManager.py
'''

import os
import re
import pprint

from Logger import *


class BucketsDatabaseManager(object):
    '''
    BucketsDatabaseManager 
    '''

    # Constructor
    def __init__(self):
        Print("BucketsDatabaseManager Constructor called...")

    def Create_Database(self, dbName=None):
        '''
        Create a new database
        '''
        if(dbName == None):
            Print("Please specify a valid database name. Exiting...")
            exit(1)
        else:
            Print("TODO: Write the code for creating a new database and all the exception handling...")
            Print("Creating database with name = " + dbName)
            pass
            #TODO Add the code for creating a new database and all the Exception handling

