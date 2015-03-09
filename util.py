"""This file includes basic utility functions and files"""
import inspect
import sys
from itertools import cycle

class bcolors:
    """
    Produce colorful outputs
    usage:
            print bcolors.BOLD + 'BOLD' + 'bcolors.ENDC
    Works ONLY on *nix systems
    """
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def raiseNotDefined():
    """A helper function which helpts to exits gracefully if method is undefined."""

    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print "*** Method not implemented: %s at line %s of %s" % (method, line, fileName)
    sys.exit(0)

def readConfigFile(fname, N=9):
    """
    read a sudoku input config file and return the encoded list of values
    return value format: (x-pos, y-pos, val)
    N is the size of the board
    """

    row = cycle([x for x in range(N)])
    result = []

    with open(fname, 'r') as fin:
        val = []
        for line in fin:
            if line.strip() == '':
                continue
            i = row.next()
            val.extend([((i, j), int(x)) for j,x in enumerate(line) if str.isdigit(x)])
            if i == N-1:
                result.append(val)
                val = []
    return result
