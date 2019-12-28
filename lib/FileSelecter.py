'''
Created on Dec 2, 2019
@author: amitvinx
@file  : FileSelecter.py
'''

import logging
import sys
import os
import re
import pprint
from Logger import *

# Returns list of files matching file patterns
def GetFileList(filePatterns):
    Debug(filePatterns)
    filesToParseList = []

    for unit in (filePatterns['directories']):
        if(unit['ignore']):
            continue
        if(unit['recursive']):
            Debug("Doing recursive search for path " + unit['path'])
            for root, dirs, files in os.walk(unit['path']):
                Debug("Root = " + root + ":")
                # Don't search .snapshot directory
                dirs[:] = [d for d in dirs if not d.startswith('.snapshot')]
                # Remove hidden directories if specified
                if(unit['exclude_hidden']):
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                # Remove exclude directories if specified
                for excludeDir in unit['exclude_dirs']:
                    Debug("Excluding directory " + excludeDir)
                    dirs[:] = [d for d in dirs if not bool(re.search(excludeDir, d))]
                # Search for files to include
                for myFile in files:
                    fileRejected = False
                    Debug("Considering file \t" + myFile)
                    for includePattern in unit['include']:
                        # Include the file if the filename matches include patterns
                        if(bool(re.search(includePattern, myFile))):
                            # Reject the file if the filename matches exclude patterns
                            for excludePattern in unit['exclude']:
                                if(excludePattern and bool(re.search(excludePattern, myFile))):
                                    fileRejected = True
                                    break
                            # Add the file if not rejected
                            if(not fileRejected):
                                filesToParseList.append(root +"/" + myFile)
                                Debug("Selected file \t" + myFile)
                                break
        else:
            Debug("Doing non-recursive search for path " + unit['path'])
            Debug("Root = " + unit['path'] + ":")
            # Search for files to include
            for myFile in os.listdir(unit['path']):
                fileRejected = False
                Debug("Considering file \t" + myFile)
                for includePattern in unit['include']:
                    # Include the file if the filename matches include patterns
                    if(bool(re.search(includePattern, myFile))):
                        # Reject the file if the filename matches exclude patterns
                        for excludePattern in unit['exclude']:
                            if(excludePattern and bool(re.search(excludePattern, myFile))):
                                fileRejected = True
                                break
                        # Add the file if not rejected
                        if(not fileRejected):
                            filesToParseList.append(unit['path'] +"/" + myFile)
                            Debug("Selected file \t" + myFile)
                            fileAdded = True
                            break

    # Remove all the files matching global exclude patterns
    for globalExcludes in filePatterns['global_exclude_patterns']:
        Debug("Excluding global exclude pattern = " + globalExcludes)
        filesToParseList[:] = [d for d in filesToParseList if not bool(re.search(globalExcludes, d))]

    # Print("Total number of files matched the criteria = " + str(len(filesToParseList)))
    # Print(pprint.pformat(filesToParseList, indent=2))
    return filesToParseList

