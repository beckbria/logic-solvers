from .context import solvers
from solvers import Alphametic
import unittest

class AlphameticTest(unittest.TestCase):
    """Tests for the Alphametic solver"""

    def testDivision(self):
        a = Alphametic()
        a.AddDivision(dividend="FHPOHSKF", divisor="ITSSKR", quotient="HIF")
        a.AddDivision(dividend="FHPOHS", divisor="ITSSKR", quotient="H", remainder="TPRPI")
        a.AddProduct(result="FISSHK", initial_value="ITSSKR", multiplier="H")
        a.AddSubtraction(result="TPRPI", initial_value="FHPOHS", reduction="FISSHK")
        a.AddDivision(dividend="TPRPIK", divisor="ITSSKR", quotient="I", remainder="RRPCI")
        a.AddProduct(result="ITSSKR", initial_value="ITSSKR", multiplier="I")
        a.AddSubtraction(result="RRPCI", initial_value="TPRPIK", reduction="ITSSKR")
        a.AddDivision(dividend="RRPCIF", divisor="ITSSKR", quotient="F", remainder="ITPCKP")
        a.AddProduct(result="OHSSCF", initial_value="ITSSKR", multiplier="F")
        a.AddSubtraction(result="ITPCKP", initial_value="RRPCIF", reduction="OHSSCF")
        expectedSolution = {"P":0, "I": 1, "T": 2, "C": 3, "H": 4, "F": 5, "O": 6, "R": 7, "K": 8, "S": 9}
        self.assertEqual(a.Solution(), expectedSolution)

    def testKnownLetters(self):
        a = Alphametic()
        a.AddSum(initial_value="CEYLON", addition="BLACK", result="KETTLE")
        a.AddKnownLetter("N", 8)
        a.AddKnownLetter("Y", 2)
        expectedSolution = {"A":3, "O":1, "B":9, "T":0, "L":7, "K":6, "E":4, "C":5, "Y":2, "N":8}
        self.assertEqual(a.Solution(), expectedSolution)
