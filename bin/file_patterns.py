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
