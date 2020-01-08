'''
Created on Dec 2, 2019
@author: amitvinx
@file  : Logger.py
'''
import logging
from termcolor import colored
import platform

def SetupLogger(fileName="Logger.log", loggingLevel=logging.INFO):
    # Logger Setup
    rootLogger= logging.getLogger()
    rootLogger.setLevel(loggingLevel)
    handler = logging.FileHandler(fileName, 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s [%(levelname)-8.8s]  %(message)s')
    handler.setFormatter(formatter)
    rootLogger.addHandler(handler)
#    logging.basicConfig(
#        filename=fileName,
#        format="%(asctime)s [%(levelname)-8.8s]  %(message)s",
#        datefmt='%Y-%m-%d %H:%M:%S',
#        level=loggingLevel,
#        filemode='w'
#        )
    # Print to STDOUT also
    # rootLogger.addHandler(logging.StreamHandler())

def Info(message=None):
    if(message != None):
        logging.info(message)
        if(platform.system() == 'Windows'):
            print("[INFO]: " + message)
        else:
            print(colored("[INFO]: ", attrs=['bold']) + message)

def Print(message=None):
    if(message != None):
        print(str(message))
        logging.info(str(message))

def Log(message=None):
    if(message != None):
        logging.info(str(message))

def Warn(message=None):
    if(message != None):
        logging.warning(str(message))
        if(platform.system() == 'Windows'):
            print("[WARN]: " + message)
        else:
            print(colored("[WARN]: ", 'yellow', attrs=['bold']) + message)

def Error(message=None):
    if(message != None):
        logging.error(message)
        if(platform.system() == 'Windows'):
            print("[ERROR]: "+ message)
        else:
            print(colored("[ERROR]: ", 'red', attrs=['bold']) + colored(message, 'red'))

def Critical(message=None):
    if(message != None):
        logging.critical(str(message))
        if(platform.system() == 'Windows'):
            print("[CRITICAL]: "+ message)
        else:
            print(colored("[CRITICAL]: ", 'red', attrs=['bold']) + colored(message, 'red'))
        exit(1)

def Debug(message=None):
    if(message != None):
        logging.debug(str(message))
