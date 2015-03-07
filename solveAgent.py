"""This file contains different Solving Agents for CSP Problems """

def minConflict(problem, numIter=100000):
    """Min Conflict : Solves Constraint Satisfaction Problems.
    Given a possible assignment of all variables in CSP, it re-assigns all variables iteratively untill all contraints are satisfied
    INPUTS:
    problem: CSP Problem
    numIter: Number of maximum Iterations Allowed
    OUTPUT
    Solution to CSP, or failure
    """

    state = problem.getStartState()
    print "Initial State"
    problem.visualize(state)

    for i in range(numIter):
        
        var = problem.getVar(state)      #Get the next conflicted variable randomly

        #No conflict, i.e. We have solved the problem
        if var == -1:
            print "Solution state found in", i, "iterations"
            problem.visualize(state)
            return state
        
        val = problem.getValue(state, var)      #Get the value which will be assigned. Value should be chosen such that it causes least conflicts. Ties are broken randomly
        state = problem.updateBoard(state, var, val)
    
    print "Solution not found! Try with high iterations"
    return []
