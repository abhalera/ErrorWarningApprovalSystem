#!python
'''
Created on Nov 28, 2019
@author: amitvinx
@file  : ErrorWarningApproval.py
'''
try:
    import UsrIntel.R1
except:
    pass
    #Warn("Could not find UserIntel.R1 package. Ignoring...")
import sys
import os
#import tkinter
import argparse
toolPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(toolPath + '/../lib')
from Logger import *
from LogParser import *
from FileSelecter import *
from ErrorWarningManager import *
from BucketsDatabaseManager import *


def WelcomeBanner():
    print('''
        _____                   __        __               _                _                                    _ ____            _                 
       | ____|_ __ _ __ ___  _ _\ \      / /_ _ _ __ _ __ (_)_ __   __ _   / \   _ __  _ __  _ __ _____   ____ _| / ___| _   _ ___| |_ ___ _ __ ___  
       |  _| | '__| '__/ _ \| '__\ \ /\ / / _` | '__| '_ \| | '_ \ / _` | / _ \ | '_ \| '_ \| '__/ _ \ \ / / _` | \___ \| | | / __| __/ _ \ '_ ` _ \ 
       | |___| |  | | | (_) | |   \ V  V / (_| | |  | | | | | | | | (_| |/ ___ \| |_) | |_) | | | (_) \ V / (_| | |___) | |_| \__ \ ||  __/ | | | | |
       |_____|_|  |_|  \___/|_|    \_/\_/ \__,_|_|  |_| |_|_|_| |_|\__, /_/   \_\ .__/| .__/|_|  \___/ \_/ \__,_|_|____/ \__, |___/\__\___|_| |_| |_|
                                                                   |___/        |_|   |_|                                |___/                       
                                                                       ''')

def ParseCommandline():
    parser = argparse.ArgumentParser(
        prog = "ErrorWarningApproval.py",
        description = ("Error and Warnings Administratrator. "
                       "Keep the track of Errors and Warnings "
                       "in your project...")
    )
    parser.add_argument(
        'help',
        help = "Get help for a command",
        nargs='?'
    )
    parser.add_argument(
        '-cmd',
        help    = "Run a specified command",
        choices = [
            'nop',
            'list_buckets',
            'list_files',
            'report',
            'clean',
            'create_database',
            'list_database',
            'report_bucket',
            'add_bucket',
            'remove_bucket',
            'update_bucket',
        ],
        default = 'nop'
    )
    parser.add_argument(
        '-xls',
        help  = "Generate Excel report",
        nargs = '?',
        const = 'ewadmin.xlsx',
    )
    parser.add_argument(
        '-db',
        '--database',
        help  = "name of the database",
        nargs = '?',
        const = 'default.db',
    )
    parser.add_argument(
        '-csv',
        help  = "Generate CSV report",
        nargs = '?',
        const = 'ewadmin.csv',
    )
    parser.add_argument(
        '-b',
        '--bucket',
        help  = "list of buckets",
        nargs = '*',
    )
    parser.add_argument(
        '-cf',
        '--config_files',
        help  = "list of config files",
        nargs = '*',
    )
    parser.add_argument(
        '-bf',
        '--bucket_files',
        help  = "list of config files",
        nargs = '*',
    )
    parser.add_argument(
        '-m',
        '--mail',
        help  = "list of e-mail recepients",
        nargs = '*',
    )
    parser.add_argument(
        '-bre',
        '--bucket_regex',
        help  = "Bucket regular expression",
    )
    parser.add_argument(
        '-v',
        '--verbosity',
        help    = "Specify verbosity level as 'info'|'debug'",
        choices = [
            'info',
            'debug',
        ],
    )
    parser.add_argument(
        '-rl',
        '--report_level',
        help    = "Specify level of reporting'",
        choices = [
            '1',
            '2',
            '3',
            '4',
            '5',
        ],
        default = '1',
    )
    parser.add_argument(
        '-eo',
        '--errors_only',
        help   = "Report errors only",
        action = 'store_true'
    )
    parser.add_argument(
        '-wo',
        '--warnings_only',
        help   = "Report errors only",
        action = 'store_true'
    )
    parser.add_argument(
        '-gui',
        help   = "GUI mode",
        action = 'store_true'
    )

    args = parser.parse_args()
    return args

# Dump CSV Report
def GenCSVReport(instEWManager, args, eData, wData, eHeaders, wHeaders):
    pass

# Print Report on STDOUT
def GenStdoutReport(instEWManager, args):
    from tabulate import tabulate
    import textwrap
    wrapper120 = textwrap.TextWrapper(width=120)
    wrapper80  = textwrap.TextWrapper(width=80)
    wrapper50  = textwrap.TextWrapper(width=50)
    eHeaders = ["Error Bucket", "Bucket Count"]
    wHeaders = ["Warning Bucket", "Bucket Count"]
    eData    = []
    wData    = []
    if(not args.warnings_only):
        if(int(args.report_level) > 2):
            eHeaders.append("Error Messages")
            eHeaders.append("Log File")
            eHeaders.append("Log Occurences")
        else:
            if(int(args.report_level) > 1):
                eHeaders.append("Error Messages")
        for bucket in instEWManager.GetErrorsBucketsList():
            iCount = instEWManager.GetErrorsCountForBucket(bucket)
            if(args.bucket and bucket not in args.bucket):
                continue
            if(args.bucket_regex and not bool(re.search(args.bucket_regex, bucket))):
                continue
            if(int(args.report_level) > 2):
                for error in instEWManager.GetErrorsListForBucket(bucket):
                    errorLogCount = instEWManager.GetErrorsFileCountDictForBucketText(bucket, error)
                    for key in errorLogCount.keys():
                        if(args.xls):
                            eData.append([bucket, iCount, error,  key, errorLogCount[key]])
                        else:
                            eData.append([bucket, iCount, wrapper50.fill(error),  wrapper80.fill(key), errorLogCount[key]])
            else:
                if(int(args.report_level) > 1):
                    for error in instEWManager.GetErrorsListForBucket(bucket):
                        if(args.xls):
                            eData.append([bucket, iCount, error])
                        else:
                            eData.append([bucket, iCount, wrapper80.fill(error)])
                else:
                    eData.append([bucket, iCount])

        if not args.xls:
            Info('\n' + tabulate(eData, headers=eHeaders, tablefmt='fancy_grid'))
        Debug("Printing eData...")
        Debug(pprint.pformat(eData, indent=4))

    if(not args.errors_only):
        if(int(args.report_level) > 2):
            wHeaders.append("Warning Messages")
            wHeaders.append("Log File")
            wHeaders.append("Occurences")
        else:
            if(int(args.report_level) > 1):
                wHeaders.append("Warning Messages")
        for bucket in instEWManager.GetWarningsBucketsList():
            iCount = instEWManager.GetWarningsCountForBucket(bucket)
            if(args.bucket and bucket not in args.bucket):
                continue
            if(args.bucket_regex and not bool(re.search(args.bucket_regex, bucket))):
                continue
            if(int(args.report_level) > 2):
                for warning in instEWManager.GetWarningsListForBucket(bucket):
                    warningLogCount = instEWManager.GetWarningsFileCountDictForBucketText(bucket, warning)
                    for key in warningLogCount.keys():
                        if(args.xls):
                            wData.append([bucket, iCount, warning, key, warningLogCount[key]])
                        else:
                            wData.append([bucket, iCount, wrapper50.fill(warning), wrapper80.fill(key), warningLogCount[key]])
            else:
                if(int(args.report_level) > 1):
                    for warning in instEWManager.GetWarningsListForBucket(bucket):
                        if(args.xls):
                            wData.append([bucket, iCount, warning])
                        else:
                            wData.append([bucket, iCount, wrapper80.fill(warning)])
                else:
                    wData.append([bucket, instEWManager.GetWarningsCountForBucket(bucket)])
        if not args.xls:
            Info('\n' + tabulate(wData, headers=wHeaders, tablefmt="fancy_grid"))
        Debug("Printing wData...")
        Debug(pprint.pformat(wData, indent=4))

    GenXLSReport(instEWManager, args, eData, wData, eHeaders, wHeaders)
    GenCSVReport(instEWManager, args, eData, wData, eHeaders, wHeaders)


# Dump XLSX Report
def GenXLSReport(instEWManager, args, eData, wData, eHeaders, wHeaders):
    columnWidths = [
        [0, 30],
        [1, 10],
        [2, 80],
        [3, 80],
        [4, 10],
    ]
    # Keep the track of rows and columns of eData and wData
    eRowMax = eColMax = wRowMax = wColMax = 0
    if(eData):
        eRowMax = len(eData)
        eColMax = len(eData[0])
    if(wData):
        wRowMax = len(wData)
        wColMax = len(wData[0])
    #print(eRowMax, eColMax, wRowMax, wColMax)
    if(args.xls):
        import xlsxwriter
        workbook = xlsxwriter.Workbook(args.xls)
        bold     = workbook.add_format({'bold': True})
        italic   = workbook.add_format({'italic': True})
        wrap     = workbook.add_format({'text_wrap': True})
        # Populate Errors sheet
        if(not args.warnings_only):
            eWorksheet = workbook.add_worksheet("Errors")
            for i, width in columnWidths:
                eWorksheet.set_column(i, i, width)
            eWorksheet.write_row(0, 0, eHeaders, bold)
            row = 1
            for rowData in eData:
                eWorksheet.write_row(row, 0, rowData, wrap)
                row = row + 1
            eWorksheet.autofilter(0,0,eRowMax, eColMax-1)

        # Populate Warnings sheet
        if(not args.errors_only):
            wWorksheet = workbook.add_worksheet("Warnings")
            for i, width in columnWidths:
                wWorksheet.set_column(i, i, width)
            wWorksheet.write_row(0, 0, wHeaders, bold)
            row = 1
            for rowData in wData:
                wWorksheet.write_row(row, 0, rowData, wrap)
                row = row + 1
            wWorksheet.autofilter(0,0,wRowMax, wColMax-1)

        workbook.close()
        Print("Dumping report to " + args.xls)
        if(args.mail):
            if(os.name == 'posix'):
                Print("Emailing report file " + args.xls +" to " + ' '.join(args.mail))
                cmd = 'echo \"Error Warnings Approval System Report\" | mutt -s \"EWAS Report\" -a \"./' + args.xls + '\" -- ' + ''.join(args.mail)
                # print(cmd)
                os.system(cmd)
            else:
                if(os.name == 'nt'):
                    Print("OS not supported for e-mailing information...")
                else:
                    Print("OS not supported for e-mailing information...")

def Report(args):
    # Instantiate ErrorWarningManager
    instEWManager = ErrorWarningManager(filesPatternsToParseDict, errorWarningBuckets)
    GenStdoutReport(instEWManager, args)

def List_Buckets(args):
    args.report_level = 1
    Report(args)

def Parse_Config_Files(args):
    import configparser
    # filesPatternsToParseDict = {'directories':[], 'global_exclude_patterns':[]}
    for configFile in args.config_files:
        config = configparser.ConfigParser()
        Debug("Parsing config file = " + configFile)
        if(not os.path.isfile(configFile)):
            Critical("Config file = " + configFile + " does not exist.  Exiting...")
            continue
        config.read(configFile)
        for section in config.sections():
            dirHash = {}
            if section.lower() == "demo":
                continue
            if section.lower() == "globalignore":
                for pattern in config[section]['pattern'].split('```'):
                    filesPatternsToParseDict['global_exclude_patterns'].append(pattern)
            else:
                dirHash['step'] = section.lower()
                for val in config[section]:
                    if(val.lower() == 'include' or val.lower() == 'exclude' or val.lower() == 'exclude_dirs'):
                        dirHash[val] = config[section][val].split('```')
                    else:
                        if(config[section][val] == '1'):
                            dirHash[val] = True
                        else:
                            if(config[section][val] == '0'):
                                dirHash[val] = False
                            else:
                                dirHash[val] = config[section][val]

                filesPatternsToParseDict['directories'].append(dirHash)

    Debug("Printing filesPatternsToParseDict")
    Debug(pprint.pformat(filesPatternsToParseDict, indent=4))

def List_Files(args):
    fileList = GetFileList(filesPatternsToParseDict)
    Info("The following files will be parsed...")
    if(not fileList):
        Critical("Oops. No files to be parsed here. Please specify correct configuration file using -cf argument...")
    else:
        for logFile in fileList:
            Info(logFile)

def Parse_Bucket_Config_Files(args):
    Debug("The bucket configuration file(s) are " + ' '.join(args.bucket_files))
    import configparser
    for bucketFile in args.bucket_files:
        bucket = configparser.ConfigParser()
        Debug("Parsing bucket config file = " + bucketFile)
        if(not os.path.isfile(bucketFile)):
            Critical("Config file = " + bucketFile + " does not exist.  Exiting...")
            continue
        bucket.read(bucketFile)
        for section in bucket.sections():
            if section.lower() == "demo" or (section.lower() != "warnings" and section.lower() != "errors"):
                Debug("Ignoring section " + section)
                continue

            for val in bucket[section]:
                # We are processing the warnings section
                if section.lower() == "warnings":
                    errorWarningBuckets['warnings'][val.upper()] = bucket[section][val].split('```')
                # We are processing the errors section
                else:
                    errorWarningBuckets['errors'][val.upper()] = bucket[section][val].split('```')
        Debug("Printing errorWarningBuckets")
        Debug(pprint.pformat(errorWarningBuckets, indent=4))

def Create_Database(args, dbManager=None):
    Info("TODO: Input = Database Name or None, Output = Should create a new sqlite database and add required tables...")
    dbManager.Create_Database(args.database)

def List_Database(args):
    Info("TODO: Input = None, Output = Should list all the databases existing in the db sub-directory...")

def Report_Bucket(args, bucketNamesList=None):
    Info("TODO: Input = List of bucket names or None, Output = Should return details of bucket information...")

def Add_Bucket(args, bucketsInfoDict=None):
    Info("TODO: Input = Dictionary of bucket information or None, Output = Success->True, Failure->False...")

def Remove_Bucket(args, bucketNamesList=None):
    Info("TODO: Input = List of bucket names or None, Output = Should remove buckets information of the input buckets from the database...")

def Update_Bucket(args, bucketsInfoDict=None):
    Info("TODO: Input = Dictionary of bucket information or None, Update the buckets information... Output = Success->True, Failure->False...")

if __name__ == '__main__':
    WelcomeBanner()
    args = ParseCommandline()

    # Setup the Logger
    loggingLevel = logging.INFO
    if(args.verbosity == 'debug'):
        loggingLevel=logging.DEBUG

    SetupLogger(fileName="Approval.log", loggingLevel=loggingLevel)
    loggingLevel = None
    # Parse Command-line Arguments
    bucketsDbManager = BucketsDatabaseManager()

    if(args.config_files):
        Debug("Parsing directory configuration files...")
        Parse_Config_Files(args)

    if(args.bucket_files):
        Debug("Parsing bucket configuration files...")
        Parse_Bucket_Config_Files(args)

    if(args.cmd == 'report'):
        Debug("Executing report command...")
        Report(args)
    if(args.cmd == 'list_buckets'):
        Debug("Executing list_buckets command...")
        List_Buckets(args)
    if(args.cmd == 'list_files'):
        Debug("Executing list_files command...")
        List_Files(args)
    if(args.cmd == 'create_database'):
        Debug("Executing create_database command...")
        Create_Database(args, bucketsDbManager)
    if(args.cmd == 'list_database'):
        Debug("Executing list_database command...")
        List_Database(args)
    if(args.cmd == 'report_bucket'):
        Debug("Executing report_bucket command...")
        Report_Bucket(args)
    if(args.cmd == 'add_bucket'):
        Debug("Executing add_bucket command...")
        Add_Bucket(args)
    if(args.cmd == 'remove_bucket'):
        Debug("Executing remove_bucket command...")
        Remove_Bucket(args)
    if(args.cmd == 'update_bucket'):
        Debug("Executing update_bucket command...")
        Update_Bucket(args)
    if(args.cmd == 'nop'):
        Info("Printing arguments...")
        Info(pprint.pformat(args))

