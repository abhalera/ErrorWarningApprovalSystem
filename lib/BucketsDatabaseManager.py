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
        Debug("BucketsDatabaseManager Constructor called...")

    def Create_Database(self, dbName=None):
        '''
        Create a new database
        '''
        if(dbName == None):
            Critical("Please specify a valid database name. Exiting...")
        else:
            Debug("TODO: Write the code for creating a new database and all the exception handling...")
            #TODO Add the code for creating a new database and all the Exception handling

