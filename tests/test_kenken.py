from .context import solvers
from solvers import KenKen
import unittest

class KenKenTest(unittest.TestCase):
    """Tests for the Keen solver"""

    def test5x5(self):
        # Create a 5x5 puzzle
        k = KenKen(5)
        k.AddDivision(2, (0,0), (0,1))
        k.AddDivision(2, (1,2), (1,3))
        k.AddDivision(2, (3,3), (4,3))
        k.AddProduct(12, (1,1), (2,1))
        k.AddProduct(5, (3,2), (4,2))
        k.AddProduct(12, (0,2), (0,3))
        k.AddDifference(3, (1,0), (2,0))
        k.AddDifference(2, (3,0), (3,1))
        k.AddDifference(1, (0,4), (1,4))
        k.AddSum(5, (4,0), (4,1))
        k.AddSum(9, (2,2), (2,3), (2,4))
        k.AddSum(5, (3,4), (4,4))
        expectedSolution = [[1,5,2,3,4],[2,3,4,5,1],[4,2,3,1,5],[3,1,5,4,2],[5,4,1,2,3]]
        self.assertEqual(k.Solution(), expectedSolution)

if __name__ == '__main__':
    unittest.main()
