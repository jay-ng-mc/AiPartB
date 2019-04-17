
import queue
import math
import operator
import time
import itertools

from xXminecraftEmperorsXx import Formatting


class Algorithm:
    fringe_nodes = queue.PriorityQueue()        # nodes that are adjacent to explored nodes, ordered by f(n)

    def init(self, board, my_pieces, goal, explored_states):
        pass

    def get_next_move(self, board, my_pieces, goal, explored_states):
        self.board = board
        self.my_pieces = my_pieces
        self.goal = goal
        self.explored_states = explored_states

    def heuristic(self, board, my_pieces, goal):
        pass

    def node_expander(self):
        pass

    def path_finder(self):
        pass