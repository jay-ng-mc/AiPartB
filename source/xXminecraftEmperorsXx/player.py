from xXminecraftEmperorsXx.board import Board
from xXminecraftEmperorsXx.algorithm import Algorithm

import queue
import time
import operator

q, r, s = 0, 1, 2   # axes
_GOALS = {
    "r":(q,3),
    "g":(r,3),
    "b":(s,3)
}
_NEXT_TURN = {
    "r":"g",
    "g":"b",
    "b":"r"
}
_TURN_ID = {
    "r":0,
    "g":1,
    "b":2
}
_LIMIT = 4


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

        next_move = self.max_n()

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

    def max_n(self):
        # real_board = self.board.get()
        projected_board = self.board.copy()           # projected board to play around with

        tree = self.build_tree(projected_board)
        current = tree

        children = current.children
        moves, utilities = [], []
        for child in children:
            snap = child.snapshot
            utility = self.back_utility(child)
            moves.append(snap)
            utilities.append(utility)
        max_utility = max(utilities)
        index = utilities.index(max_utility)
        move = moves[index]

        return move

    def back_utility(self, current):
        assert(current is not None)
        assert(len(current.children) > 0)
        color = current.turn
        util_pos = _TURN_ID[color]
        children = current.children
        utilities = []
        for child in children:
            if child.utility is None:
                utility = self.back_utility(child)
            else:
                utility = child.utility[util_pos]
            utilities.append(utility)
        return max(utilities)

    def build_tree(self, root_board):
        DEPTH_LIMIT = 2
        snapshot = self.snapshot(root_board)
        root = Tree(snapshot=snapshot, level=0, parent=None, turn=self.color[0])
        fringe_nodes = queue.Queue()
        fringe_nodes.put(root)

        while not fringe_nodes.empty():
            node = fringe_nodes.get()
            level = node.level
            if level < DEPTH_LIMIT:
                children = self.node_expander(node)
                node.add_children(children)
                for child in children:
                    fringe_nodes.put(child)
            else:
                board = self.unsnap(node.snapshot)
                node.utility = self.calculate_utilities(board, node.snapshot)

        return root

    def node_expander(self, node):
        # generates children of node
        unit_moves = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]  # unit vectors of a piece's possible moves
        possible_moves = []  # list of a piece's possible moves
        valid_moves = []  # list of all possible moves for this turn, minus ones that are not legal
        children = []

        board = self.unsnap(node.snapshot)
        my_pieces = tuple(piece for (piece, color) in board.items() if color == node.turn)

        for piece in my_pieces:
            possible_moves.clear()

            # add option to leave board
            if piece in self.goal_hexes:
                valid_moves.append(("EXIT", piece, None, None))
                continue

            for unit_move in unit_moves:
                new_pos = tuple(map(operator.add, piece, unit_move))  # new_pos is a place the piece can move to
                (q, r) = new_pos

                jump_target = None
                action_type = "MOVE"
                # check if any piece on there
                if new_pos in board and board[new_pos] != "":
                    jump_target = new_pos
                    action_type = "JUMP"
                    new_pos = tuple(map(operator.add, new_pos, unit_move))  # move again = jump over piece
                    (q, r) = new_pos

                if new_pos in board and board[new_pos] != "":
                    # if location to jump to isn't free, cannot jump
                    continue

                # skip move if it puts piece out of board
                if max(abs(q), abs(r), abs(-q-r)) > self.board.radius():
                    continue

                valid_moves.append((action_type, piece, new_pos, jump_target))

            if len(valid_moves) == 0:
                valid_moves.append(("PASS", None, None, None))

            for move in valid_moves:
                next_board = self.next_board(board, move)
                snapshot = self.snapshot(next_board)
                child = Tree(snapshot, level=node.level+1, parent=node, turn=_NEXT_TURN[node.turn])
                children.append(child)

        print("DEBUG children=", children)

        return children

    def next_board(self, board, move):
        action_type, piece, new_pos, jump_target = move[0], move[1], move[2], move[3]
        next_board = {}
        next_board.update(board)

        color = next_board[piece]
        next_board[piece] = ""
        if action_type in ["MOVE", "JUMP"]:
            next_board[new_pos] = color
            if jump_target is not None:
                next_board[jump_target] = color

        return next_board

    def calculate_utilities(self, board, player_pieces):
        algorithm = Algorithm()
        # red_pieces = tuple([key for key in board.keys() if board[key] == "r"])
        # green_pieces = tuple([key for key in board.keys() if board[key] == "g"])
        # blue_pieces = tuple([key for key in board.keys() if board[key] == "b"])
        red_pieces = player_pieces["r"]
        green_pieces = player_pieces["g"]
        blue_pieces = player_pieces["b"]
        util_red = algorithm.eval(board, "r", red_pieces, _GOALS["r"])
        util_green = algorithm.eval(board, "g", green_pieces, _GOALS["g"])
        util_blue = algorithm.eval(board, "b", blue_pieces, _GOALS["b"])

        utilities = (util_red, util_green, util_blue)
        return utilities

    def snapshot(self, board):
        red_pieces = tuple(piece for piece, color in board.items() if color == "r")
        green_pieces = tuple(piece for piece, color in board.items() if color == "g")
        blue_pieces = tuple(piece for piece, color in board.items() if color == "b")
        player_pieces = {
            "r": red_pieces,
            "g": green_pieces,
            "b": blue_pieces
        }
        return player_pieces

    def unsnap(self, snapshot):
        board = {}
        coord_range = range(-Board.RADIUS, Board.RADIUS + 1)
        for coord in [(q, r) for q in coord_range for r in coord_range if -q - r in coord_range]:
            board[coord] = ""

        for color in "rgb":
            pieces = snapshot[color]
            for piece in pieces:
                board[piece] = color

        return board

    def main(self):
        self.__init__("red")
        self.action()

    # def node_limit(self, current, limit):
    #     if current <= limit:
    #         return True
    #     else:
    #         return False
    #
    #
    # def time_limit(self, start_time, limit):
    #     if (time.time() - start_time) >= limit:
    #         print("# Time Elapsed: ", time.time()-start_time)
    #         return False
    #     else:
    #         return True

    # def path_finder(self, board, player_pieces):
    #     # player_pieces : Dictionary
    #     utilities = (0, 0, 0)           # player utilities
    #     fringe_nodes = queue.Queue()    # nodes that are adjacent to explored nodes, ordered by f(n)
    #     fringe_nodes.put((utilities, player_pieces, "root"))
    #     # add root node to fringe to be expanded, root is current state
    #
    #     node_count = 0  # keep track of node resource
    #     start_time = time.time()  # keep track of time resource
    #     goal_reached = False
    #     # min_f = [None, None]
    #
    #     tree_node = self.tree
    #     turn = self.color[0]
    #     next_board = board
    #     while tree_node.level < _LIMIT:
    #         self.node_expander(tree_node, next_board, turn)
    #         turn = _NEXT_TURN[turn]
    #
    #         # queue chooses next tree node to explore
    #         for child in tree_node.children:
    #             fringe_nodes.put(child)
    #         tree_node = fringe_nodes.get()
    #
    #     fringe_nodes.put("end")         # needed for loop logic to work
    #
    #     # now tree node level is equal to limit, this is the leaf layer of minimax
    #     while not fringe_nodes.empty():
    #         self.node_expander(tree_node, board, turn, calc_util=True)
    #         node = fringe_nodes.get()
    #
    #
    # def node_expander_temp(self, node, board, turn_color, calc_util=False):
    #     unit_moves = [(1,-1), (1,0), (0,1), (-1,1), (-1,0), (0,-1)]     # unit vectors of a piece's possible moves
    #     possible_moves = []                                                 # list of a piece's possible moves
    #     valid_moves = []                       # list of all possible moves for this turn, minus ones that are not legal
    #     next_board = {}
    #
    #     state = node.state
    #     my_pieces = state[self.color]
    #     for piece in my_pieces:
    #         possible_moves.clear()
    #
    #         # add option to leave board
    #         if piece in self.goal_hexes:
    #             valid_moves.append((piece, None))
    #             continue
    #
    #         for unit_move in unit_moves:
    #             new_pos = tuple(map(operator.add, piece, unit_move))  # new_pos is a place the piece can move to
    #             (q, r) = new_pos
    #
    #             # check if any piece on there
    #             jump_target = None
    #             if new_pos in board and board[new_pos] != "":
    #                 if board[new_pos] != self.color[0]:
    #                     jump_target = new_pos
    #                 new_pos = tuple(map(operator.add, new_pos, unit_move))  # move again = jump over piece
    #                 (q, r) = new_pos
    #
    #             if new_pos in board and board[new_pos] != "":
    #                 # if location to jump to isn't free, cannot jump
    #                 continue
    #
    #             # skip move if it puts piece out of board
    #             if max(abs(q), abs(r), abs(-q-r)) > self.board.radius():
    #                 continue
    #
    #             valid_moves.append((piece, new_pos, jump_target))
    #
    #     # explore successors of current node, iterate through valid moves
    #     for choice in valid_moves:
    #         # choice[0] is original position of piece, index is index of piece in node tuple
    #         index = my_pieces.index(choice[0])
    #         # if piece not leaving board
    #         if choice[1] is None:
    #             # exit the board
    #             # choice[1] is new position of the piece, next_node is the new state
    #             next_my_pieces = my_pieces[:index] + my_pieces[index + 1:]
    #         elif choice[2] is None:
    #             # no jump, simple move
    #             # choice[2] is jump_target
    #             next_my_pieces = my_pieces[:index] + (choice[1],) + my_pieces[index + 1:]
    #         else:
    #             # remove piece from conquered player
    #             # jump over an enemy piece, add it to my pieces
    #             conquered_piece_color = board[choice[2]]
    #             their_pieces = state[conquered_piece_color]
    #             cpc_index = their_pieces.index(choice[2])
    #             state[conquered_piece_color] = their_pieces[:cpc_index] + their_pieces[cpc_index + 1:]
    #             next_my_pieces = my_pieces[:index] + (choice[1],) + my_pieces[index + 1:] + choice[2]
    #
    #         state[self.color] = next_my_pieces
    #
    #         next_node = Tree(level=node.level+1, parent=node, state=state, turn=_NEXT_TURN[turn_color])
    #
    #         if calc_util:
    #             # store node utility. super unclean, refactor this
    #             for color in "rgb":
    #                 pieces = state[color]
    #                 for piece in pieces:
    #                     next_board[piece] = color
    #             next_node.utility = self.calculate_utilities(next_board, state)
    #
    #         node.add_child(next_node)


class Tree:
    # Generic tree node
    def __init__(self, snapshot, level, parent, turn, utility=None, children=None):
        self.snapshot = snapshot
        self.level = level
        self.parent = parent
        self.turn = turn
        self.utility = utility
        self.children = []
        if children is not None:
            for child in children:
                self.children.append(child)

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        for child in children:
            self.children.append(child)


if __name__ == "__main__":
    player = MinecraftPlayer("red")
    player.main()
