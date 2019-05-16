from xXminecraftEmperorsXx.board import Board
from xXminecraftEmperorsXx.algorithm import Algorithm

"""
Todo:


"""

import queue
import time
import operator

q, r, s = 0, 1, 2   # axes
_GOALS = {
    "r":(q,3),
    "g":(r,3),
    "b":(s,3)
}


class MinecraftPlayer:

    # fringe_nodes = queue.PriorityQueue()

    def __init__(self, color):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter color will be a string representing the player your
        program will play as (Red, Green or Blue). The value will be one of the 
        strings "red", "green", or "blue" correspondingly.
        """
        # TODO: Set up state representation.

        self.board = Board()
        self.color = color
        self.goal = _GOALS[color[0]]  # axis, value version of goal
        self.goal_hexes = self.board.get_goal(color)
        self.my_pieces = tuple(Board.get_start(self.color))
        self.explored_states = {}   # set of explored states in form of tuple holding pieces

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the node_count state of the game, your player should select and
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        """
        # TODO: Decide what action to take.

        next_move = self.path_finder(
            self.board.get(),
            self.my_pieces
        )[1]

        # modify to match output format
        print(next_move)
        return next_move

    def update(self, color, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter color will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red",
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action
        (or pass) for the player color (your method does not need to validate
        the action/pass against the game rules).
        """
        # TODO: Update state representation in response to action.

        self.board.update(color, action)

    # uses A* search
    def path_finder(self, board, my_pieces):
        utilities = (0, 0, 0)           # player utilities
        fringe_nodes = queue.Queue()    # nodes that are adjacent to explored nodes, ordered by f(n)
        fringe_nodes.put((utilities, my_pieces, "root"))
        # add root node to fringe to be expanded, root is current state

        node_count = 0  # keep track of node resource
        start_time = time.time()  # keep track of time resource
        goal_reached = False
        # min_f = [None, None]

        while self.time_limit(start_time, limit=5) is True:
            # while node_limit(node_count, limit=50) is True:
            # run node_expander i number of times before checking time elapsed
            i = 1000
            while not fringe_nodes.empty() and i > 0 and (goal_reached is False or goal_reached[0] < min_f[0]):

                goal_reached = self.node_expander(board, fringe_nodes, min_f)

                if goal_reached is not False:
                    print("# Path found")
                    node = goal_reached[1]

                i -= 1
            node_count += 1

        # if goal not found, must have reached resource limit
        if goal_reached is False:
            print("# Resource limit")
            node = min_f[1]

        path = []
        while node != "root":
            path.append(node)
            node = self.explored_states[node]
        path.reverse()

        return path

    def node_expander(self, board, fringe_nodes):
        # returns the cheapest fringe state that matches goal
        # returns False if no goal-matching state is found
        # "cheats" by using (if h(n)==0) to determine if next_state matches goal, saves having to expand the next_state

        # node is the current state of your pieces on the board, index 1 removes priority value
        node = fringe_nodes.get()                                   # node contains utilities, state, and prev_state
        utilities = node[0]                                         # utility for each player (normalized)
        state = node[1]                                             # state = tuple of piece coordinates
        prev_state = node[2]

        # if already explored, discard node
        if state in self.explored_states:
            return False

        # add state to explored states
        if prev_state is None:
            self.explored_states[state] = "root"
        else:
            self.explored_states[state] = prev_state

        unit_moves = [(1,-1), (1,0), (0,1), (-1,1), (-1,0), (0,-1)]     # unit vectors of a piece's possible moves
        possible_moves = []                                                 # list of a piece's possible moves
        valid_moves = []                        # list of all possible moves for this turn, minus ones that are not legal

        for piece in state:
            possible_moves.clear()

            # add option to leave board
            if piece in self.goal_hexes:
                valid_moves.append((piece, None))
                continue

            for unit_move in unit_moves:
                new_pos = tuple(map(operator.add, piece, unit_move))  # new_pos is a place the piece can move to
                (q, r) = new_pos

                # check if any piece on there (since beginning of the turn or in the simulation)
                if new_pos in board or new_pos in state:
                    new_pos = tuple(map(operator.add, new_pos, unit_move))  # move again = jump over piece
                    (q, r) = new_pos

                if new_pos in board or new_pos in state:
                    continue

                # skip move if it puts piece out of board
                if max(abs(q), abs(r), abs(-q-r)) > self.board.radius():
                    continue

                valid_moves.append((piece, new_pos))

        # explore successors of current node, iterate through valid moves
        for choice in valid_moves:
            # choice[0] is original position of piece, index is index of piece in node tuple
            index = state.index(choice[0])
            # if piece not leaving board
            if choice[1] is not None:
                # choice[1] is new position of the piece, next_node is the new state
                next_state = state[:index] + (choice[1],) + state[index+1:]
            else:
                next_state = state[:index] + state[index+1:]

            if next_state not in self.explored_states:
                utilities = self.calculate_utilities(board)
                fringe_nodes.put((utilities, next_state, state))
            else:
                pass

        # goal has not been found
        return False

    def calculate_utilities(self, board):
        algorithm = Algorithm()
        red_pieces = tuple([key for key in board.keys() if board[key] == "r"])
        green_pieces = tuple([key for key in board.keys() if board[key] == "g"])
        blue_pieces = tuple([key for key in board.keys() if board[key] == "b"])
        util_red = algorithm.eval(board, "r", red_pieces, _GOALS["r"])
        util_green = algorithm.eval(board, "g", green_pieces, _GOALS["g"])
        util_blue = algorithm.eval(board, "b", blue_pieces, _GOALS["b"])

        utilities = (util_red, util_green, util_blue)
        return utilities

    def node_limit(self, current, limit):
        if current <= limit:
            return True
        else:
            return False


    def time_limit(self, start_time, limit):
        if (time.time() - start_time) >= limit:
            print("# Time Elapsed: ", time.time()-start_time)
            return False
        else:
            return True

    def main(self):
        self.__init__("red")
        self.action()


if __name__ == "__main__":
    player = MinecraftPlayer("red")
    player.main()
