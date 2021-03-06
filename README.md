# Min-Conflicts
Implements Min Conflicts Algorithm to variety of problems

Inspired by CS 188 course on Artificial Intelligence (https://courses.edx.org/courses/BerkeleyX/CS188.1x-4/1T2015/info) 
This is not homework, so it does not violate any Honor Policy.

Designed and Implemented by Kush Jain (https://github.com/kushjain) and Abhishek Rose

###Problems we are trying to solve
Currently we are focusing on :

* NQueens : On a NxN chessboard, arrange the N queens in such a way that no queen threatens each other. Two queens are said to attack (or threat) each other if they lie in same column, row and diagonal
* Sudoku : Solves for N*N board

All Problem Definitions could be found in problems.py file

### Algorithms we Are Implementing
Implemented:

* Min-Conflicts : Randomly initialize all variables. The resulting state most probably violates one or more constraints imposed by problem. Select any conflicted variable at random, and assign it a new value such that it violates least constraints. More could be found at : http://en.wikipedia.org/wiki/Min-conflicts_algorithm

When we successfully complete this, we may experiment with variants of this.
All algorithms could be found in solveagents.py

### Progress

8 March
* Sudoku Board completed

7 March
* NQueens completely finished. 

4 March
* Wrote Skeleton Frameworks for Problems : NQueens, Sudoku.
* Wrote Min Conflicts Algorithms.

### Keep in Mind!

* Code can get stuck in Local minima and return sub-optimal (or wrong) solution for now.
* Instead of random initialization, greedy initialization may work better
* In Sudoku, visualize() might break depending on OS. Will revert to simple visualize
