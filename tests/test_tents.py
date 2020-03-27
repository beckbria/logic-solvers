from .context import solvers
from solvers import Tents
import unittest

class TentsTest(unittest.TestCase):
    """Tests for the Keen solver"""

    def test8x8(self):
        # Create a 5x5 puzzle
        t = Tents([
            [True, False, False, False, False, False, True, False],
            [False, True, False, False, False, True, True, False],
            [False, False, False, True, False, False, False, False],
            [False, False, False, False, False, True, False, False],
            [False, False, True, False, False, False, False, False],
            [True, False, False, False, False, False, False, True],
            [False, True, False, False, False, False, False, False],
            [False, False, False, False, True, False, False, False]],
            [2,2,1,1,2,1,1,2],
            [2,1,2,1,3,1,2,0])

        TREE = Tents.TREE
        TENT = Tents.TENT
        EMPTY = Tents.EMPTY

        expectedSolution = [
            [TREE, TENT, EMPTY, EMPTY, EMPTY, EMPTY, TREE, TENT],
            [EMPTY, TREE, EMPTY, EMPTY, TENT, TREE, TREE, EMPTY],
            [EMPTY, TENT, EMPTY, TREE, EMPTY, EMPTY, TENT, EMPTY],
            [EMPTY, EMPTY, EMPTY, TENT, EMPTY, TREE, EMPTY, EMPTY],
            [TENT, EMPTY, TREE, EMPTY, EMPTY, TENT, EMPTY, TENT],
            [TREE, EMPTY, TENT, EMPTY, EMPTY, EMPTY, EMPTY, TREE],
            [TENT, TREE, EMPTY, EMPTY, TENT, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, TREE, EMPTY, EMPTY, EMPTY]]
        self.assertEqual(t.Solution(), expectedSolution)

if __name__ == '__main__':
    unittest.main()