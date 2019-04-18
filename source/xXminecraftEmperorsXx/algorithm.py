
import queue
import math
import operator
import time
import itertools

from xXminecraftEmperorsXx import Formatting


class Algorithm:
    fringe_nodes = queue.PriorityQueue()        # nodes that are adjacent to explored nodes, ordered by f(n)

    def __init__(self):
        file = open(".\\source\\xXminecraftEmperorsXx\\weights.txt", "r")
        self.weights = Formatting.string_to_tuple(file.read())
        self.board = {}
        self.my_pieces = ()
        self.goal = ()
        self.explored_states = {}
        self.fringe_nodes.empty()

    def get_next_move(self, board, my_pieces, goal, explored_states):
        self.board = board
        self.my_pieces = my_pieces
        self.goal = goal
        self.explored_states = explored_states

    def eval(self, board, my_pieces, goal):
        pass

    def node_expander(self):
        pass

    # iterative depth first search
    def idfs(self):
        pass