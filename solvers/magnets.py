from z3 import *
from .z3util import *
from enum import Enum


class Magnets:
    EMPTY = 0
    PLUS = 1
    MINUS = 2

    """Solver for the Magnets logic puzzle: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/magnets.html"""

    def __init__(self, columnPlusCounts, columnMinusCounts, rowPlusCounts, rowMinusCounts):
        """
        Creates empty rectangular magnets puzzle.

        columnPlusCounts: List of count of how many plus signs are in each column (None if unknown)
        columnMinusCounts: List of count of how many minus signs are in each column (None if unknown)
        rowPlusCounts: List of count of how many plus signs are in each row. (None if unknown)
        rowMinusCounts: List of count of how many plus signs are in each row. (None if unknown)
        """
        self.__prefix = 'tents'
        if len(columnPlusCounts) != len(columnMinusCounts) or len(rowPlusCounts) != len(rowMinusCounts):
            raise ValueError('Inconsistent dimensions')

        self.width = len(columnPlusCounts)
        self.height = len(rowPlusCounts)
        self.columnPlusCounts = columnPlusCounts.copy()
        self.columnMinusCounts = columnMinusCounts.copy()
        self.rowPlusCounts = rowPlusCounts.copy()
        self.rowMinusCounts = rowMinusCounts.copy()
        self.grid = Z3IntDict2D(self.width, self.height, self.__prefix)
        self.solver = Solver()
        self.__addValueConstraints()
        self.__addRowConstraints()
        self.__addColumnConstraints()

    def Solution(self):
        """Solves the grid and returns a 2D array of the values"""
        self.solver.check()
        m = self.solver.model()
        answer = [[0] * self.width for i in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                answer[y][x] = int(str(m[self.grid[(x, y)]]))
        return answer

    def PrintSolution(self):
        """Returns a printable version of the solution."""
        sol = ""
        charMap = {
            Magnets.EMPTY: '.',
            Magnets.PLUS:  '+',
            Magnets.MINUS: '-',
        }
        for row in self.Solution():
            for space in row:
                sol = sol + charMap.get(space, '?')
            sol = sol + '\n'
        return sol

    def AddPair(self, first, second):
        """Requires that the two coordinates correspond to a magnet"""
        a = self.grid[first]
        b = self.grid[second]
        self.solver.add(Or([
            And([a == Magnets.PLUS, b == Magnets.MINUS]),
            And([a == Magnets.MINUS, b == Magnets.PLUS]),
            And([a == Magnets.EMPTY, b == Magnets.EMPTY])]))

    def __addValueConstraints(self):
        """Adds constraints that the no two cells are adjacent"""
        for x in range(self.width):
            for y in range(self.height):
                g = self.grid[(x, y)]
                self.solver.add(
                    Or([g == Magnets.EMPTY, g == Magnets.PLUS, g == Magnets.MINUS]))
                if x > 0:
                    left = self.grid[(x-1, y)]
                    self.solver.add(Or([g != left, g == Magnets.EMPTY]))
                if y > 0:
                    up = self.grid[(x, y-1)]
                    self.solver.add(Or([g != up, g == Magnets.EMPTY]))

    def __addRowConstraints(self):
        """Adds constraints that the total number of plus and minus signs in each row is correct"""
        for y in range(self.height):
            plusTarget = self.rowPlusCounts[y]
            minusTarget = self.rowMinusCounts[y]
            plusTotal = 0
            minusTotal = 0
            for x in range(self.width):
                g = self.grid[(x, y)]
                plusTotal = plusTotal + If(g == Magnets.PLUS, 1, 0)
                minusTotal = minusTotal + If(g == Magnets.MINUS, 1, 0)
            if plusTarget != None:
                self.solver.add(plusTotal == plusTarget)
            if minusTarget != None:
                self.solver.add(minusTotal == minusTarget)

    def __addColumnConstraints(self):
        """Adds constraints that the total number of plus and minus signs in each column is correct"""
        for x in range(self.width):
            plusTarget = self.columnPlusCounts[x]
            minusTarget = self.columnMinusCounts[x]
            plusTotal = 0
            minusTotal = 0
            for y in range(self.height):
                g = self.grid[(x, y)]
                plusTotal = plusTotal + If(g == Magnets.PLUS, 1, 0)
                minusTotal = minusTotal + If(g == Magnets.MINUS, 1, 0)
            if plusTarget != None:
                self.solver.add(plusTotal == plusTarget)
            if minusTarget != None:
                self.solver.add(minusTotal == minusTarget)
