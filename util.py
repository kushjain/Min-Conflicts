"""This file includes basic utility functions and files"""
import inspect
import sys

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


def readConfigFile(fname, N):
    """
    Choose which readConfig File to call. One deals where each row input is on different line and another deals when whole puzzle is on single line
    """"

    #Can we merge two functions together?
    
    with open(fname, 'r') as fin:
        #Easier way to access single line?
        for line in fin:
            if len(line) > N:
                result = readConfigFile_same(fname, N)
                break
            else:
                result = readConfigFile_different(fname)
        return result


def readConfigFile_different(fname):
    """
    read a sudoku input config file : Each row is in different line
    return value format: ((x-pos, y-pos), val)
    """
    i = 0
    result = []
    with open(fname, 'r') as fin:
        for line in fin:
            result.extend([((i, j), int(x)) for j,x in enumerate(line) if str.isdigit(x)])
            i = i+1
    return result

def readConfigFile_same(fname, N):
    """
    read a sudoku input config file : Complete puzzle is on same line
    return value format: ((x-pos, y-pos), val)
    """
    i = 0
    result = []
    with open(fname, 'r') as fin:

        #Improve it. There must be easier way to access a single line from file.
        for line in fin:
            puzzle = line
            break
        
        while i<N:
            row = puzzle[i*N:i*N+N+1]
            result.extend([((i, j), int(k)) for j, k in enumerate(row) if str.isdigit(k)])
            i += 1
            
    return result
