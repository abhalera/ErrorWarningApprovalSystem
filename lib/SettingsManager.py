'''
Created on Jan 9, 2020
@author: amitvinx
@file  : SettingsManager.py
'''

import os
import re
import pprint

from Logger import *

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


class SettingsManager(metaclass=Singleton):
    '''
    SettingsManager
    '''

    # Constructor
    # Reads .catalyzer.ini file from the home directory and reads the settings
    def __init__(self, tool="EWAS"):
        self._settingsDict = {}
        self._defaultTool = tool
        Debug("SettingsManager Constructor called...")
        iniFile = os.environ['HOME'] + '/.catalyzer.ini'
        if(not os.path.isfile(iniFile)):
            Warn("Could not find ~/.catalyzer.ini file. Please create one to store default settings...")

        import configparser
        Debug("Parsing ~/catalyzer.ini file = ")
        self._config = configparser.ConfigParser()
        self._config.read(iniFile)

    # Get Default Database
    def Get_Default_Database(self):
        return self._config[self._defaultTool]['default_database']

    # Get Databases List
    def Get_Databases_List(self):
        return map(str.strip, self._config[self._defaultTool]['databases'].split(','))

    # Get Database
    def Get_Database(self, number):
        databases = self._config[self._defaultTool]['databases'].split(',')
        return databases[number].strip()

    # Get Search Config Files List
    def Get_Search_Config_Files_List(self):
        return list(map(str.strip, self._config[self._defaultTool]['search_config_files'].split(',')))

    # Get Bucket Config Files List
    def Get_Bucket_Config_Files_List(self):
        return list(map(str.strip, self._config[self._defaultTool]['bucket_config_files'].split(',')))

    # Get any setting.
    def Get_Setting(self, settingName):
        if(not settingName in self._config[self._defaultTool]):
            Critical("Setting '" + settingName + "' not found in section '" + self._defaultTool + "' in file '.catalyzer.ini'")
        else:
            # TODO: Add a check of list or scalar and add map function to remove spaces
            return self._config[self._defaultTool][settingName]

