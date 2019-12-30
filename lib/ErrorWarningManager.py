'''
Created on Dec 10, 2019
@author: amitvinx
@file  : ErrorWarningManager.py
'''

import os
import re
import pprint

from Logger import *
from LogParser import *
from FileSelecter import *
from SynopsysErrorsWarnings import *

# Specify various directories and file patterns to be used for parsing
filesPatternsToParseDict = {
    # List of directories and the file patterns
    'directories': [
        # You can specify multiple such blocks
        # {
        #     'path': '/nfs/site/home/amitvinx',
        #     'exclude_dirs' : [
        #         '.vnc',
        #     ],
        #     'include' : [
        #         '.*\.log',
        #     ],
        #     'exclude' : [
        #         '^\.',
        #     ],
        #     'recursive' : True,
        #     'exclude_hidden' : True,
        #     'ignore' : False,
        # },
        # {
        #     'path': '../sample_logs',
        #     # Exclude file if directory/sub-directory matches following patterns
        #     'exclude_dirs' : [
        #         'scripts_flow',
        #     ],
        #     # Include files that match following regular expressions
        #     'include' : [
        #         r'.*\.log$',
        #         # r'\.rpt$',
        #     ],
        #     # Exclude files that match following regular expressions
        #     'exclude' : [
        #         '^\.',
        #         'scripts_flow',
        #     ],
        #     # Control recursive search
        #     'recursive' : True,
        #     # Exclude hidden_directories
        #     'exclude_hidden' : True,
        #     'ignore' : False,
        # },
    ],
    # Global patterns to exclude
    'global_exclude_patterns' : [
        # 'abc',
        # 'def',
        # 'jkl',
        # 'Xion',
    ],
}

errorWarningBuckets = {
    'warnings': {
        # 'WARNING_CHANGED_INSTANCE_NAME'  : [
        #     'Warning: Changed instance name tdl_eu_gpgpu_ctxstart_reg to tdl_eu_gpgpu_ctxstart_reg_inst .*',
        # ],
        # 'WARNING_INCONSISTENT_PIN_DIR'  : [
        #  'Warning: The pin direction of .* pin on .* cell in the .* technology library is inconsistent with the same-name pin in the .* physical library. No physical link for the logical lib cell. .*'
        # ],
        # 'WARNING_NON_DEFAULT_CONTACT_CODE'  : [
        #     'Warning: Non-default ContactCode .* on layer .* has cut size with no matching cut name found.'
        # ],



    },
    'errors': {
        # 'ERROR_NO_ATTRIBUTES'    : [
        #     'ERROR==> No attributes matching pattern.*',
        # ],
        # 'ERROR_UNABLE_EXPAND'    : [
        #     'ERROR==> Unable to expand clocks for base clock.*',
        # ],
    },
}

class ErrorWarningManager(object):
    '''
    ErrorWarningManager
    '''

    # Constructor
    # Requires file patterns to search for Error and warnings
    def __init__(self, filePatterns=None, errorWarningBuckets=None):
        Debug("ErrorWarningManager Constructor called...")

        # File patterns checks
        if(filePatterns == None):
            Critical("Can not create ErrorWarningManager without  valid file" +
                     " patterns data. Please provide a valid file patterns " +
                     " using filePatterns parameter...")

        # Buckets checks
        if(errorWarningBuckets == None):
            Critical("Can not create ErrorWarningManager without  valid buckets" +
                     " data. Please provide a valid buckets data using" +
                     " errorWarningBuckets parameter...")

        self._filePatterns = filePatterns
        self._errorWarningBuckets = errorWarningBuckets
        self._fileList = GetFileList(self._filePatterns)
        self._bucketsInfo = {'errors': {}, 'warnings': {}}
        for errorBucket in self._errorWarningBuckets['errors']:
            self._bucketsInfo['errors'][errorBucket] = {'text':{},'count':0}
        for warnBucket in self._errorWarningBuckets['warnings']:
            self._bucketsInfo['warnings'][warnBucket] = {'text':{},'count':0}

        self._bucketsInfo['errors']['uncategorized'] = {'text':{},'count':0}
        self._bucketsInfo['warnings']['uncategorized'] = {'text':{},'count':0}

        Debug(pprint.pformat(self._bucketsInfo, indent=4))

        self._Process()


    def _Process(self):
        '''
        Extract errors and warnings information
        '''
        for logFile in self._fileList:
            l = LogParser(
                fileName = logFile,
                signature =
                {
                    'exists':
                    [
                    ],
                    'EXISTS':
                    [
                        'Warning.*',
                        'Error.*',
                        'WARNING.*',
                        'ERROR.*',
                    ],
                    'namevalue':
                    [
                        # {
                        #     'name' : 'totalTime',
                        #     'value': 'SNPS_INFO : METRIC \| STRING INFO.TOTAL_TIME \| (.*)',
                        # },
                        # {
                        #     'name' : 'memoryUsed',
                        #     'value': 'SNPS_INFO   : METRIC \| INTEGER INFO\.MEMORY_USED     \| (\d+)',
                        # },
                    ]
                }
            )

            # Parse the log file
            l.Parse()

            # Bucketize the errors
            Info("Total number of errors found in file " + logFile + " = "
                 + str(len(l.GetEXISTSMatchList('ERROR.*') +
                           l.GetEXISTSMatchList('Error.*'))))
            for item in l.GetEXISTSMatchList('ERROR.*') + l.GetEXISTSMatchList('Error.*'):
                matched = False
                fileAdded = False
                # Check Automatic Tool specific bukets
                match = re.search("^E[rR][rR][oO][rR]:.*\((.*)\)", item)
                if(match):
                    bucket = match.group(1)
                    if(bucket in SynopsysErrorsWarningsDict.keys()):
                        if(bucket in self._bucketsInfo['errors']):
                            self._bucketsInfo['errors'][bucket]['count'] = self._bucketsInfo['errors'][bucket]['count'] + 1
                            Debug("COMPARING ITEM=\'" + item + "\'")
                            Debug("BUCKET=" + bucket)
                            Debug(pprint.pformat(self._bucketsInfo['errors'][bucket], indent=2))
                            if(item in self._bucketsInfo['errors'][bucket]['text']):
                                if(logFile in self._bucketsInfo['errors'][bucket]['text'][item]):
                                    self._bucketsInfo['errors'][bucket]['text'][item][logFile] = self._bucketsInfo['errors'][bucket]['text'][item][logFile] + 1
                                else:
                                    self._bucketsInfo['errors'][bucket]['text'][item][logFile] = 1
                            else:
                                self._bucketsInfo['errors'][bucket]['text'][item] = {logFile : 1}
                        else:
                            Debug("ADDING ITEM=\'" + item + "\'")
                            self._bucketsInfo['errors'][bucket] = {'count':1, 'text':{item:{logFile:1}}}

                        continue

                for bucket in self._errorWarningBuckets['errors']:
                    # Check user specified buckets
                    for pattern in self._errorWarningBuckets['errors'][bucket]:
                        searchExpression = pattern
                        searchExpression = re.sub("\s+", "\\\s+", searchExpression.strip())
                        if(bool(re.search(searchExpression, item))):
                            matched = True
                            self._bucketsInfo['errors'][bucket]['count'] = self._bucketsInfo['errors'][bucket]['count'] + 1
                            if(item in self._bucketsInfo['errors'][bucket]['text']):
                                if(logFile in self._bucketsInfo['errors'][bucket]['text'][item]):
                                    self._bucketsInfo['errors'][bucket]['text'][item][logFile] = self._bucketsInfo['errors'][bucket]['text'][item][logFile] + 1
                                else:
                                    self._bucketsInfo['errors'][bucket]['text'][item][logFile] = 1
                            else:
                                self._bucketsInfo['errors'][bucket]['text'][item] = {logFile : 1}
                                break
                    if(matched):
                        break

                if(not matched):
                    # Populate uncategorized bucket if no matching buckets found
                    self._bucketsInfo['errors']['uncategorized']['count'] = self._bucketsInfo['errors']['uncategorized']['count'] + 1
                    if(item in self._bucketsInfo['errors']['uncategorized']['text']):
                        if(logFile in self._bucketsInfo['errors']['uncategorized']['text'][item]):
                            self._bucketsInfo['errors']['uncategorized']['text'][item][logFile] = self._bucketsInfo['errors']['uncategorized']['text'][item][logFile] + 1
                        else:
                            self._bucketsInfo['errors']['uncategorized']['text'][item][logFile] = 1
                    else:
                        self._bucketsInfo['errors']['uncategorized']['text'][item] = {logFile : 1}

            # Bucketize the warnings
            Info("Total number of warnings found in file " + logFile + " = "
                 + str(len(l.GetEXISTSMatchList('WARNING.*') +
                          l.GetEXISTSMatchList('Warning.*'))))
            for item in l.GetEXISTSMatchList('WARNING.*') + l.GetEXISTSMatchList('Warning.*'):
                matched = False
                fileAdded = False
                # Check Automatic Tool specific bukets
                match = re.search("^W[aA][rR][nN][iI][nN][gG]:.*\((.*)\)", item)
                if(match):
                    bucket = match.group(1)
                    if(bucket in SynopsysErrorsWarningsDict.keys()):
                        if(bucket in self._bucketsInfo['warnings']):
                            self._bucketsInfo['warnings'][bucket]['count'] = self._bucketsInfo['warnings'][bucket]['count'] + 1
                            #Debug("COMPARING ITEM=\'" + item + "\'")
                            #Debug("BUCKET=" + bucket)
                            #Debug(pprint.pformat(self._bucketsInfo['warnings'][bucket], indent=2))
                            if(item in self._bucketsInfo['warnings'][bucket]['text']):
                                if(logFile in self._bucketsInfo['warnings'][bucket]['text'][item]):
                                    self._bucketsInfo['warnings'][bucket]['text'][item][logFile] = self._bucketsInfo['warnings'][bucket]['text'][item][logFile] + 1
                                else:
                                    self._bucketsInfo['warnings'][bucket]['text'][item][logFile] = 1
                            else:
                                self._bucketsInfo['warnings'][bucket]['text'][item] = {logFile : 1}
                        else:
                            Debug("ADDING ITEM=\'" + item + "\'")
                            self._bucketsInfo['warnings'][bucket] = {'count':1, 'text':{item:{logFile:1}}}

                        continue

                for bucket in self._errorWarningBuckets['warnings']:
                    # Check user specified buckets
                    for pattern in self._errorWarningBuckets['warnings'][bucket]:
                        searchExpression = pattern
                        searchExpression = re.sub("\s+", "\\\s+", searchExpression.strip())
                        if(bool(re.search(searchExpression, item))):
                            matched = True
                            self._bucketsInfo['warnings'][bucket]['count'] = self._bucketsInfo['warnings'][bucket]['count'] + 1
                            if(item in self._bucketsInfo['warnings'][bucket]['text']):
                                if(logFile in self._bucketsInfo['warnings'][bucket]['text'][item]):
                                    self._bucketsInfo['warnings'][bucket]['text'][item][logFile] = self._bucketsInfo['warnings'][bucket]['text'][item][logFile] + 1
                                else:
                                    self._bucketsInfo['warnings'][bucket]['text'][item][logFile] = 1
                            else:
                                self._bucketsInfo['warnings'][bucket]['text'][item] = {logFile : 1}
                                break
                    if(matched):
                        break

                if(not matched):
                    # Populate uncategorized bucket if no matching buckets found
                    self._bucketsInfo['warnings']['uncategorized']['count'] = self._bucketsInfo['warnings']['uncategorized']['count'] + 1
                    if(item in self._bucketsInfo['warnings']['uncategorized']['text']):
                        if(logFile in self._bucketsInfo['warnings']['uncategorized']['text'][item]):
                            self._bucketsInfo['warnings']['uncategorized']['text'][item][logFile] = self._bucketsInfo['warnings']['uncategorized']['text'][item][logFile] + 1
                        else:
                            self._bucketsInfo['warnings']['uncategorized']['text'][item][logFile] = 1
                    else:
                        self._bucketsInfo['warnings']['uncategorized']['text'][item] = {logFile : 1}

            Info("Data after parsing all the logs")
            Debug(pprint.pformat(self._bucketsInfo, indent=2))

    # Returns dictionary of all warnings belonging to a bucket
    def GetWarningsDictForBucket(self, bucket=None):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['warnings'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            return self._bucketsInfo['warnings'][bucket]['text']

    # Returns list of all warnings belonging to a bucket
    def GetWarningsListForBucket(self, bucket=None):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['warnings'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            return self._bucketsInfo['warnings'][bucket]['text'].keys()

    # Returns list of all files belonging to a bucket
    def GetWarningsFileListForBucket(self, bucket=None):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['warnings'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            test = {}
            for text in self._bucketsInfo['warnings'][bucket]['text'].keys():
                for log in self._bucketsInfo['warnings'][bucket]['text'][text].keys():
                    test[log] = 1
            return test.keys()

    # Returns list of all files belonging to a warning bucket
    def GetWarningsFileCountDictForBucketText(self, bucket, text):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['warnings'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            return self._bucketsInfo['warnings'][bucket]['text'][text]


    # Returns count of all warnings belonging to a bucket
    def GetWarningsCountForBucket(self, bucket=None):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['warnings'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            return self._bucketsInfo['warnings'][bucket]['count']


    # Returns dictionary of all errors belonging to a bucket
    def GetErrorsDictForBucket(self, bucket=None):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['errors'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            return self._bucketsInfo['errors'][bucket]['text']

    # Returns list of all errors belonging to a bucket
    def GetErrorsListForBucket(self, bucket=None):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['errors'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            return self._bucketsInfo['errors'][bucket]['text'].keys()

    # Returns list of all files belonging to an error bucket
    def GetErrorsFileListForBucket(self, bucket=None):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['errors'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            test = {}
            for text in self._bucketsInfo['errors'][bucket]['text'].keys():
                for log in self._bucketsInfo['errors'][bucket]['text'][text].keys():
                    test[log] = 1
            return test.keys()

    # Returns list of all files belonging to an error bucket
    def GetErrorsFileCountDictForBucketText(self, bucket, text):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['errors'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            return self._bucketsInfo['errors'][bucket]['text'][text]

    # Returns count of all errors belonging to a bucket
    def GetErrorsCountForBucket(self, bucket=None):
        if(not bucket):
            Critical("Please provide a valid bucket name using the \'bucket\' parameter")
        if(not bucket in self._bucketsInfo['errors'].keys()):
            Critical("Bucket " + bucket + " does not exist...")
        else:
            return self._bucketsInfo['errors'][bucket]['count']


    # Returns all error Bucket names
    def GetErrorsBucketsList(self):
        return self._bucketsInfo['errors'].keys()

    # Returns all warning Bucket names
    def GetWarningsBucketsList(self):
        return self._bucketsInfo['warnings'].keys()
