from z3 import *
from .z3util import *

# Future improvements:
# Assert that each square is added to only a single constraint
# Assert that every square is added to a constraint

class Keen:
    """Solver for the Keen logic puzzle: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/keen.html"""
    def __init__(self, size):
        """Creates empty square puzzle.  size: Size of the square"""
        self.__prefix = 'keen'
        self.size = size
        self.grid = Z3IntDict2D(size, size, self.__prefix)
        self.solver = Solver()
        self.__addNumericRangeConstraints()
        self.__addUniquenessConstraints()

    def Solution(self):
        """Solves the grid and returns a 2D array of the values"""
        self.solver.check()
        m = self.solver.model()
        answer = [[0] * self.size for i in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                answer[y][x] = int(str(m[self.grid[(x,y)]]))
        return answer

    def AddSum(self, target, *coordinatesList):
        """
        Adds a sum constraint to the grid.

        squares: List of (x,y) tuples
        target: The sum of those squares
        """
        self.solver.add(Sum(self.__squares(coordinatesList)) == target)

    def AddProduct(self, target, *coordinatesList):
        """
        Adds a product constraint to the grid.

        squares: List of (x,y) tuples
        target: The sum of those squares
        """
        self.solver.add(Product(self.__squares(coordinatesList)) == target)

    def AddDifference(self, target, first, second):
        """
        Adds a subtraction constraint to the grid.

        first, second: (x,y) tuples containing coordinates of the squares
        """
        sq = self.__squares([first, second])
        self.solver.add(Or(sq[0]-sq[1] == target, sq[1]-sq[0] == target))

    def AddDivision(self, target, first, second):
        """
        Adds a division constraint to the grid.

        first, second: (x,y) tuples containing coordinates of the squares
        """
        sq = self.__squares([first, second])
        self.solver.add(Or(sq[0]*target == sq[1], sq[1]*target == sq[0]))

    def __squares(self, coordinatesList):
        """Given a list of (x,y) tuples, returns the grid squares corresponding to them"""
        return list(map(lambda c: self.grid[c], coordinatesList))

    def __addNumericRangeConstraints(self):
        """Ensures that all grid squares are in the range [1,size]"""
        for key in self.grid.keys():
            self.solver.add(Or([self.grid[key] == j for j in range(1, self.size + 1)]))

    def __addUniquenessConstraints(self):
        """Ensures that all rows and columns contain distinct values"""
        row_c = [Distinct([self.grid[(j,i)] for j in range(self.size)]) for i in range(self.size)]
        col_c = [Distinct([self.grid[(i,j)] for j in range(self.size)]) for i in range(self.size)]
        self.solver.add(row_c + col_c)