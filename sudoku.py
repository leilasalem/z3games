from z3 import *
from itertools import combinations


def exactly_one(literals):
    c = []
    for pair in combinations(literals, 2):
        a, b = pair[0], pair[1]
        c += [Or(literals)]
        return And(c)

# print all the lines corresponding to line of grid
def print_solution(model, literals):
    lines = []
    for i in range(9):
        lines += [[]]
        for j in range(9):
            # look for corresponding digit to cell
            digit = 0
            for x in range(9):
                if model.evaluate(lits[i][j][x]):
                    digit = x + 1
                lines[i] += [digit]
        
    for line in lines:
        print(" ".join([str(x) for x in line]))

def solve(grid):
    # Define the literals
    # sudoku : 9x9 grid
    # for each cell, 9 different digits
    # literals: 9 x 9 x 9 grid

    lits = []
    for i in range(9):
        lits += [[]]
        for j in range(9):
            lits[i] += [[]]
            for digit in range(9):
                lits[i][j] += [Bool("x_%i_%i_%i" % (i, j, digit))]

    s = Solver()

    # Add first set of constraints
    # one possible value for each cell
    for i in range(9):
        for j in range(9):
            s.add(exactly_one(lits[i][j]))

    # each value occurs only once per row
    for i in range(9):
        for x in range(9):
            row = []
            for j in range(9):
                row += [lits[i][j][x]]
            s.add(exactly_one(row))

    # and once per column
    for j in range(9):
        for x in range(9):
            s.add(exactly_one([lits[i][j][x] for i in range(9)]))

    # each value used only once in each 3x3 subgrid
    # for every subgrid
    for i in range(3):
        for j in range(3):
            # need to do this (cells line 55) for every digit
            # and separate constraints for each so -
            for k in range(9):
                grid_cells = []
            # for every cell in each subgrid
                for x in range(3):
                    for y in range(3):
                        grid_cells += [lits[3*i + x][3*j+y][k]]
                    s.add(exactly_one(grid_cells))
        
        # now assume we have matrix grid[][] representing values in grid
        # 0 means there is no value
        # we add the constraints to ensure literals set accordingly

        for i in range(9):
            for j in range(9):
                if grid[i][j] > 0:
                    s.add(lits[i][j][grid[i][j]-1])
        
        if str(s.check()) == 'sat':
            print_solution(s.model(), lits)
        else:
            print("unsat")
