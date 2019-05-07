import unittest
from xXminecraftEmperorsXx.algorithm import Algorithm


class TestAlgorithm(unittest.TestCase):

    def test_piece_separation(self):
        algorithm = Algorithm()
        my_pieces1 = ((1,2),(2,3),(3,-1))
        my_pieces2 = ((1,2),(3,-1))
        self.assertEqual(algorithm.piece_separation(my_pieces2), 2)
        self.assertEqual(algorithm.piece_separation(my_pieces1), 4)
        pass


if __name__ == "__main__":
    unittest.main()
