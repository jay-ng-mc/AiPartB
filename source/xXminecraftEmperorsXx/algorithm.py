
import queue
import math
import operator
import time
import itertools
import numpy

from xXminecraftEmperorsXx import Formatting


class Algorithm:

    def __init__(self):
        file = open(".\\source\\xXminecraftEmperorsXx\\weights.txt", "r")
        self.weights = Formatting.string_to_tuple(file.read())

    def weight_update(self, test):
        pass

    def get_next_move(self, board, my_pieces, goal, explored_states):
        self.board = board
        self.my_pieces = my_pieces
        self.goal = goal
        self.explored_states = explored_states

    @staticmethod
    def eval(board, my_pieces, goal):
        distance = 0
        for piece in my_pieces:
            distance += (tuple(goal)[0][0] - piece[0])
        return distance

    def node_expander(self):
        pass

    # iterative depth first search
    def idfs(self):
        pass

