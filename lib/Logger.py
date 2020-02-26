'''
Created on Dec 2, 2019
@author: amitvinx
@file  : Logger.py
'''
import logging
from termcolor import cprint, colored
import platform
if(platform.system() == 'Windows'):
    from colorama import init
    init()

def SetupLogger(fileName="Logger.log", loggingLevel=logging.INFO):
    '''
    Name    : SetupLogger
    Args    :
              fileName = <Name of the log file>
              loggingLevel = <logging.INFO/logging.DEBUG>
    Returns : None
    Purpose : This function should be called before using any of the other functions from this module.
              It sets up the log file and the logging level
    '''
    # Logger Setup
    rootLogger= logging.getLogger()
    rootLogger.setLevel(loggingLevel)
    handler = logging.FileHandler(fileName, 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s [%(levelname)-8.8s]  %(message)s')
    handler.setFormatter(formatter)
    rootLogger.addHandler(handler)

def Info(message=None):
    '''
    Name    : Info
    Args    :
              message = <Message to be printed and/or logged.>
    Returns : None
    Purpose : Print INFO using system color and bold face on STDOUT and log file
    '''
    if(message != None):
        logging.info(message)
        cprint("[INFO]: " + message, attrs=["bold"])

def Print(message=None):
    '''
    Name    : Print
    Args    :
              message = <Message to be printed and/or logged.>
    Returns : None
    Purpose : Simply print message without any formatting/coloring on STDOUT and log file
    '''
    if(message != None):
        print(str(message))
        logging.info(str(message))

def Log(message=None):
    '''
    Name    : Log
    Args    :
              message = <Message to be printed and/or logged.>
    Returns : None
    Purpose : Log message without any formatting/coloring to the log file
    '''
    if(message != None):
        logging.info(str(message))

def Warn(message=None):
    '''
    Name    : Warn
    Args    :
              message = <Message to be printed and/or logged.>
    Returns : None
    Purpose : Print WARNING using yellow color and bold face on STDOUT and log file
    '''
    if(message != None):
        logging.warning(str(message))
        cprint("[WARN]: "+ message, 'yellow', attrs=["bold"])

def Error(message=None):
    '''
    Name    : Error
    Args    :
              message = <Message to be printed and/or logged.>
    Returns : None
    Purpose : Print ERROR using red color on STDOUT and log file
    '''
    if(message != None):
        logging.error(message)
        cprint("[ERROR]: "+ message,'red')

def Critical(message=None):
    '''
    Name    : Critical
    Args    :
              message = <Message to be printed and/or logged.>
    Returns : None
    Purpose : Print CRITICAL message using red color and bold face on STDOUT and log file
              The program terminates if a CRITICAL is encountered
    '''
    if(message != None):
        logging.critical(str(message))
        cprint("[CRITICAL]: "+ message, 'red', attrs=["bold"])
        exit(1)

def Debug(message=None):
    '''
    Name    : Critical
    Args    :
              message = <Message to be printed and/or logged.>
    Returns : None
    Purpose : Debug message without any formatting/coloring to the log file
    '''
    if(message != None):
        logging.debug(str(message))
