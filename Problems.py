#!/usr/bin/env python2
from random import random,sample,choice, shuffle
import solveAgent
import util
import os   # for detecting *nix

"""This file includes problem definitons"""


##########################################################
#NQueens
##########################################################


class NQueensProblem:
    """ In this, we attempt to place N queens on NxN chessboard in such a way that no queen threatens each other
    Rules for Queens are standard chess. If the queens are places in a same row, same column or diagonal, they are said to attack each other.
    Thus, we have to place qeach queen in unique row, column and diagonal. """

    def __init__(self, N):

        self.size = N
        self.valDomain = [x for x in range(self.size)]                      #The Value domain from which variables can take value
        self.board = [-1 for x in range(self.size)]     #We are only making one dimensional array as opposed to matrix and enforcing different row constraint here itself.

    def getStartState(self):
        """We have done random assignments, (somewhat greedily). However, a greedy assignments may be used to improve performance"""

        #Forcing Column Constraint randomly
        domain = [x for x in range(self.size)]
        shuffle(domain)
        self.board = domain
        
        return self.board

    def numConflicts(self, state, var):
        """ Find the number of conflicts in given state with respect to given variable"""

        # same column or on same diagonal i.e. abs(x1-x2) == abs(y1-y2)
        #  Illustration for diagonal:
        #     1   2   3
        # 1 |   |   | x |<------|
        # 2 |   |   |   |       |-- x=(1,3)
        # 3 | y |   |   |               |-> abs(1-3) == abs(3-1) == 2
        #     ^                 |-- y=(3,1)
        #     L-----------------|
        
        return len([True for i in range(self.size) if i != var and (state[i] == state[var] or abs(i-var) == abs(state[i]-state[var]))])

    def getVar(self, state):
        """Return randomly any conflicted state"""
       
        # randomly sample the states
        varPool = sample(range(self.size), self.size)

        # Iterate over the pool and return the first conflicted state
        while varPool:
            var = varPool.pop()
            if self.numConflicts(state, var) > 0:
                return var

        return -1   #Return this if there is no conflicted state


    def getValue(self, state, var):
        """ Find the Least Conflicted value of var"""

        conflicts = {}
        newState = list(state)
        currConflicts = self.numConflicts(state, var)
        
        #For all possible values of var, find the number of conflicts that happen with it.
        for val in self.valDomain:
            newState[var] = val
            conflicts[val] = self.numConflicts(newState, var)
        
        #Find the minimum conflict values
        minConflictVal = conflicts[min(conflicts, key=conflicts.get)]   #Sort the conflicts by values

        #If there are more than one value, with same minimum number, we need to break the tie randomly, or code might get stuck in wrong solution
        allMinVal = [val for val,numConflicts in conflicts.items() if numConflicts == minConflictVal]

        #Do the quick check to see if we are returning same value, and if possible, choose another value.
        if currConflicts == minConflictVal and len(allMinVal) != 1:
            allMinVal.remove(state[var])
        
        minVal = choice(allMinVal)


        return minVal

    def updateBoard(self, state, var, val):
        state[var] = val
        return state

    def visualize(self, state):
        """Visualize the current state using ASCII-art of the board"""

        print '_' * self.size * 4
        for i in range(self.size):
            print '|' + '___|' * state[i] + '_x_|' + '___|' * (self.size-state[i]-1)
        print ''

##########################################################
#NQueens
##########################################################
        
class sudoku:
    """This class contains member functions which describe the empty sudoko board"""

    def __init__(self, N = 9, predefinedValues=()):
        """Initializes sudoku board. Values describe the predefined values in board: It is set containing tuples (position, value)"""
        
        # board size must be n^2 for some n
        if int(N**0.5)**2 != N:
            raise Exception('sudoku: Illegal board size')

        self.size = N

        #Initialize the board positions
        self.board = [[-1 for i in range(self.size)] for j in range(self.size)]
        self.fixedPos = set()
        for pos, val in predefinedValues:
            self.fixedPos.add(pos)
            self.board[pos[0]][pos[1]] = val

        #Initialize the rest of board and assign domains to rest of positions
        self.valDomain = {}
        for x in range(self.size):
            for y in range(self.size):
                pos = (x, y)
                if pos not in self.fixedPos:
                    self.valDomain[pos] = [i for i in range(1, self.size+1)]
        
        self.region = lambda pos: (int(pos[0]/self.size**0.5), int(pos[1]/self.size**0.5))

    def applyUnaryConstraints(self, position):
        """Given a position, it takes the value and apply the Unary contraints with respect to fixed configuration of board"""

        domain = self.valDomain[position]
        x, y = position

        # iterate over each fixed point
        for fixedX, fixedY in self.fixedPos:
            # check if in same column or row or region
            if fixedX == x or fixedY == y or self.region((fixedX,fixedY)) == self.region(position):
                val = self.board[fixedX][fixedY]
                try:
                    domain.remove(val)
                except ValueError:  # 'remove' throws 'ValueError' if element not found
                    pass
        return domain

    def getStartState(self):
        """Initializes the board, and returns starting configuration"""

        for x in range(self.size):
            for y in range(self.size):
                position = (x, y)
                if position not in self.fixedPos:
                    # adjust the domain according to fixed values
                    self.valDomain[position] = self.applyUnaryConstraints(position)
                    self.board[x][y] = choice(self.valDomain[position])

        return self.board


    def isConflicted(self, state, position):
        """Tells whether given position is conflicted"""

        return self.numConflicts(state, position) > 0

    def getVar(self, state):
        """Returns randomnly selected conflicted variable"""

        Range = [(a,b) for a in range(self.size) for b in range(self.size)]

        while Range:
            position = choice(Range)

            if position in self.fixedPos:
                Range.remove(position)
                continue
                
            if self.isConflicted(state, position):
                return position
                break
            else:
                Range.remove(position)

        return -1

    def numConflicts(self, state, position):
        """Returns the number of conflicts in given state with respect to given Position"""

        x, y = position
        val = state[x][y]
        # same row
        result = [True for i in range(self.size) if (i != y and state[x][i] == val)]
        # same column
        result.extend([True for i in range(self.size) if (i != x and state[i][y] == val)])

        # same region
        region = self.region(position)
        start = region[0]*int(self.size**0.5), region[1]*int(self.size**0.5)
        stop = start[0] + int(self.size**0.5), start[1] + int(self.size**0.5)
        result.extend([True for i in range(start[0],stop[0]) for j in range(start[1],stop[1]) if (i,j) != position and state[i][j] == val])

        return len(result)

    def getValue(self, state, var):
        """ Find the Least Conflicted value of var"""

        conflicts = {}
        newState = list(state)
        currConflicts = self.numConflicts(state, var)
        
        #For all possible values of var, find the number of conflicts that happen with it.
        for val in self.valDomain[var]:
            newState = self.updateBoard(state, var, val)
            conflicts[val] = self.numConflicts(newState, var)
        
        #Find the minimum conflict values
        minConflictVal = conflicts[min(conflicts, key=conflicts.get)]   #Sort the conflicts by values

        #If there are more than one value, with same minimum number, we need to break the tie randomly, or code might get stuck in wrong solution
        allMinVal = [val for val,numConflicts in conflicts.items() if numConflicts == minConflictVal]

        minVal = choice(allMinVal)

        return minVal

    def updateBoard(self, state, var, val):
        state[var[0]][var[1]] = val
        return state

    def unix_visualize(self, state):
        """Visualize the current state using ASCII-art of the board"""
        #works only on *nix system

        # no comment needed ;)
        n = int(self.size**0.5)
        pattern = (util.bcolors.OKGREEN, util.bcolors.OKBLUE)
        print '_' * self.size * 4
        for i in range(self.size):
            print util.bcolors.WARNING + '|' + util.bcolors.ENDC,
            for j in range(self.size):
                if (i,j) in self.fixedPos:
                    print util.bcolors.UNDERLINE + util.bcolors.BOLD + str(state[i][j]) + util.bcolors.ENDC,
                else:
                    switch = (reduce(lambda rst, d: rst * n + d, self.region((i,j))))
                    print pattern[switch%2] + str(state[i][j]) + util.bcolors.ENDC,
                print util.bcolors.WARNING + '|' + util.bcolors.ENDC,
            print ''
        print ''

    def visualize(self, state):
        """Visualize the current state using ASCII-art of the board"""
        
        if os.name == 'posix':
            self.unix_visualize(state)
            return

        print '_' * self.size * 4

        for i in range(self.size):
            print '|', 
            for j in range(self.size):
                print state[i][j], '|', 
            print '' 
        print ''
        
        #util.raiseNotDefined()


############################################
    #TESTING
###########################################

# run with '-h' for 'usage'
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", choices=['NQueens', 'sudoku'], default='NQueens', help="type of problem")
parser.add_argument("-n", type=int, default=4, help="size of problem")
parser.add_argument("-i", default='test', help="file containing the initial input configuration for sudoku")
args = parser.parse_args()


if args.p == "NQueens":
    prob = [NQueensProblem(args.n)]    # no solution for < 4
    print 'NQueens: n =', args.n
elif args.p == "sudoku":
    predefValues = util.readConfigFile(args.i)
    prob = [sudoku(N=args.n, predefinedValues=val) for val in predefValues]
    print 'sudoku: n =', args.n

#state = prob.getStartState()

for p in prob:
    print solveAgent.minConflict(p)
