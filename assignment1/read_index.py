# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
import parsing
import sys, getopt
from parsing import *

#removes 1st argument saves command line
argumentList = sys.argv[1:]

#different commands
options = ""
long_options = ["doc=","term="]
try:
    #parse argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
    #checking arguements
    docBool = False
    termBool = False
    docValue = ""
    termValue = ""

    for currentArgument, currentValue in arguments:
        if currentArgument in ("--doc"):
            docBool = True
            docValue = currentValue
        if currentArgument in ("--term"):
            termBool = True
            termValue = currentValue
    #run functions to retrieve data
    if docBool & termBool:
        getInverted(docValue, termValue)
    elif docBool:
        getDoc(docValue)
    elif termBool:
        getTerm(termValue)

except getopt.error as err:
    print(str(err))

