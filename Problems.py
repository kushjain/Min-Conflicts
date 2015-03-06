#!/usr/bin/python2
import inspect
import sys
from random import random,sample,choice
import solveAgent


##########################################################
"""This file includes problem definitons"""

"""CODE STILL TO CONSTRUCT
class NQueensProblem
    getVar - finding a conflicted variable and returning it
    numConflicts: Full Function
    getValue : Finding Possible domain of Values
    isGoalState : FInd if given state is goal state or Not


class sudoku
    All functions needed to be filled.
"""
#########################################################


class NQueensProblem:
    """ In this, we attempt to place N queens on NxN chessboard in such a way that no queen threatens each other
    Rules for Queens are standard chess. If the queens are places in a same row, same column or diagonal, they are said to attack each other.
    Thus, we have to place qeach queen in unique row, column and diagonal. """

    def __init__(self, N, debugState=[]):
        self.size = N
        if debugState:
            self.board = debugState
        else:
            self.board = [int(random()*self.size) for x in range(self.size)]     #We are only making one dimensional array as opposed to matrix and enforcing different row constraint here itself.

    def getStartState(self):
        """We have done random assignments. However, a greedy assignments may be used to improve performance"""
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

        # iterate over the pool and return the first conflicted state
        while varPool:
            var = varPool.pop()
            if self.numConflicts(state, var) > 0:
                return var

        return -1   #Return this if there is no conflicted state

    def isGoalState(self, state):
        """Returns true if goal is acheived"""

        # goal state is reached iff there are no conflicted states
        for i in range(self.size):
            if self.numConflicts(state, i) > 0:
                return False

        return True

    def getValue(self, state, var, debug=False):
        """ Find the Least Conflicted value of var"""

        conflicts = {}
        newState = list(state)
        
        #For all possible values of var, find the number of conflicts that happen with it.
        for val in range(self.size):
            newState[var] = val
            conflicts[val] = self.numConflicts(newState, var)
        
        #Find the minimum conflict values
        minConflictVal = conflicts[min(conflicts, key=conflicts.get)]

        #If there are more than one value, with same minimum number, we need to break the tie randomly, or code might get stuck in wrong solution
        allMinVal = [val for val,numConflicts in conflicts.items() if numConflicts == minConflictVal]
        minVal = choice(allMinVal)

        if debug:
            # return the whole list
            return minVal, conflicts.items()
        else:
            return minVal

    def visualize(self, state):
        """Visualize the current state using ASCII-art of the board"""

        print '_' * self.size * 4
        for i in range(self.size):
            print '|' + '___|' * state[i] + '_x_|' + '___|' * (self.size-state[i]-1)
        print ''

class sudoku:
    """This class contains member functions which describe the empty sudoko board"""

    def __init__(self, N = 9, predefinedValues=()):
        """Initializes sudoku board. Values describe the predefined values in board: It is set containing tuples (position, value)"""
        
        self.size = N


        #Initialize the board positions
        self.board = [[-1 for i in range(self.size)] for j in range(self.size)]
        self.fixedPos = set()
        for item in predefinedValues:
            pos = item[0]
            value = item[1]
            self.fixedPod.add(pos)
            self.board[pos[0]][pos[1]] = value


        #Initialize the rest of board and assign domains to rest of positions
        self.valDomain = {}
        for x in range(N):
            for y in range(N):
                pos = (x, y)
                if pos not in self.fixedPos:
                    self.valDomain[pos] = [x for x in range(1, N+1)]


    def applyUnaryConstraints(self, position):
        """Given a position, it takes the value and apply the Unary contraints with respect to fixed configuration of board"""

        domain = self.valDomain[position]
        x, y = position
        
        """Construct Code Here
        for all x in self.fixedPos:
            get fixedY
            val = board[x][fixedY]
            remove val from domain
        for all y in self.fixedPos:
            get fixedX
            val = board[fixedX][y]
            remove val from domain

        REGION CODING
        """

        #return domain
        
        raiseNotDefined()

    def getStartState(self):
        """Initializes the board, and returns starting configuration"""

        for x in range(self.size):
            for y in range(self.size):
                position = (x, y)
                if position not in fixedPos:
                    self.valDomain[position] = applyUnaryConstraints(position)
                    newVal = choice(self.valDomain[position])
                    self.board[x][y] = newVal

        return self.board


    def isGoalState(self, state):
        """Returns whether the current state is Goal"""

        raiseNotDefined()


    def iConflicted(self, state, position):
        """Tells whether given position is conflicted"""

        raiseNotDefined()
        

    def getVar(self, state):
        """Returns randomnly selected conflicted variable"""

        xRange = [a for a in range(N)]
        yRange = [a for a in range(N)]

        while True:
            x = choice(xRange)
            y = choice(yRange)
            position = (x, y)

            if position in fixedPos:
                """Remove x and y from xRange and yRange"""
                continue
                
            if isConflicted(state, position):
                pos = position
                break
            else:
                """Remove x and y from xRange and yRange"""

        #return pos
        raiseNotDefined()

    def numConflicts(self, state, position):
        """Returns the number of conflicts in given state with respect to given Position"""

        raiseNotDefined()


    def getVal(self, state, var):
        """ Find the Least Conflicted value of var"""

        conflicts = {}
        newState = state
        
        #For all possible values of var, find the number of conflicts that happen with it.
        for val in self.valDomain[var]:
            newState[var[0]][var[1]] = val
            conflicts[val] = numConflicts(self, newState, var)
        
        #Find the minimum conflict values
        minConflicts = conflicts[min(conflicts, key=conflicts.get)]

        #If there are more than one value, with same minimum number, we need to break the tie randomly, or code might get stuck in wrong solution
        allMinVal = [val for val, numConflict in conflicts.items() if numConflict == 1]
        minVal = int(random()*len(allMinVal))

        return minVal
        
        
#############################################
# HELPER FUNCTIONS
#############################################

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print "*** Method not implemented: %s at line %s of %s" % (method, line, fileName)
    sys.exit(0)


############################################
    #TESTING
###########################################

# run with '-h' for 'usage'
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", choices=['NQueens', 'sudoku'], default='NQueens', help="type of problem")
parser.add_argument("-n", type=int, default=8, help="size of problem")
args = parser.parse_args()

# can be improved?
if args.p == "NQueens":
    prob = NQueensProblem(args.n)    # no solution for < 4
    print 'NQueens: n =', args.n
elif args.p == "sudoku":
    raiseNotDefined()
    prob = sudoku()
    print 'sudoku: n =', args.n   # 'n' irrelevant?

state = prob.getStartState()
print "State", state, " Is Goal", prob.isGoalState(state)
print solveAgent.minConflict(prob, debugPrint=False)
