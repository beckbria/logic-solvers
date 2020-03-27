from z3 import *
from .z3util import *
from enum import Enum

class Tents:
    EMPTY = 0
    TENT = 1
    TREE = 2

    __NO_NEIGHBOR = 0

    """Solver for the Keen logic puzzle: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/keen.html"""
    def __init__(self, treeGrid, columnCounts, rowCounts):
        """
        Creates empty rectangular tree puzzle.

        treeGrid: A 2D list of boolean.  True indicates a tree.  Must be of
            dimensions len(columnCounts) x len(rowCounts)
        columnCounts: List of count of how many tents are in each puzzle
        rowCounts: List of count of how many tents are in each row.
        """
        self.__prefix = 'tents'
        self.width = len(columnCounts)
        self.height = len(rowCounts)
        self.columnCounts = columnCounts.copy()
        self.rowCounts = rowCounts.copy()
        self.grid = Z3IntDict2D(self.width, self.height, self.__prefix)
        self.neighbor = Z3IntDict2D(self.width, self.height, self.__prefix)
        self.solver = Solver()
        self.__addValueConstraints()
        self.__addTreeConstraints(treeGrid)
        #self.__addNeighborConstraints()

    def Solution(self):
        """Solves the grid and returns a 2D array of the values"""
        self.solver.check()
        m = self.solver.model()
        answer = [[0] * self.width for i in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                answer[y][x] = int(str(m[self.grid[(x,y)]]))
        return answer

    def PrintSolution(self):
        """Returns a printable version of the solution."""
        sol = ""
        charMap = {
            Tents.EMPTY: ' ',
            Tents.TENT: '\u25ec',
            Tents.TREE: '\U0001f332',
        }
        for row in self.Solution():
            for space in row:
                sol = sol + charMap.get(space, '?')
            sol = sol + '\n'
        return sol

    def __addValueConstraints(self):
        """Adds constraints that the number of tents in each row and column match the expected total"""
        for x in range(self.width):
            for y in range(self.height):
                g = self.grid[(x,y)]
                n = self.neighbor[(x,y)]
                self.solver.add(Or([g == Tents.EMPTY, g == self.TREE, g == Tents.TENT]))
                self.solver.add(Or([
                    And([g == Tents.EMPTY, n == Tents.__NO_NEIGHBOR]),
                    And([g != Tents.EMPTY, n != Tents.__NO_NEIGHBOR])]))

    def __addTreeConstraints(self, treeGrid):
        """Adds constraints that trees are located where the grid specifics (and only there)"""
        nextNeighbor = 1
        for x in range(self.width):
            for y in range(self.height):
                g = self.grid[(x,y)]
                n = self.neighbor[(x,y)]   
                if treeGrid[y][x]:
                    # This space is a tree
                    self.solver.add(g == Tents.TREE)
                    self.solver.add(n == nextNeighbor)  ## This is the problem!  Can only compare to immutables
                    nextNeighbor = nextNeighbor + 1
                else:
                    # This space is not a tree
                    self.solver.add(g != Tents.TREE)
                    self.solver.add(n == Tents.__NO_NEIGHBOR)
        self.treeCount = nextNeighbor - 1

    def __addNeighborConstraints(self):
        """Adds constraints that there is a 1:1 neighbor relationship between trees/tents"""
        for x in range(self.width):
            for y in range(self.height):
                g = self.grid[(x,y)]
                gLeft = self.grid[(x-1, y)]
                gRight = self.grid[(x+1, y)]
                gUp = self.grid[(x, y-1)]
                gDown = self.grid[(x, y+1)]
                n = self.neighbor[(x,y)]
                nLeft = self.neighbor[(x-1, y)]
                nRight = self.neighbor[(x+1, y)]
                nUp = self.neighbor[(x, y-1)]
                nDown = self.neighbor[(x, y+1)]
                isEmpty = (g == Tents.EMPTY)
                adjacentCount = If(And([n == nLeft, g != gLeft]), 1, 0) \
                    + If(And([n == nRight, g != gRight]), 1, 0) \
                    + If(And([n == nUp, g != gUp]), 1, 0) \
                    + If(And([n == nDown, g != gDown]), 1, 0)
                self.solver.add(Or([isEmpty, adjacentCount == 1]))