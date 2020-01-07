'''
Created on Jan 2, 2020
@author: amitvinx
@file  : SessionManager.py
'''

import os
import re
import pprint
import getpass
import time 
from pathlib import Path

from Logger import *
from UsersManager import *
SESSION_TIMEOUT = 60
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

class SessionManager(metaclass=Singleton):
    '''
    SessionManager
    '''

    # Constructor
    def __init__(self):
        Debug("SessionManager Constructor called...")
        self._user = getpass.getuser()
        self._userManager = UsersManager()
        if(not os.path.isdir(os.environ['EWAS_ROOT'] + '/.sessions/')):
            try:
                os.mkdir(os.environ['EWAS_ROOT'] + '/.sessions/')
            except:
                Critical("Error while constructing sessions manager. Please contact EWAS Administratrator...")
        self._fileSession = os.environ['EWAS_ROOT'] + '/.sessions/.' + self._user
        self._isAdmin = self._userManager.IsAdmin(self._user)
        if(not self.IsSessionActive()):
            Info("Your session is not active. You need to login again. Please enter username and password to login...")
            if(self._userManager.Login()):
                self.ActivateSession()

    def IsAdmin(self):
        return self._isAdmin

    def ActivateSession(self):
        Debug("Activating session...")
        Debug("Touching file " + self._fileSession)
        Path(self._fileSession).touch()

    def IsSessionActive(self):
        Debug("Checking if the session is still active...")
        if(not os.path.isfile(self._fileSession)):
            Debug("Sessions file " + self._fileSession + " is not present...")
            return False
        lstUpdTimeFrmEpoch =  int(os.path.getmtime(self._fileSession))
        crrntTimeFrmEpoch  =  int(time.time())
        diffInSeconds = crrntTimeFrmEpoch - lstUpdTimeFrmEpoch
        Debug("File         = " + self._fileSession)
        Debug("Update       = " + str(lstUpdTimeFrmEpoch))
        Debug("Current Time = " + str(crrntTimeFrmEpoch))
        if(diffInSeconds > SESSION_TIMEOUT):
            os.remove(self._fileSession)
            Debug("Session has become stale. Delete the sessions file...")
            return False
        else:
            Debug("Session is active...")
            self.ActivateSession()
            return True
