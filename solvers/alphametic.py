from z3 import *

# Future improvements: Chains of addition/subtraction/multiplication
# to support cases like FOO+BAR+BAZ=DUCK

class Alphametic:
    """Solver for alphametic puzzles, where each letter maps uniquely to a 0-9 digit.  All letters must be in the A-Z range, case insensitive"""
    def __init__(self, base=10):
        """Creates empty square puzzle.  size: Size of the square"""
        # A map from letter to z3 variable for its value
        self.letters = {}
        self.solver = Solver()
        if not isinstance(base, int) or base < 2:
            raise ValueError("Invalid base: " + str(base))
        self.base = base
        self.prefix = "alphametic"

    def Solution(self):
        """Solves the grid and returns a dict of the values"""
        self.__addNumericConstraints()
        self.solver.check()
        m = self.solver.model()
        answer = {}
        for letter in self.letters:
            answer[letter] = int(str(m[self.letters[letter]]))
        return answer

    def AddSum(self, result, initial_value, addition):
        """
        Adds an addition constraint to the grid.

        result, initial_value, addition: Strings representing alphametic numbers or integer constants
        """
        res = self.__parseArgument(result)
        iv = self.__parseArgument(initial_value)
        add = self.__parseArgument(addition)
        self.solver.add(iv + add == res)

    def AddProduct(self, result, initial_value, multiplier):
        """
        Adds a multiplication constraint to the grid.

        result, initial_value, multiplier: Strings representing alphametic numbers or integer constants
        """
        res = self.__parseArgument(result)
        iv = self.__parseArgument(initial_value)
        mul = self.__parseArgument(multiplier)
        self.solver.add(iv * mul == res)

    def AddSubtraction(self, result, initial_value, reduction):
        """
        Adds a subtraction constraint to the grid.

        result, initial_value, reduction: Strings representing alphametic numbers or integer constants
        """
        res = self.__parseArgument(result)
        iv = self.__parseArgument(initial_value)
        red = self.__parseArgument(reduction)
        self.solver.add(iv - red == res)

    def AddDivision(self, dividend, divisor, quotient=None, remainder=None):
        """
        Adds a division constraint.  Can add constraints for either the
        quotient (integer division), the remainder, or both.

        divident, divisor: Strings representing alphametic numbers or integer constants
        quotient: String representing alphametic numbers or integer constant.  None if no constraint required
        remainder: String representing alphametic numbers or integer constant.  None if no constraint required
        """

        divid = self.__parseArgument(dividend)
        divis = self.__parseArgument(divisor)

        if quotient is not None:
            quot = self.__parseArgument(quotient)
            self.solver.add(divid / divis == quot)
        if remainder is not None:
            rem = self.__parseArgument(remainder)
            self.solver.add(divid % divis == rem)

    def __parseArgument(self, arg):
        """Parses an argument - either an alphametic string or an integer constant - into a form consumable by Z3"""
        if isinstance(arg, str):
            return self.__numberFromString(arg)
        if isinstance(arg, int):
            return arg      # TODO: I wonder if this will cause issues with non-constant-ness and we'll need to add new functions that take the integers
        raise TypeError("Not a valid parameter type")

    def __numberFromString(self, numStr):
        """Converts a string such as 'ABC' into its value i.e. base^2*A + base*B + C"""
        result = 0
        for i in range(len(numStr)):
            result = (result * self.base) + self.__variableForChar(numStr[i])
        return result

    def __variableForChar(self, char):
        """Ensures that the variable for a character exists and returns that variable"""
        c = str(char).upper()
        if len(c) != 1 or c < 'A' or c > 'Z':
            raise ValueError("Invalid letter: " + char)
        if not c in self.letters.keys():
            self.letters[c] = Int(self.prefix + c)
        return self.letters[c]

    def __addNumericConstraints(self):
        """Ensures that there are at most letters than the base size and that each is a distinct 0-n value"""
        if len(self.letters) > self.base:
            raise ValueError("More than " + self.base + " distinct letters found: " + self.letters.keys())
        self.solver.add(Distinct(list(self.letters.values())))
        for l in self.letters.values():
            self.solver.add(Or([l == j for j in range(self.base)]))

