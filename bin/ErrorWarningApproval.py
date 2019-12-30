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
# from file_patterns import *
# from buckets import *


def WelcomeBanner():
    Info("Welcome to Error/Warning Aproval System...")
    #TODO Add a proper Banner
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
        ],
        default = 'nop'
    )
    parser.add_argument(
        '-xls',
        help  = "Generate Excel report",
        nargs = '?',
        const = 'ewadmin.xlsx',
    )
    # parser.add_argument(
    #     '-csv',
    #     help  = "Generate CSV report",
    #     nargs = '?',
    #     const = 'ewadmin.csv',
    # )
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



def Run():
    # Instantiate ErrorWarningManager
    instEWManager = ErrorWarningManager(
        filesPatternsToParseDict,
        errorWarningBuckets)
    Info("Total number of uncategorized errors = " +
        str(instEWManager.GetErrorsCountForBucket('uncategorized')))
    for bucket in errorWarningBuckets['errors']:
        Info("Total number of " + bucket + " errors = " +
             str(instEWManager.GetErrorsCountForBucket(bucket)))
    for file in instEWManager.GetErrorsFileListForBucket('uncategorized'):
        Info(file)

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
            Print(tabulate(eData, headers=eHeaders, tablefmt='fancy_grid'))
        # Print(pprint.pformat(eData, indent=4))

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
            Print(tabulate(wData, headers=wHeaders, tablefmt="fancy_grid"))

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
        #Print("Parsing config file = " + configFile)
        if(not os.path.isfile(configFile)):
            Critical("Config file = " + configFile + " does not exist.  Exiting...")
            continue
        config.read(configFile)
        for section in config.sections():
            dirHash = {}
            if section.lower() == "demo":
                continue
            if section.lower() == "globalignore":
                #print(config[section]['pattern'])
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

    #print(pprint.pformat(filesPatternsToParseDict, indent=4))

def List_Files(args):
    fileList = GetFileList(filesPatternsToParseDict)
    Info("The following files will be parsed...")
    if(not fileList):
        Info("Oops. No files to be parsed here. Please specify correct configuration file using -cf argument...")
    else:
        for logFile in fileList:
            Info(logFile)

def Parse_Bucket_Config_Files(args):
    Info("The bucket configuration file(s) are " + ' '.join(args.bucket_files))
    import configparser
    # filesPatternsToParseDict = {'directories':[], 'global_exclude_patterns':[]}
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

        Debug(pprint.pformat(errorWarningBuckets, indent=4))

if __name__ == '__main__':
    WelcomeBanner()
    # Parse Command-line Arguments
    Info("Parsing command-line arguments...")
    args = ParseCommandline()


    # Setup the Logger
    if(args.verbosity == 'debug'):
        SetupLogger(fileName="Approval.log", loggingLevel=logging.DEBUG)
    else:
        SetupLogger(fileName="Approval.log", loggingLevel=logging.INFO)

    SetupLogger(fileName="Approval.log", loggingLevel=logging.INFO)

    if(args.config_files):
        Info("Parsing directory configuration files...")
        Parse_Config_Files(args)

    if(args.bucket_files):
        Info("Parsing bucket configuration files...")
        Parse_Bucket_Config_Files(args)

    if(args.cmd == 'report'):
        Info("Executing report command...")
        Report(args)
    if(args.cmd == 'list_buckets'):
        Info("Executing list_buckets command...")
        List_Buckets(args)
    if(args.cmd == 'list_files'):
        Info("Executing list_files command...")
        List_Files(args)
    if(args.cmd == 'nop'):
        Info("Printing arguments...")
        Info(pprint.pformat(args))

    exit(0)


# TODO: Implement the GUI

    # Debug("Printing list of files")
    # for myFile in filesToParseList:
    #     Info(myFile)
    # # Initialize Logger
    # WelcomeBanner()
    # l = LogParser(
    #     fileName =
    #     "/nfs/sc/disks/adl_media_par_02/amitvinx/sample_logs/gtlpdssmpar1.16_oct_dupf/10_syn/logs/010_elaborate/elaborate.log",
    #     signature =
    #     {
    #         'exists':
    #         [
    #             "Initializing",
    #             "Initializing\.\.\.",
    #             "Initializing.*",
    #         ],
    #         'EXISTS':
    #         [
    #             'Initializing',
    #             'Initializing...',
    #             'Initializing.*',
    #         ],
    #         'namevalue':
    #         [
    #             {
    #                 'name' : 'totalTime',
    #                 'value': 'SNPS_INFO : METRIC \| STRING INFO.TOTAL_TIME \| (.*)',
    #             },
    #             {
    #                 'name' : 'reportTime',
    #                 'value': 'SNPS_INFO   : METRIC \| STRING INFO.REPORT_TIME \| (.*)',
    #             },
    #             {
    #                 'name' : 'toolName',
    #                 'value': 'SNPS_INFO   : (METRIC) \| STRING    SYS.TOOL_NAME \| (.*)',
    #             },
    #             {
    #                 'name' : 'sevStep',
    #                 'value': 'SNPS_INFO   : SEV variable defined: SEV\(step\) : (.*)',
    #             },
    #             {
    #                 'name' : 'experiment',
    #                 'value': ' SEV variable defined: SEV\(log_file\) : \/nfs\/sc\/disks\/adl_dssm_par_01\/nayakotx\/(.*)',
    #             },
    #             {
    #                 'name' : 'multiple',
    #                 'value': 'Lynx-INFO==> Elapsed wall time of subtask \'(.*)\'      : (.*)',
    #             },
    #         ]
    #     }
    # )
    # l.Parse()
    # Info(l.DidExistsMatch('Initializing'))
    # Info(l.GetExistsMatchCount('Initialiing'))
    # for m in l.GetEXISTSMatchList('Initializing.*'):
        #     print(m)
        # Info("Tool name = " + l.GetValueForName('toolName'))
        # Info("Full match = " + l.GetReMatchForName('toolName').group())
        # Info("Group 1 match = " + l.GetGroupMatchForName('toolName', 1))
        # Info("Group 2 match = " + l.GetGroupMatchForName('toolName', 2))
        # Info("SEV Step = " + l.GetValueForName('sevStep'))
        # Info("Experiment = " + l.GetValueForName('experiment'))
        # Info("Group 1 = " + l.GetGroupMatchForName('experiment', 1))
        # Info("Group 2 = " + l.GetGroupMatchForName('experiment', 2))
        # Info("Full Match = " + l.GetFullMatchForName('experiment'))
        #
        # Info("Multiple Group 1 = " + l.GetGroupMatchForName('multiple', 1))
        # Info("Multiple Group 2 = " + l.GetGroupMatchForName('multiple', 2))
# def donothing():
#     filewin = tkinter.Toplevel(root)
#     button = tkinter.Button(filewin, text="Do nothing button")
#     button.pack()
# root = tkinter.Tk()
# # Code to add widgets will go here...
# menubar = tkinter.Menu(root)
# filemenu = tkinter.Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", command=donothing)
# filemenu.add_command(label="Open", command=donothing)
# filemenu.add_command(label="Save", command=donothing)
# filemenu.add_command(label="Save as...", command=donothing)
# filemenu.add_command(label="Close", command=donothing)
#
# filemenu.add_separator()
#
# filemenu.add_command(label="Exit", command=root.quit)
# menubar.add_cascade(label="File", menu=filemenu)
# editmenu = tkinter.Menu(menubar, tearoff=0)
# editmenu.add_command(label="Undo", command=donothing)
#
# editmenu.add_separator()
#
# editmenu.add_command(label="Cut", command=donothing)
# editmenu.add_command(label="Copy", command=donothing)
# editmenu.add_command(label="Paste", command=donothing)
# editmenu.add_command(label="Delete", command=donothing)
# editmenu.add_command(label="Select All", command=donothing)
#
# menubar.add_cascade(label="Edit", menu=editmenu)
# helpmenu = tkinter.Menu(menubar, tearoff=0)
# helpmenu.add_command(label="Help Index", command=donothing)
# helpmenu.add_command(label="About...", command=donothing)
# menubar.add_cascade(label="Help", menu=helpmenu)
#
# root.config(menu=menubar)
# root .mainloop()
