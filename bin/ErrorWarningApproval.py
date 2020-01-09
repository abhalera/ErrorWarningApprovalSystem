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
import tqdm
#import tkinter
import argparse
os.environ['EWAS_ROOT'] = os.path.abspath(os.path.join(__file__ ,"../.."))
sys.path.append(os.environ['EWAS_ROOT'] + '/lib')

from Logger import *
from LogParser import *
from FileSelecter import *
from ErrorWarningManager import *
from BucketsDatabaseManager import *
from SynopsysErrorsWarnings import *
from UsersManager import *
from SessionManager import *
from SettingsManager import *

def WelcomeBanner():
    # import random
    # import time
    # random.seed(time.process_time())
    # style = random.randint(0,7)
    style = 5
    if(style == 0):
        Print('''
        ___                               _       _
       (  _`\                            ( )  _  ( )                     _
       | (_(_) _ __  _ __   _    _ __    | | ( ) | |   _ _  _ __   ___  (_)  ___     __
       |  _)_ ( '__)( '__)/'_`\ ( '__)   | | | | | | /'_` )( '__)/' _ `\| |/' _ `\ /'_ `\ 
       | (_( )| |   | |  ( (_) )| |      | (_/ \_) |( (_| || |   | ( ) || || ( ) |( (_) |
       (____/'(_)   (_)  `\___/'(_)      `\___x___/'`\__,_)(_)   (_) (_)(_)(_) (_)`\__  |
                                                                                  ( )_) |
                                                                                   \___/'
 _____                                          _       ___                 _
(  _  )                                        (_ )    (  _`\              ( )_
| (_) | _ _    _ _    _ __   _    _   _    _ _  | |    | (_(_) _   _   ___ | ,_)   __    ___ ___
|  _  |( '_`\ ( '_`\ ( '__)/'_`\ ( ) ( ) /'_` ) | |    `\__ \ ( ) ( )/',__)| |   /'__`\/' _ ` _ `\ 
| | | || (_) )| (_) )| |  ( (_) )| \_/ |( (_| | | |    ( )_) || (_) |\__, \| |_ (  ___/| ( ) ( ) |
(_) (_)| ,__/'| ,__/'(_)  `\___/'`\___/'`\__,_)(___)   `\____)`\__, |(____/`\__)`\____)(_) (_) (_)
       | |    | |                                             ( )_| |
       (_)    (_)                                             `\___/'
                                                                       ''')

    if(style == 1):
        Print('''

       ███████╗██████╗ ██████╗  ██████╗ ██████╗     ██╗    ██╗ █████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗
       ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██║    ██║██╔══██╗██╔══██╗████╗  ██║██║████╗  ██║██╔════╝
       █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝    ██║ █╗ ██║███████║██████╔╝██╔██╗ ██║██║██╔██╗ ██║██║  ███╗
       ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗    ██║███╗██║██╔══██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██║   ██║
       ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║    ╚███╔███╔╝██║  ██║██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝
       ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝

 █████╗ ██████╗ ██████╗ ██████╗  ██████╗ ██╗   ██╗ █████╗ ██╗         ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██║   ██║██╔══██╗██║         ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
███████║██████╔╝██████╔╝██████╔╝██║   ██║██║   ██║███████║██║         ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
██╔══██║██╔═══╝ ██╔═══╝ ██╔══██╗██║   ██║╚██╗ ██╔╝██╔══██║██║         ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
██║  ██║██║     ██║     ██║  ██║╚██████╔╝ ╚████╔╝ ██║  ██║███████╗    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚══════╝    ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
                                                                       ''')

    if(style == 2):
        Print('''
         #######                                #     #
         #       #####  #####   ####  #####     #  #  #   ##   #####  #    # # #    #  ####
         #       #    # #    # #    # #    #    #  #  #  #  #  #    # ##   # # ##   # #    #
         #####   #    # #    # #    # #    #    #  #  # #    # #    # # #  # # # #  # #
         #       #####  #####  #    # #####     #  #  # ###### #####  #  # # # #  # # #  ###
         #       #   #  #   #  #    # #   #     #  #  # #    # #   #  #   ## # #   ## #    #
         ####### #    # #    #  ####  #    #     ## ##  #    # #    # #    # # #    #  ####

    #                                                         #####
   # #   #####  #####  #####   ####  #    #   ##   #         #     # #   #  ####  ##### ###### #    #
  #   #  #    # #    # #    # #    # #    #  #  #  #         #        # #  #        #   #      ##  ##
 #     # #    # #    # #    # #    # #    # #    # #          #####    #    ####    #   #####  # ## #
 ####### #####  #####  #####  #    # #    # ###### #               #   #        #   #   #      #    #
 #     # #      #      #   #  #    #  #  #  #    # #         #     #   #   #    #   #   #      #    #
 #     # #      #      #    #  ####    ##   #    # ######     #####    #    ####    #   ###### #    #

                                                                       ''')

    if(style == 3):
        Print('''

        ######## ########  ########   #######  ########     ##      ##    ###    ########  ##    ## #### ##    ##  ######
        ##       ##     ## ##     ## ##     ## ##     ##    ##  ##  ##   ## ##   ##     ## ###   ##  ##  ###   ## ##    ##
        ##       ##     ## ##     ## ##     ## ##     ##    ##  ##  ##  ##   ##  ##     ## ####  ##  ##  ####  ## ##
        ######   ########  ########  ##     ## ########     ##  ##  ## ##     ## ########  ## ## ##  ##  ## ## ## ##   ####
        ##       ##   ##   ##   ##   ##     ## ##   ##      ##  ##  ## ######### ##   ##   ##  ####  ##  ##  #### ##    ##
        ##       ##    ##  ##    ##  ##     ## ##    ##     ##  ##  ## ##     ## ##    ##  ##   ###  ##  ##   ### ##    ##
        ######## ##     ## ##     ##  #######  ##     ##     ###  ###  ##     ## ##     ## ##    ## #### ##    ##  ######

   ###    ########  ########  ########   #######  ##     ##    ###    ##           ######  ##    ##  ######  ######## ######## ##     ##
  ## ##   ##     ## ##     ## ##     ## ##     ## ##     ##   ## ##   ##          ##    ##  ##  ##  ##    ##    ##    ##       ###   ###
 ##   ##  ##     ## ##     ## ##     ## ##     ## ##     ##  ##   ##  ##          ##         ####   ##          ##    ##       #### ####
##     ## ########  ########  ########  ##     ## ##     ## ##     ## ##           ######     ##     ######     ##    ######   ## ### ##
######### ##        ##        ##   ##   ##     ##  ##   ##  ######### ##                ##    ##          ##    ##    ##       ##     ##
##     ## ##        ##        ##    ##  ##     ##   ## ##   ##     ## ##          ##    ##    ##    ##    ##    ##    ##       ##     ##
##     ## ##        ##        ##     ##  #######     ###    ##     ## ########     ######     ##     ######     ##    ######## ##     ##
                                                                       ''')

    if(style == 4):
        Print('''

      d88888b d8888b. d8888b.  .d88b.  d8888b.      db   d8b   db  .d8b.  d8888b. d8b   db d888888b d8b   db  d888b
      88'     88  `8D 88  `8D .8P  Y8. 88  `8D      88   I8I   88 d8' `8b 88  `8D 888o  88   `88'   888o  88 88' Y8b
      88ooooo 88oobY' 88oobY' 88    88 88oobY'      88   I8I   88 88ooo88 88oobY' 88V8o 88    88    88V8o 88 88
      88~~~~~ 88`8b   88`8b   88    88 88`8b        Y8   I8I   88 88~~~88 88`8b   88 V8o88    88    88 V8o88 88  ooo
      88.     88 `88. 88 `88. `8b  d8' 88 `88.      `8b d8'8b d8' 88   88 88 `88. 88  V888   .88.   88  V888 88. ~8~
      Y88888P 88   YD 88   YD  `Y88P'  88   YD       `8b8' `8d8'  YP   YP 88   YD VP   V8P Y888888P VP   V8P  Y888P

 .d8b.  d8888b. d8888b. d8888b.  .d88b.  db    db  .d8b.  db           .d8888. db    db .d8888. d888888b d88888b .88b  d88.
d8' `8b 88  `8D 88  `8D 88  `8D .8P  Y8. 88    88 d8' `8b 88           88'  YP `8b  d8' 88'  YP `~~88~~' 88'     88'YbdP`88
88ooo88 88oodD' 88oodD' 88oobY' 88    88 Y8    8P 88ooo88 88           `8bo.    `8bd8'  `8bo.      88    88ooooo 88  88  88
88~~~88 88~~~   88~~~   88`8b   88    88 `8b  d8' 88~~~88 88             `Y8b.    88      `Y8b.    88    88~~~~~ 88  88  88
88   88 88      88      88 `88. `8b  d8'  `8bd8'  88   88 88booo.      db   8D    88    db   8D    88    88.     88  88  88
YP   YP 88      88      88   YD  `Y88P'     YP    YP   YP Y88888P      `8888Y'    YP    `8888Y'    YP    Y88888P YP  YP  YP
                                                                       ''')

    if(style == 5):
        Print('''
        8888888888                                      888       888                           d8b
        888                                             888   o   888                           Y8P
        888                                             888  d8b  888
        8888888    888d888 888d888 .d88b.  888d888      888 d888b 888  8888b.  888d888 88888b.  888 88888b.   .d88b.
        888        888P"   888P"  d88""88b 888P"        888d88888b888     "88b 888P"   888 "88b 888 888 "88b d88P"88b
        888        888     888    888  888 888          88888P Y88888 .d888888 888     888  888 888 888  888 888  888
        888        888     888    Y88..88P 888          8888P   Y8888 888  888 888     888  888 888 888  888 Y88b 888
        8888888888 888     888     "Y88P"  888          888P     Y888 "Y888888 888     888  888 888 888  888  "Y88888
                                                                                                                  888
                                                                                                             Y8b d88P
                                                                                                              "Y88P"
       d8888                                                     888       .d8888b.                    888
      d88888                                                     888      d88P  Y88b                   888
     d88P888                                                     888      Y88b.                        888
    d88P 888 88888b.  88888b.  888d888 .d88b.  888  888  8888b.  888       "Y888b.   888  888 .d8888b  888888 .d88b.  88888b.d88b.
   d88P  888 888 "88b 888 "88b 888P"  d88""88b 888  888     "88b 888          "Y88b. 888  888 88K      888   d8P  Y8b 888 "888 "88b
  d88P   888 888  888 888  888 888    888  888 Y88  88P .d888888 888            "888 888  888 "Y8888b. 888   88888888 888  888  888
 d8888888888 888 d88P 888 d88P 888    Y88..88P  Y8bd8P  888  888 888      Y88b  d88P Y88b 888      X88 Y88b. Y8b.     888  888  888
d88P     888 88888P"  88888P"  888     "Y88P"    Y88P   "Y888888 888       "Y8888P"   "Y88888  88888P'  "Y888 "Y8888  888  888  888
             888      888                                                                 888
             888      888                                                            Y8b d88P
             888      888                                                             "Y88P"
                                                                       ''')

    if(style == 6):
        Print('''
      `7MM"""YMM                                        `7MMF'     A     `7MF'                             db
        MM    `7                                          `MA     ,MA     ,V
        MM   d    `7Mb,od8 `7Mb,od8 ,pW"Wq.`7Mb,od8        VM:   ,VVM:   ,V ,6"Yb.  `7Mb,od8 `7MMpMMMb.  `7MM  `7MMpMMMb.  .P"Ybmmm
        MMmmMM      MM' "'   MM' "'6W'   `Wb MM' "'         MM.  M' MM.  M'8)   MM    MM' "'   MM    MM    MM    MM    MM :MI  I8
        MM   Y  ,   MM       MM    8M     M8 MM             `MM A'  `MM A'  ,pm9MM    MM       MM    MM    MM    MM    MM  WmmmP"
        MM     ,M   MM       MM    YA.   ,A9 MM              :MM;    :MM;  8M   MM    MM       MM    MM    MM    MM    MM 8M
      .JMMmmmmMMM .JMML.   .JMML.   `Ybmd9'.JMML.             VF      VF   `Moo9^Yo..JMML.   .JMML  JMML..JMML..JMML  JMML.YMMMMMb
                                                                                                                           6'     dP
                                                                                                                            Ybmmmd'
                                                                      ,,
      db                                                            `7MM       .M"""bgd                   mm
     ;MM:                                                             MM      ,MI    "Y                   MM
    ,V^MM.   `7MMpdMAo.`7MMpdMAo.`7Mb,od8 ,pW"Wq.`7M'   `MF',6"Yb.    MM      `MMb.  `7M'   `MF',pP"Ybd mmMMmm .gP"Ya `7MMpMMMb.pMMMb.
   ,M  `MM     MM   `Wb  MM   `Wb  MM' "'6W'   `Wb VA   ,V 8)   MM    MM        `YMMNq.VA   ,V  8I   `"   MM  ,M'   Yb  MM    MM    MM
   AbmmmqMA    MM    M8  MM    M8  MM    8M     M8  VA ,V   ,pm9MM    MM      .     `MM VA ,V   `YMMMa.   MM  8M""""""  MM    MM    MM
  A'     VML   MM   ,AP  MM   ,AP  MM    YA.   ,A9   VVV   8M   MM    MM      Mb     dM  VVV    L.   I8   MM  YM.    ,  MM    MM    MM
.AMA.   .AMMA. MMbmmd'   MMbmmd' .JMML.   `Ybmd9'     W    `Moo9^Yo..JMML.    P"Ybmmd"   ,V     M9mmmP'   `Mbmo`Mbmmd'.JMML  JMML  JMML.
               MM        MM                                                             ,V
             .JMML.    .JMML.                                                        OOb"
                                                                       ''')

    if(style == 7):
        Print('''
       88888888b                                        dP   dP   dP                            oo
       88                                               88   88   88
      a88aaaa    88d888b. 88d888b. .d8888b. 88d888b.    88  .8P  .8P .d8888b. 88d888b. 88d888b. dP 88d888b. .d8888b.
       88        88'  `88 88'  `88 88'  `88 88'  `88    88  d8'  d8' 88'  `88 88'  `88 88'  `88 88 88'  `88 88'  `88
       88        88       88       88.  .88 88          88.d8P8.d8P  88.  .88 88       88    88 88 88    88 88.  .88
       88888888P dP       dP       `88888P' dP          8888' Y88'   `88888P8 dP       dP    dP dP dP    dP `8888P88
                                                                                                                 .88
                                                                                                             d8888P
 .d888888                                                        dP    .d88888b                      dP
d8'    88                                                        88    88.    "'                     88
88aaaaa88a 88d888b. 88d888b. 88d888b. .d8888b. dP   .dP .d8888b. 88    `Y88888b. dP    dP .d8888b. d8888P .d8888b. 88d8b.d8b.
88     88  88'  `88 88'  `88 88'  `88 88'  `88 88   d8' 88'  `88 88          `8b 88    88 Y8ooooo.   88   88ooood8 88'`88'`88
88     88  88.  .88 88.  .88 88       88.  .88 88 .88'  88.  .88 88    d8'   .8P 88.  .88       88   88   88.  ... 88  88  88
88     88  88Y888P' 88Y888P' dP       `88888P' 8888P'   `88888P8 dP     Y88888P  `8888P88 `88888P'   dP   `88888P' dP  dP  dP
           88       88                                                                .88
           dP       dP                                                            d8888P
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
            'select_database',
            'current_database',
            'report_bucket',
            'add_bucket',
            'remove_bucket',
            'update_bucket',
            'add_user',
            'remove_user',
            'show_config'
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
        help  = "Database number",
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
    import termcolor
    wrapper120 = textwrap.TextWrapper(width=120)
    wrapper80  = textwrap.TextWrapper(width=80)
    wrapper50  = textwrap.TextWrapper(width=50)
    wrapper40  = textwrap.TextWrapper(width=40)
    wrapper30  = textwrap.TextWrapper(width=30)
    eHeaders = ["Error Bucket", "Num"]
    wHeaders = ["Warning Bucket", "Num"]
    eData    = []
    wData    = []
    if(not args.warnings_only):
        if(int(args.report_level) > 1):
            eHeaders.append("Error Messages")
        if(int(args.report_level) > 2):
            eHeaders.append("Log File")
            eHeaders.append("FC")
        if(int(args.report_level) > 3):
            eHeaders.append("Short Description")
        if(int(args.report_level) > 4):
            eHeaders.append("Full Description")

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
                            if(int(args.report_level) > 4):
                                if(bucket in SynopsysErrorsWarningsDict):
                                    eData.append([bucket, iCount, error,  key, errorLogCount[key], SynopsysErrorsWarningsDict[bucket]['short'], SynopsysErrorsWarningsDict[bucket]['full']])
                                else:
                                    eData.append([bucket, iCount, error,  key, errorLogCount[key], "NA", "NA"])
                            else:
                                if(int(args.report_level) > 3):
                                    if(bucket in SynopsysErrorsWarningsDict):
                                        eData.append([bucket, iCount, error,  key, errorLogCount[key], SynopsysErrorsWarningsDict[bucket]['short']])
                                    else:
                                        eData.append([bucket, iCount, error,  key, errorLogCount[key], "NA"])
                                else:
                                    eData.append([bucket, iCount, error,  key, errorLogCount[key]])
                        else:
                            if(int(args.report_level) > 4):
                                if(bucket in SynopsysErrorsWarningsDict):
                                    eData.append([bucket, iCount, wrapper50.fill(error),  wrapper30.fill(key), errorLogCount[key], wrapper30.fill(SynopsysErrorsWarningsDict[bucket]['short']), wrapper40.fill(SynopsysErrorsWarningsDict[bucket]['full'])])
                                else:
                                    eData.append([bucket, iCount, wrapper50.fill(error),  wrapper30.fill(key), errorLogCount[key], "NA", "NA"])
                            else:
                                if(int(args.report_level) > 3):
                                    if(bucket in SynopsysErrorsWarningsDict):
                                        eData.append([bucket, iCount, wrapper40.fill(error),  wrapper50.fill(key), errorLogCount[key], wrapper50.fill(SynopsysErrorsWarningsDict[bucket]['short'])])
                                    else:
                                        eData.append([bucket, iCount, wrapper40.fill(error),  wrapper50.fill(key), errorLogCount[key], "NA"])
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
            print(colored('\nError information listed below...\n', 'yellow', attrs=['bold']) + tabulate(eData, headers=eHeaders, tablefmt='fancy_grid'))
            Log('\nError information listed below...\n' + tabulate(eData, headers=eHeaders, tablefmt='fancy_grid'))

        Debug("Printing eData...")
        Debug(pprint.pformat(eData, indent=4))

    if(not args.errors_only):
        if(int(args.report_level) > 1):
            wHeaders.append("Warning Messages")
        if(int(args.report_level) > 2):
            wHeaders.append("Log File")
            wHeaders.append("FC")
        if(int(args.report_level) > 3):
            wHeaders.append("Short Description")
        if(int(args.report_level) > 4):
            wHeaders.append("Full Description")

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
                            if(int(args.report_level) > 4):
                                if(bucket in SynopsysErrorsWarningsDict):
                                    wData.append([bucket, iCount, warning,  key, warningLogCount[key], SynopsysErrorsWarningsDict[bucket]['short'], SynopsysErrorsWarningsDict[bucket]['full']])
                                else:
                                    wData.append([bucket, iCount, warning,  key, warningLogCount[key], "NA", "NA"])
                            else:
                                if(int(args.report_level) > 3):
                                    if(bucket in SynopsysErrorsWarningsDict):
                                        wData.append([bucket, iCount, warning,  key, warningLogCount[key], SynopsysErrorsWarningsDict[bucket]['short']])
                                    else:
                                        wData.append([bucket, iCount, warning,  key, warningLogCount[key], "NA"])
                                else:
                                    wData.append([bucket, iCount, warning,  key, warningLogCount[key]])
                        else:
                            if(int(args.report_level) > 4):
                                if(bucket in SynopsysErrorsWarningsDict):
                                    wData.append([bucket, iCount, wrapper50.fill(warning),  wrapper30.fill(key), warningLogCount[key], wrapper30.fill(SynopsysErrorsWarningsDict[bucket]['short']), wrapper40.fill(SynopsysErrorsWarningsDict[bucket]['full'])])
                                else:
                                    wData.append([bucket, iCount, wrapper50.fill(warning),  wrapper30.fill(key), warningLogCount[key], "NA", "NA"])
                            else:
                                if(int(args.report_level) > 3):
                                    if(bucket in SynopsysErrorsWarningsDict):
                                        wData.append([bucket, iCount, wrapper40.fill(warning),  wrapper50.fill(key), warningLogCount[key], wrapper50.fill(SynopsysErrorsWarningsDict[bucket]['short'])])
                                    else:
                                        wData.append([bucket, iCount, wrapper40.fill(warning),  wrapper50.fill(key), warningLogCount[key], "NA"])
                                else:
                                    wData.append([bucket, iCount, wrapper50.fill(warning),  wrapper80.fill(key), warningLogCount[key]])
                        # if(args.xls):
                            # wData.append([bucket, iCount, warning, key, warningLogCount[key]])
                        # else:
                            # wData.append([bucket, iCount, wrapper50.fill(warning), wrapper80.fill(key), warningLogCount[key]])
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
            print(colored('\nWarning information listed below...\n', 'yellow', attrs=['bold']) + tabulate(wData, headers=wHeaders, tablefmt="fancy_grid"))
            Log('\nWarning information listed below...\n' + tabulate(wData, headers=wHeaders, tablefmt="fancy_grid"))
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
            prevData = 'StartingRow'
            for rowData in eData:
                eWorksheet.write_row(row, 0, rowData, wrap)
                if(int(args.report_level) >= 2):
                    eWorksheet.set_row(row,None,None,{'level' : 1})
                    if(rowData[0] != prevData):
                        if(prevData != 'StartingRow'):
                            Debug("Setting row = " + str(row-1) + " as collapsed")
                            eWorksheet.set_row(row-1,None,None,{'collapsed' : True})
                    prevData = rowData[0]
                row = row + 1
            if(int(args.report_level) >= 2):
                eWorksheet.set_row(row-1,None,None,{'collapsed' : True})

            eWorksheet.autofilter(0,0,eRowMax, eColMax-1)

        # Populate Warnings sheet
        if(not args.errors_only):
            wWorksheet = workbook.add_worksheet("Warnings")
            for i, width in columnWidths:
                wWorksheet.set_column(i, i, width)
            wWorksheet.write_row(0, 0, wHeaders, bold)
            row = 1
            prevData = 'StartingRow'
            for rowData in wData:
                wWorksheet.write_row(row, 0, rowData, wrap)
                if(int(args.report_level) >= 2):
                    wWorksheet.set_row(row,None,None,{'level' : 1})
                    if(rowData[0] != prevData):
                        if(prevData != 'StartingRow'):
                            Debug("Setting row = " + str(row-1) + " as collapsed")
                            wWorksheet.set_row(row-1,None,None,{'collapsed' : True})
                    prevData = rowData[0]
                row = row + 1
            if(int(args.report_level) >= 2):
                wWorksheet.set_row(row-1,None,None,{'collapsed' : True})

            wWorksheet.autofilter(0,0,wRowMax, wColMax-1)

        workbook.close()
        Info("Dumping report to " + args.xls)
        if(args.mail):
            if(os.name == 'posix'):
                Info("Emailing report file " + args.xls +" to " + ' '.join(args.mail))
                cmd = 'echo \"Error Warnings Approval System Report\" | mutt -s \"EWAS Report\" -a \"./' + args.xls + '\" -- ' + ''.join(args.mail)
                # print(cmd)
                os.system(cmd)
            else:
                if(os.name == 'nt'):
                    Warn("OS not supported for e-mailing information...")
                else:
                    Warn("OS not supported for e-mailing information...")

def Report(args):
    # Instantiate ErrorWarningManager
    instEWManager = ErrorWarningManager(filesPatternsToParseDict, errorWarningBuckets)
    GenStdoutReport(instEWManager, args)

def List_Buckets(args):
    args.report_level = 1
    Report(args)

#   Database related functions
def List_Databases(args):
    Info("List of Databases available = ")
    i = 1
    for database in SettingsManager().Get_Databases_List():
        Info('\t' + str(i) + '. '+ database)
        i+=1

def Select_Database(args):
    List_Databases(args)
    dbNumber = int(input("Enter database number to select: "))-1
    BucketsDatabaseManager().Select_Database(SettingsManager().Get_Database(dbNumber))
    Current_Database(args)

def Current_Database(args):
    Info("Current Database : " + BucketsDatabaseManager().Selected_Database())

def Parse_Config_Files(args, files=None):
    import configparser
    if(not files):
        files = args.config_files

    for configFile in files:
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

def Parse_Bucket_Config_Files(args, files=None):
    Debug("The bucket configuration file(s) are " + ' '.join(args.bucket_files))
    import configparser
    if(not files):
        files = args.bucket_files

    for bucketFile in files:
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

def Create_Database(args, dbManager):
    if(not dbManager):
        Critical("dbManager is None. Can't create database. Exiting...")
    dbManager.Create_Database(dbName=args.database)

def Report_Bucket(args, bucketNamesList=None):
    Info("TODO: Input = List of bucket names or None, Output = Should return details of bucket information...")

def Add_Bucket(args, bucketsInfoDict=None):
    Info("TODO: Input = Dictionary of bucket information or None, Output = Success->True, Failure->False...")

def Remove_Bucket(args, bucketNamesList=None):
    Info("TODO: Input = List of bucket names or None, Output = Should remove buckets information of the input buckets from the database...")

def Update_Bucket(args, bucketsInfoDict=None):
    Info("TODO: Input = Dictionary of bucket information or None, Update the buckets information... Output = Success->True, Failure->False...")

def Add_User(args, usersManager):
    session = SessionManager()
    import getpass
    import hashlib
    Info("Please enter the details about the user to be added below...")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    email = input("Email: ")
    isAdmin = input("Is Admin? 0->No, 1->Yes: ")
    if(usersManager.Add_User(username=username, password=hashlib.md5(str(password).encode('utf-8')).hexdigest(), email=email, is_admin=bool(isAdmin))):
        Critical("Could not add the user...")
    else:
        Info("User " + username + " successfully added to the database...")

def Remove_User(args, usersManager):
    session = SessionManager()
    if(not session.IsAdmin()):
        Critical("You are not an ADMINISTRATOR. You can not remove a user...")

    import getpass
    import hashlib
    Info("Please enter the details about the user to be removed below...")
    username = input("Username: ")
    if(usersManager.Remove_User(username=username)):
        Critical("Could not remove the user...")
    else:
        Info("User " + username + " successfully removed from the database...")

def Show_Config(args):
    session = SessionManager()
    Print("Printing current settings for EWAS...")
    Info("Default Database = " + SettingsManager().Get_Default_Database())
    Info("List of Databases = ")
    for database in SettingsManager().Get_Databases_List():
        Info('\t' + database)
    Info("List of Search Config Files = ")
    for myFile in SettingsManager().Get_Search_Config_Files_List():
        Info('\t' + myFile)
    Info("List of Bucket Config Files = ")
    for myFile in SettingsManager().Get_Bucket_Config_Files_List():
        Info('\t' + myFile)

if __name__ == '__main__':
    # Parse Command-line Arguments
    args = ParseCommandline()

    # Setup the Logger
    loggingLevel = logging.INFO
    if(args.verbosity == 'debug'):
        loggingLevel=logging.DEBUG

    SetupLogger(fileName="Approval.log", loggingLevel=loggingLevel)
    loggingLevel = None
    WelcomeBanner()
    session = SessionManager()
    settingsManager = SettingsManager()
    bucketsDbManager = BucketsDatabaseManager()
    usersManager = UsersManager()

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
        List_Databases(args)
    if(args.cmd == 'select_database'):
        Debug("Executing select_database command...")
        Select_Database(args)
    if(args.cmd == 'current_database'):
        Debug("Executing current_database command...")
        Current_Database(args)
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
    if(args.cmd == 'add_user'):
        Debug("Executing add_user command...")
        Add_User(args, usersManager)
    if(args.cmd == 'remove_user'):
        Debug("Executing remove_user command...")
        Remove_User(args, usersManager)
    if(args.cmd == 'show_config'):
        Debug("Executing show_config command...")
        Show_Config(args)
    if(args.cmd == 'nop'):
        Info("Printing arguments...")
        Info(pprint.pformat(args))

