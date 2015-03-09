#!/usr/bin/env python2

#
# convert http://magictour.free.fr/ sudoku file to config file format
# run with '-h' for help
#

def insertAtInterval(string, interval, term='\n'):
    """
    return a new string with 'term' inserted repeatedly according to 'interval'
    """
    
    newStr = ''
    for i in range(0, len(string), interval):
        newStr = newStr + string[i:i+interval] + term
    return newStr

def formatAsConfigFile(fname, N=9, writeName=''):
    """
    convert file 'fname' to config file format and write to file 'writeName'
    WARNING: No error handling
    """

    if writeName == '':
        writeName = fname + '_fmt.txt'

    fout = open(writeName, 'w')
    with open(fname, 'r') as fin:
        for line in fin:
            fout.write(insertAtInterval(line, N))
    fout.close()

##################################################

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="file to be formatted as config file")
parser.add_argument('-n', type=int, default=9, help="size of board (default: 9)")
parser.add_argument('-o', dest='output_file', default='', help="name of output config file (default: 'input_file'_fmt.txt")
args = parser.parse_args()

formatAsConfigFile(args.input_file, args.n, args.output_file)
