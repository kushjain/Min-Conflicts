#!/usr/bin/python2
import inspect
import sys
from random import random,sample,choice, shuffle
import solveAgent


##########################################################
"""This file includes problem definitons"""

"""CODE STILL TO CONSTRUCT
class NQueensProblem
    isGoalState: We are basically calling getVar() function again. Merge the functions for redundancy purposes?
    minVal: Choose a different value if possible if the current value is in least-conflicted mode.


class sudoku
    All functions needed to be filled.
"""
#########################################################


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

class sudoku:
    """This class contains member functions which describe the empty sudoko board"""

    def __init__(self, N = 9, predefinedValues=()):
        """Initializes sudoku board. Values describe the predefined values in board: It is set containing tuples (position, value)"""
        
        # TODO check board dimensions
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

        for fixedX, fixedY in self.fixedPos:
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
                    self.valDomain[position] = self.applyUnaryConstraints(position)
                    self.board[x][y] = choice(self.valDomain[position])

        return self.board


    def isConflicted(self, state, position):
        """Tells whether given position is conflicted"""

        return self.numConflicts(state, position) > 0

    def getVar(self, state):
        """Returns randomnly selected conflicted variable"""

        xRange = [a for a in range(self.size)]
        yRange = [a for a in range(self.size)]

        while xRange and yRange:
            x = choice(xRange)
            y = choice(yRange)
            position = (x, y)

            if position in self.fixedPos:
                xRange.remove(x)
                yRange.remove(y)
                continue
                
            if self.isConflicted(state, position):
                return position
                break
            else:
                xRange.remove(x)
                yRange.remove(y)

        return -1

    def numConflicts(self, state, position):
        """Returns the number of conflicts in given state with respect to given Position"""

        result = 0
        x, y = position
        val = state[x][y]
        result = [True for i in range(self.size) if (i != y and state[x][i] == val) or (i != x and state[i][y] == val)]

        region = self.region(position)
        start = int(region[0]*(self.size**0.5))
        stop = start + int(self.size**0.5)
        result.extend([True for i in range(start,stop) for j in range(start,stop) if (i,j) != position and state[i][j] == val])

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

    def visualize(self, state):
        """Visualize the current state using ASCII-art of the board"""

        print '_' * self.size * 4
        for i in range(self.size):
            print '|',
            for j in range(self.size):
                print state[i][j], '|',
            print ''
        print ''
       
        
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
parser.add_argument("-n", type=int, default=4, help="size of problem")
args = parser.parse_args()

# can be improved?
if args.p == "NQueens":
    prob = NQueensProblem(args.n)    # no solution for < 4
    print 'NQueens: n =', args.n
elif args.p == "sudoku":
    prob = sudoku(N=args.n, predefinedValues=[((0,0), 4), ((1,1), 1), ((2,2), 2), ((3,3), 3)])
    print 'sudoku: n =', args.n   # 'n' irrelevant?

#state = prob.getStartState()
print solveAgent.minConflict(prob)
