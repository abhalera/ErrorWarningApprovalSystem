'''
Created on Nov 28, 2019
@author: amitvinx
@file  : LogParser.py
'''
import os
import re
import pprint

from Logger import *

class LogParser(object):
    '''
    Single File Parser for keywords
    '''

    def __init__(self, fileName=None, signature=None):
        '''
        Constructor
        '''
        Debug("LogParser Constructor called...")

        # File checks
        if(fileName == None):
            Critical("Can not create LogParser without a valid file name. Please provide a valid file name using fileName argument...")
        if(not os.path.isfile(fileName)):
            Critical("Specified file " + fileName + " does not exist. Please provide a valid file name using fileName argument...")

        # Signature checks
        if(signature== None):
            Critical("Can not create LogParser without a valid signature. Please provide a valid signature using signature argument...")

        if(len(signature['exists']) != len(set(signature['exists']))):
            Critical("Duplicate entries found in signature['exists']. Please remove the duplicates...")

        if(len(signature['EXISTS']) != len(set(signature['EXISTS']))):
            Critical("Duplicate entries found in signature['EXISTS']. Please remove the duplicates...")

        self.fileName  = fileName
        self.signature = signature
        self._result= {}
        self._fileText = None
        self._FileToString()

    def _FileToString(self):
        textFile = open(self.fileName, 'r')
        self._fileText = textFile.read()
        textFile.close()

    def Parse(self):
        '''
        Parse the file
        '''
        Info("Parsing file " + self.fileName)
        Debug(self.signature)

        # exists Case insensitive
        self._result['exists'] = {}
        for r in self.signature['exists']:
            Debug("Trying to match ignoring case \'" + r + "\'")
            match = re.findall('(?i)'+r, self._fileText)
            Debug("Number of matches = " + str(len(match)))
            Debug("Matches:")
            for e in match:
                Debug("\t" + e)
                self._result['exists'][r] = {'count' : len(match), 'match' : match}

        # EXISTS Case sensitive
        self._result['EXISTS'] = {}
        for r in self.signature['EXISTS']:
            Debug("Trying to match case sensitive \'" + r + "\'")
            match = re.findall(r, self._fileText)
            Debug("Number of matches = " + str(len(match)))
            Debug("Matches:")
            for e in match:
                Debug("\t" + e)
                self._result['EXISTS'][r] = {'count' : len(match), 'match' : match}

        # namevalue Case insensitive
        # TODO : Fix this code for multiple matches
        self._result['namevalue'] = {}
        for r in self.signature['namevalue']:
            searchExpression = r['value']
            searchExpression = re.sub("\s+", "\\\s+", searchExpression.strip())
            Debug("Trying to match case sensitive namevalue \'" +
                  searchExpression + "\'")
            match = re.search(searchExpression, self._fileText)
            if(match):
                self._result['namevalue'][r['name']] = {'value' : match.group(1), 'match' : match}
            else:
                self._result['namevalue'][r['name']] = {'value' : None, 'match' : None}


        self._fileText = None
        Debug(self._result)

    # Returns True if pattern matched else False 
    def DidExistsMatch(self, searchExpression):
        Debug("Returning result for searchExpression = '" + searchExpression +
             "'")
        if(searchExpression in self._result['exists']):
            if(self._result['exists'][searchExpression]['count'] > 0):
                return True
            else:
                return False
        else:
            Info("Search Expression = '" + searchExpression + "' not present in signature")
            return False

    # Returns number of times the pattern matched
    def GetExistsMatchCount(self, searchExpression):
        Debug("Returning result for searchExpression = '" + searchExpression +
             "'")
        if(searchExpression in self._result['exists']):
            return self._result['exists'][searchExpression]['count']
        else:
            Info("Search Expression = '" + searchExpression + "' not present in signature")
            return -1

    # Returns list of matching lines 
    def GetExistsMatchList(self, searchExpression):
        Debug("Returning result for searchExpression = '" + searchExpression +
             "'")
        if(searchExpression in self._result['exists']):
            return self._result['exists'][searchExpression]['match']
        else:
            Info("Search Expression = '" + searchExpression + "' not present in signature")
            return None

    # Returns True if pattern matched else false 
    def DidEXISTSMatch(self, searchExpression):
        Debug("Returning result for searchExpression = '" + searchExpression +
             "'")
        if(searchExpression in self._result['EXISTS']):
            if(self._result['EXISTS'][searchExpression]['count'] > 0):
                return True
            else:
                return False
        else:
            Info("Search Expression = '" + searchExpression + "' not present in signature")
            return False

    # Returns number of times the pattern matched
    def GetEXISTSMatchCount(self, searchExpression):
        Debug("Returning result for searchExpression = '" + searchExpression +
             "'")
        if(searchExpression in self._result['EXISTS']):
            return self._result['EXISTS'][searchExpression]['count']
        else:
            Info("Search Expression = '" + searchExpression + "' not present in signature")
            return -1

    # Returns list of matching lines 
    def GetEXISTSMatchList(self, searchExpression):
        Debug("Returning result for searchExpression = '" + searchExpression +
             "'")
        if(searchExpression in self._result['EXISTS']):
            return self._result['EXISTS'][searchExpression]['match']
        else:
            Info("Search Expression = '" + searchExpression + "' not present in signature")
            return [] 

    # Returns value of the namevalue pattern matched
    def GetValueForName(self, name):
        Debug("Returning value for name = '" + name +
             "'")
        if(name in self._result['namevalue']):
            if(self._result['namevalue'][name]['value']):
                return self._result['namevalue'][name]['value']
            else:
                return "___VALUE_NO_NOT_FOUND___"
        else:
            Info("Namevalue = '" + name + "' not present in signature")
            return "___VALUE_NO_NOT_FOUND___"

    # Returns re match object for  the namevalue pattern matched
    def GetReMatchForName(self, name):
        Debug("Returning re match for name = '" + name +
             "'")
        if(name in self._result['namevalue']):
            if(self._result['namevalue'][name]['match']):
                return self._result['namevalue'][name]['match']
            else:
                return "___MATCH_NO_NOT_FOUND___"
        else:
            Info("Namevalue = '" + name + "' not present in signature")
            return "___MATCH_NO_NOT_FOUND___"

    # Returns full match for  the namevalue pattern matched
    def GetFullMatchForName(self, name):
        Debug("Returning full match for name = '" + name +
             "'")
        if(name in self._result['namevalue']):
            return self._result['namevalue'][name]['match'].group()
        else:
            Info("Namevalue = '" + name + "' not present in signature")
            return "___MATCH_NO_NOT_FOUND___"

    # Returns group match for  the namevalue pattern matched
    def GetGroupMatchForName(self, name, groupNumber):
        Debug("Returning group match for name = '" + name + "'" + " and group number = '" + str(groupNumber) + "'")
        if(name in self._result['namevalue']):
            try:
                return self._result['namevalue'][name]['match'].group(groupNumber)
            except:
                Info("Group number " + str(groupNumber) + " not found in result")
                return "___GROUP_NO_NOT_FOUND___"

        else:
            Info("Namevalue = '" + name + "' not present in signature")
            return "___GROUP_NO_NOT_FOUND___"
