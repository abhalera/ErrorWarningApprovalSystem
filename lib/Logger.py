'''
Created on Dec 2, 2019
@author: amitvinx
@file  : Logger.py
'''
import logging


def SetupLogger(fileName="Logger.log", loggingLevel=logging.INFO):
    # Logger Setup
    logging.basicConfig(
        filename=fileName,
        format="%(asctime)s [%(levelname)-8.8s]  %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        level=loggingLevel,
        filemode='w'
        )
    # Print to STDOUT also
    logging.getLogger().addHandler(logging.StreamHandler())

def Info(message=None):
    if(message != None):
        logging.info(message)

def Print(message=None):
    if(message != None):
        print(message)
        logging.info(message)

def Warn(message=None):
    if(message != None):
        logging.warning(message)

def Error(message=None):
    if(message != None):
        logging.error(message)

def Critical(message=None):
    if(message != None):
        logging.critical(message)
        exit(1)

def Debug(message=None):
    if(message != None):
        logging.debug(message)

