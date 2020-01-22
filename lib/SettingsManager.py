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
        self._defaultTool = tool
        Debug("SettingsManager Constructor called...")
        iniFile = os.environ['HOME'] + '/.catalyzer.ini'
        if(not os.path.isfile(iniFile)):
            Critical("Could not find .catalyzer.ini file in HOME directory. Please create one to store default settings...")

        import configparser
        Debug("Parsing ~/catalyzer.ini file = ")
        self._config = configparser.ConfigParser()
        self._config.read(iniFile)

    ################################################################################
    ############################## Global Settings #################################
    ################################################################################
    # Get Users Database
    def Get_Users_Database(self):
        try:
            return self._config['GLOBAL']['users_database']
        except:
            Critical("Could not read users_database setting from config file .catalyzer.ini ...")

    ################################################################################
    ########################### Generic APIs #######################################
    ################################################################################
    # Get any setting.
    def Get_Setting(self, settingName, sectionName=None):
        if(not sectionName):
            sectionName = self._defaultTool
        if(not settingName in self._config[sectionName]):
            Critical("Setting '" + settingName + "' not found in section '" + sectionName + "' in file '.catalyzer.ini'")
        else:
            # TODO: Add a check of list or scalar and add map function to remove spaces
            return self._config[sectionName][settingName]


    ################################################################################
    ################################ EWAS Settings #################################
    ################################################################################
    # Get Databases List
    def Get_EWAS_Databases_List(self):
        return map(str.strip, self._config[self._defaultTool]['databases'].split(','))

    # Get Database
    def Get_EWAS_Database(self, number):
        databases = self._config[self._defaultTool]['databases'].split(',')
        return databases[number].strip()

    # Get Search Config Files List
    def Get_EWAS_Search_Config_Files_List(self):
        return list(map(str.strip, self._config[self._defaultTool]['search_config_files'].split(',')))

    # Get Bucket Config Files List
    def Get_EWAS_Bucket_Config_Files_List(self):
        return list(map(str.strip, self._config[self._defaultTool]['bucket_config_files'].split(',')))

