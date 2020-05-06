from .context import solvers
from solvers import Magnets
import unittest


class MagnetsTest(unittest.TestCase):
    """Tests for the Keen solver"""

    def test6x5(self):
        # Create a 5x5 puzzle
        m = Magnets([3, None, None, None, 1], [None, None, None, 0, None],
                    [2, 2, None, None, 1, None], [None, 2, None, None, 2, None])
        m.AddPair((0, 0), (1, 0))
        m.AddPair((3, 0), (4, 0))
        m.AddPair((3, 1), (4, 1))
        m.AddPair((2, 2), (3, 2))
        m.AddPair((2, 3), (3, 3))
        m.AddPair((2, 4), (3, 4))
        m.AddPair((0, 5), (1, 5))
        m.AddPair((2, 5), (3, 5))
        m.AddPair((2, 0), (2, 1))
        m.AddPair((0, 1), (0, 2))
        m.AddPair((1, 1), (1, 2))
        m.AddPair((0, 3), (0, 4))
        m.AddPair((1, 3), (1, 4))
        m.AddPair((4, 2), (4, 3))
        m.AddPair((4, 4), (4, 5))

        expectedSolution = [
            [1, 2, 1, 0, 0],
            [0, 1, 2, 1, 2],
            [0, 2, 0, 0, 1],
            [1, 0, 0, 0, 2],
            [2, 0, 2, 1, 0],
            [1, 2, 0, 0, 0],
        ]
        self.assertEqual(m.Solution(), expectedSolution)


if __name__ == '__main__':
    unittest.main()
