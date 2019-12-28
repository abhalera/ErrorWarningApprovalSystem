from SynopsysErrorsWarnings import *
import os
import subprocess
import re
f = open("SynopsysErrorsWarningsNew.py", "w")
f.write("SynopsysErrorsWarningsDict = [\n")
count = 1
for rwId in SynopsysErrorsWarningsDict:
    # test = os.system("sed -n -e \'/" + rwId + "/,/WHAT NEXT/ p\' ./SynopsysErrorsWarnings.py.bak")
    cmd = ["sed", "-n", "-e", "/" + rwId + "/,/WHAT/p", "./SynopsysErrorsWarnings.py.bak"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
    full  = ""
    short = ""
    myList = result.split("\n")
    start = 0
    end = 0
    for line in myList:
        if end == 0:
            end = 1
            continue

        if(bool(re.search("DESCRIPTION", line))):
            end = 11111111
            start = 1
            continue
        if(bool(re.search("^WHAT", line))):
            continue
        if start == 1:
            start = 0
            full = full + " " + re.sub("^\s+", "", line)
        if end != 11111111:
            short = short + " " + re.sub("^\s+", "", line)


    full  = re.sub("^\s+", "", full)
    short = re.sub("^\s+", "", short)
    f.write("'" + rwId + "'" + ":\n{\n'short': \"" + short + "\",\n'full' : \"" + full + "\"\n},\n")
    print(count)
    count = count + 1


f.write("]")
f.close()
