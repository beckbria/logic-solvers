from z3 import *
from .z3util import *
from enum import Enum


class Sudoku:
    EMPTY = 0
    PLUS = 1
    MINUS = 2

    """Solver for Sudoku Logic Puzzle"""

    # TODO: Constructor that takes string or array input

    def __init__(self, dimension=3):
        """
        Creates empty sudoku puzzle.

        Dimension: Size of each sub-square.  For a standard sudoku the dimension is 3
        """
        self.__prefix = 'sudoku'
        self.dimension = dimension
        self.size = dimension * dimension
        self.grid = Z3IntDict2D(self.size, self.size, self.__prefix)
        self.solver = Solver()
        self.debugPrint = False
        self.__addValueConstraints()
        self.__addRowConstraints()
        self.__addColumnConstraints()
        self.__addSubsquareConstraints()

    def Solution(self):
        """Solves the grid and returns a 2D array of the values"""
        self.solver.check()
        m = self.solver.model()
        answer = [[0] * self.size for i in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                answer[y][x] = int(str(m[self.grid[(x,y)]]))
        return answer

    def AddSquare(self, x, y, val):
        self.solver.add(self.grid[(x,y)] == val)

    def AddThermometer(self, bulbToTip, thermoclines=-1, thermoclineDelta=3):
        """
        Adds an ascending thermometer constraint
        
        bulbToTip: a list of tuples [(x1,y1), (x2,y2)]
        thermoclines: The number of thermoclines
        thermoclineDelta: the jump in value to be considered a thermocline
        """
        tcl = 0
        for n in range(1, len(bulbToTip)):
            second = self.__gridFromTuple(bulbToTip[n])
            first = self.__gridFromTuple(bulbToTip[n-1])
            tcl = tcl + If(second - first >= thermoclineDelta, 1, 0)
            self.solver.add(second > first)
        if thermoclines >= 0:
            self.solver.add(tcl == thermoclines)


    def AddMultiThermometer(self, bulbsToTip, thermoclines=-1, thermoclineDelta=3):
        """
        Adds an ascending thermometer constraint
        
        bulbToTip: a list of lists of tuples [[(x1,y1), (x2,y2)], [(x3,y3), (x2,y2)]
        thermoclines: The number of thermoclines
        thermoclineDelta: the jump in value to be considered a thermocline
        """
        tcl = 0
        for bulbToTip in bulbsToTip:
            for n in range(1, len(bulbToTip)):
                second = self.__gridFromTuple(bulbToTip[n])
                first = self.__gridFromTuple(bulbToTip[n-1])
                tcl = tcl + If(second - first >= thermoclineDelta, 1, 0)
                self.solver.add(second > first)
        if thermoclines >= 0:
            self.solver.add(tcl == thermoclines)       

    def __gridFromTuple(self, t):
        return self.grid[(t[0], t[1])]

    def __addValueConstraints(self):
        """Adds constraints that each cell is between one and the size of the grid"""
        for x in range(self.size):
            for y in range(self.size):
                g = self.grid[(x, y)]
                self.solver.add(Or([g == i for i in range(1, self.size + 1)]))


    def __addRowConstraints(self):
        """Adds constraints that the total number of plus and minus signs in each row is correct"""
        for y in range(self.size):
            row = [self.grid[(x,y)] for x in range(self.size)]
            self.solver.add(Distinct(row))
            rawRow = [(x,y) for x in range(self.size)]
            if self.debugPrint:
                print("Row Constraint: ")
                print(rawRow)


    def __addColumnConstraints(self):
        """Adds constraints that the total number of plus and minus signs in each column is correct"""
        for x in range(self.size):
            col = [self.grid[(x,y)] for y in range(self.size)]
            self.solver.add(Distinct(col))
            rawCol = [(x,y) for y in range(self.size)]
            if self.debugPrint:
                print("Col Constraint: ")
                print(rawCol)

    def __addSubsquareConstraints(self):
        for xSquare in range(self.dimension):
            for ySquare in range(self.dimension):
                left = xSquare * self.dimension
                top = ySquare * self.dimension
                subsquare = [self.grid[(left + x, top + y)] for x in range(self.dimension) for y in range(self.dimension)]
                self.solver.add(Distinct(subsquare))
                rawSubsquare = [(x,y) for x in range(self.dimension) for y in range(self.dimension)]
                if self.debugPrint:
                    print("Subsquare constraint: ")
                    print(rawSubsquare)

    
