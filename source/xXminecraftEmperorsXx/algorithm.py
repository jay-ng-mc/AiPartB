import queue
import math
import operator
import time
import itertools
import numpy as np

from xXminecraftEmperorsXx import Formatting

_FILE_PATH = ".\\source\\xXminecraftEmperorsXx\\weights.txt"


class Algorithm:

    def __init__(self):
        file = open(_FILE_PATH, "r")
        self.weights = Formatting.string_to_tuple(file.read())

    def weight_update(self, test):
        pass

    def evaltemp(self, board, player_color, my_pieces, goal):
        distance = 0
        for piece in my_pieces:
            distance += (tuple(goal)[0][0] - piece[0])
        return distance

    def eval(self, board, player_color, my_pieces, goal):
        # Returns a float value in range (0,1) to indicate the goodness of the current board state for the player
        # board : Dictionary
        # my_pieces : tuple
        # goal : tuple
        pass

    def features(self, board, player_color, my_pieces, goal):
        # Returns a numpy vector that contains the features of the current board state
        # board : Dictionary
        # my_pieces : tuple
        # goal : tuple
        features = []

        f1 = len(my_pieces)
        f2 = self.piece_separation(my_pieces)
        # f3 = self.dist_intercept(my_pieces)
        f4 = self.dist_to_goal(my_pieces)
        f5 = self.can_take(board, my_pieces)
        f6 = self.can_jump(board, my_pieces)

        f7 = self.dist_from_enemy(board, my_pieces)
        f8 = self.second_dist_from_enemy(board, my_pieces)
        f9 = self.dist_btw_enemy(board)
        f10 = self.dist_btw_enemy(board)

        features_vector = np.array(features)
        return features_vector

    @staticmethod
    def piece_separation(my_pieces):
        # Returns an integer value indicating total separation between all pieces (combinatorial)
        # my_pieces : tuple
        total_separation = 0
        for i in range(0, len(my_pieces)):
            for j in range(i, len(my_pieces)):
                p1 = np.array(my_pieces[i])
                p2 = np.array(my_pieces[j])
                axis_sep_min = min(np.absolute(p1-p2))
                total_separation += axis_sep_min
        return total_separation

    @staticmethod
    def dist_intercept(my_pieces, goal):
        # Returns the integer distance that pairs of pieces have to travel to arrive at an "intercept" point
        # "Intercept" is defined as the hex which has the same value on one of two non-goal axes for both pieces in pair
        # e.g. pair of pieces: (1,2,-3), (-2,0,2); goal: q=3 (q being first axis); intercept: (3,0,-3)
        # my_pieces: tuple
        pass

    # iterative depth first search
    def idfs(self):
        pass
