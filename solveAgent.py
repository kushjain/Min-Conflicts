"""This file contains different Solving Agents for CSP Problems """

def minConflict(problem, numIter=1000):
    """Min Conflict : Solves Constraint Satisfaction Problems.
    Given a possible assignment of all variables in CSP, it re-assigns all variables iteratively untill all contraints are satisfied
    INPUTS:
    problem: CSP Problem
    numIter: Number of maximum Iterations Allowed
    OUTPUT
    Solution to CSP, or failure
    """

    state = problem.getStartState()

    for i in range(numIter):

        if problem.isGoalState(state):
            return state
        
        var = problem.firstConflict(state)      #Get the variable which will be re-assigned
        val = problem.getValue(state, var)      #Get the value which will be assigned. Value should be chosen such that it causes least conflicts. Ties are broken randomly
        state[var] = val

    return []
