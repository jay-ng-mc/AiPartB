import unittest

from xXminecraftEmperorsXx.algorithm import Algorithm
from xXminecraftEmperorsXx.board import Board


class TestAlgorithm(unittest.TestCase):
    algorithm = Algorithm()
    board_platonic = Board()
    board = board_platonic.get()

    def test_piece_separation(self):
        my_pieces1 = ((1, 2), (2, 1), (3, -1))
        my_pieces2 = ((1, 2), (3, -1))
        self.assertEqual(self.algorithm.piece_separation(my_pieces2), 2)
        self.assertEqual(self.algorithm.piece_separation(my_pieces1), 4)
        pass

    def test_jumps(self):
        my_pieces = ((1, 2), (2, 1), (3, -1))
        for piece in my_pieces:
            self.board[piece] = "r"
        self.assertEqual(self.algorithm.jumps(self.board, my_pieces, "red", enemy_only=False), 4)


    def test_dist_from_enemy(self):
        my_pieces = ((1, 2), (2, 1), (3, -1))
        test_enemies = ((1,0))
        test_enemies2 = ((1,0), (1,1))
        # for piece in my_pieces:
        #     self.board[piece] = "self"
        for piece in test_enemies2:
            self.board[piece] = "enemy"
        distance1 = self.algorithm.dist_from_enemy(self.board, my_pieces)
        distance2 = self.algorithm.dist_from_enemy(self.board, my_pieces, num_enemies=2)

        self.assertEqual(distance1, 1)
        self.assertEqual(distance2, [1,2])


if __name__ == "__main__":
    unittest.main()
