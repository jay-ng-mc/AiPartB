
import queue
import math
import operator
import time
import itertools

from xXminecraftEmperorsXx import Formatting


class Algorithm:

    # specify axes names of the three values in coordinates tuple passed to heuristic()
    q,r,s = 0,1,2
    board_radius = 3


    board = {}
    explored_states = {}                        # key: coordinate tuple
    fringe_nodes = queue.PriorityQueue()        # nodes that are adjacent to explored nodes, ordered by f(n)
    min_f = [None, None]                        # node with minimum f(n). min_f[0] holds f(n) value, min_f[1] holds state

    matrix_size = board_radius * 2 + 1
    board_matrix = [[None for x in range(matrix_size)] for y in range(matrix_size)]


    # main used to debug algorithm.py, not called in actual use
    # def main():
    #     global board, board_matrix, explored_states, fringe_nodes
    #     # board key: coordinate tuple, data: piece color
    #     board_input = {"(-3, 0, 3)":"r", "(-3, 1, 2)":"r", "(-3, 2, 1)":"r", "(-3, 3, 0)":"r"}
    #     # board_input = {"(0, 0, 0)": "r", "(0, 1, -1)": "r", "(0, 2, -2)": "r", "(0, -1, 1)": "r"}
    #     # board_input = {(-3, 0, 3): "r", (-3, 1, 2): "r", (-3, 2, 1): "r", (-3, 3, 0): "r", (-2, -1, 3): "block", (-2, 0, 2): "block", (-2, 1, 1): "block"}
    #     # board_input = {"(-3, 0, 3)":"r"}
    #     # board_input = {"(-3, 0, 3)": "r", "(-3, 1, 2)": "r", "(-2, -1, 3)": "block"}
    #     # board_input = {"(-3, 0, 3)": "r", "(-2, 0, 2)": "r", "(-2, -1, 3)": "block"}
    #     board.update(board_input)
    #
    #     # converting board to matrix allows for more efficient code (can access by axes)
    #     board_matrix = dict_to_matrix(board)
    #
    #     global q, r, s
    #     # h = heuristic(((0,0,0),(-1,0,3)), (q,-3))
    #     # print("h(n) = ", h)
    #
    #     goal = (q,3)
    #
    #     fringe_nodes.put((0, 0, ((-3, 0, 3), (-3, 1, 2), (-3, 2, 1), (-3, 3, 0)), None))
    #     # fringe_nodes.put((0, 0, ((0, 0, 0), (0, 1, -1), (0, 2, -2), (0, -1, 1)), None))
    #     # fringe_nodes.put((0, 0, ((-3, 0, 3), (-3, 1, 2)), None))
    #     # fringe_nodes.put((0, 0, ((-3, 0, 3), (-2, 0, 2)), None))
    #     # fringe_nodes.put((3, 0, ((-3, 0, 3),), None))
    #
    #
    #     start_time = time.time()
    #
    #     # path = path_finder(goal)
    #     # print("# Path: ", path)
    #
    #     # simulated get_next_move input
    #     get_next_move({"(-3, 0, 3)":"r", "(-3, 1, 2)":"r", "(-3, 2, 1)":"r", "(-3, 3, 0)":"r",
    #                    "(-2, -1, 3)": "block", "(-2, 0, 2)": "block", "(-2, 1, 1)": "block",
    #                    "(-1, -1, 2)": "block", "(-1, 0, 1)": "block", "(-1, 1, 0)": "block"},
    #                   ((-3, 0, 3), (-3, 1, 2), (-3, 2, 1), (-3, 3, 0)),
    #                   (q, 3))
    #
    #     end_time = time.time()
    #
    #     print("# Time taken: ", end_time - start_time)
    #
    #     return None


    def get_next_move(board_input, my_pieces, goal):
        global board, board_matrix, explored_states, fringe_nodes
        board = board_input
        board_matrix = dict_to_matrix(board)
        fringe_nodes.put((0, 0, my_pieces, None))
        path = path_finder(goal)
        print("# Next Move: ", path[1])

        return path[1]


    # coords is a list of 1 to 4 coordinate tuples of pieces
    #   coordinate tuple includes 3 axes i.e. q,r,s where s is derived from -q-r
    # goal is single tuple consisting of 2 elements: axis (i.e. q,r,s) and value (i.e. -3,3)
    def heuristic(coords, goal):
        global board_matrix, q, r, s
        axes = [q, r, s]
        num_pieces = len(coords)
        # num_pairs = (num_pieces * (num_pieces-1))/2
        combinations = []       # combinations of pairs of pieces
        sum_separations = []    # sum of separations of pairs of pieces
        odd_piece = []          # unpaired piece in situations where there are odd number of pieces
        piece_distances = []      # sum of shortest distances between pieces and their goal
        # blocks_goal_axis_coords = []
        # block_discount = []
        # num_jumps_array = []
        # num_jumps = 0
        goal_axis = goal[0]     # axis perpendicular to the side our pieces have to move to
        goal_value = goal[1]    # either -n or n, where n is the radius of the hexagonal board
        #   distinguishes between the two sides perpendicular to the goal_axis

        for coord in coords:
            piece_distance = abs(coord[goal_axis] - goal_value)   # position of piece of goal_axis
            piece_distances.append(piece_distance)

        total_distance = sum(piece_distances)

        # keep track of steps between pieces
        piece_separation = [[None for i in range(num_pieces)] for j in range(num_pieces)]

        piece_pairs = []

        # since we want to move toward one axis (increase or decrease axis value), other two axes must be inversely affected
        axes.remove(goal_axis)
        # p1 and p2 are pieces
        for p1 in range(len(coords)):
            for p2 in range(p1+1, len(coords)):
                piece_pairs.append([p1, p2])

                y_dist = abs(coords[p1][axes[0]] - coords[p2][axes[0]])
                z_dist = abs(coords[p1][axes[1]] - coords[p2][axes[1]])
                # -1 because one piece reaches cross, the other piece sits behind it (from the goal)
                piece_separation[p1][p2] = y_dist + z_dist - 1

        # brittle, only applies to < 4 pieces
        for i in range(len(piece_pairs)):
            for j in range(i, len(piece_pairs)):
                pieces = [piece_pairs[i][0], piece_pairs[i][1], piece_pairs[j][0], piece_pairs[j][1]]
                # no duplicates
                if len(pieces) == len(set(pieces)):
                    combinations.append([piece_pairs[i], piece_pairs[j]])

        if len(combinations) == 0:
            for i in range(len(piece_pairs)):
                combinations.append([piece_pairs[i]])
                for x in range(num_pieces):
                    if x not in set(tuple(itertools.chain.from_iterable(combinations[i]))):
                        odd_piece.append(coords[x])

        # future implementation
        # for piece_pair in piece_pairs:
        #     (p1, p2) = piece_pair
        #     intersection_x = min([coords[p1][axes[0]], coords[p2][axes[0]]], key=lambda x: abs(-goal_value - x))
        #     intersection_y = min([coords[p1][axes[1]], coords[p2][axes[1]]], key=lambda x: abs(-goal_value - x))
        #     intersection_goal_axis_val = - intersection_x - intersection_y
            # num_jumps_array.append(abs(goal_value - intersection_goal_axis_val))

        # future implementation of estimation for jumping for odd pieces. currently assume odd pieces can always jump
        # jumps = []
        # for odd in odd_piece:
        #     piece_distance = abs(odd[goal_axis] - goal_value)
        #     jumps.append(math.floor(piece_distance / 2))
        # if len(jumps) > 0:
        #     num_jumps_array = list(map(operator.add, num_jumps_array, jumps))

        for i in range(len(combinations)):
            sum_separation = 0
            for j in range(len(combinations[i])):
                p1 = combinations[i][j][0]
                p2 = combinations[i][j][1]

                separation = piece_separation[p1][p2]
                sum_separation += separation
            sum_separations.append(sum_separation)

        if len(sum_separations) > 0:
            minsum_separation = min(sum_separations)
        else:
            minsum_separation = 0

        # some code for future implementation of num_jumps
        # for i in range(len(sum_separations)):
        #     if minsum_separation is None or sum_separations[i] < minsum_separation:
        #         minsum_separation = sum_separations[i]
        #         num_jumps = minsum_separation + num_jumps_array[i]

        # h = total_distance + num_pieces - num_jumps

        # modifier on heuristic value "h(n)"
        h = math.ceil(total_distance/2) + minsum_separation + num_pieces

        return h


    def node_expander(goal):
        # returns the cheapest fringe state that matches goal
        # returns False if no goal-matching state is found
        # "cheats" by using (if h(n)==0) to determine if next_state matches goal, saves having to expand the next_state

        global board_radius
        global board, explored_states, fringe_nodes
        global min_f

        # node is the current state of your pieces on the board, index 1 removes priority value
        node = fringe_nodes.get()                                           # node contains f, g, and state
        g = node[1]                                                         # g = cost of reaching state
        state = node[2]                                                     # state = tuple of piece coordinates
        prev_state = node[3]

        goal_axis = goal[0]     # axis perpendicular to the side our pieces have to move to
        goal_value = goal[1]    # either -n or n, where n is the radius of the hexagonal board

        # stringification needed because strings are always identical if equivalent, tuples are not
        stringified_state = Formatting.tuple_to_string(state)

        # if already explored, discard node
        if stringified_state in explored_states:
            return False

        # add state to explored states
        if prev_state is None:
            explored_states[stringified_state] = "root"
        else:
            stringified_prev = Formatting.tuple_to_string(prev_state)
            explored_states[stringified_state] = stringified_prev

        unit_moves = [(1,-1,0),(1,0,-1),(0,1,-1),(-1,1,0),(-1,0,1),(0,-1,1)]     # unit vectors of a piece's possible moves
        possible_moves = []                                                 # list of a piece's possible moves
        valid_moves = []                        # list of all possible moves for this turn, minus ones that are not legal

        for piece in state:
            possible_moves.clear()

            # add option to leave board
            if piece[goal_axis] == goal_value:
                valid_moves.append((piece, None))
                continue

            for unit_move in unit_moves:
                new_pos = tuple(map(operator.add, piece, unit_move))  # new_pos is a place the piece can move to
                (q, r, s) = new_pos
                stringified_new_pos = Formatting.tuple_to_string(new_pos)

                # check if any piece on there (since beginning of the turn or in the simulation)
                if stringified_new_pos in board or new_pos in state:
                    new_pos = tuple(map(operator.add, new_pos, unit_move))  # move again = jump over piece
                    (q, r, s) = new_pos
                    stringified_new_pos = Formatting.tuple_to_string(new_pos)

                if stringified_new_pos in board or new_pos in state:
                    continue

                # skip move if it puts piece out of board
                if max(abs(q), abs(r), abs(s)) > board_radius:
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

            stringified_next = Formatting.tuple_to_string(next_state)
            if stringified_next not in explored_states:
                h = heuristic(coords=next_state, goal=goal)

                if h == 0:
                    explored_states[stringified_next] = Formatting.tuple_to_string(state)
                    # goal has been found
                    return (g + 1, next_state)

                # f is estimated total path cost, h is predicted cost of remaining path, g is current path cost
                f = h + g

                fringe_nodes.put((f, g + 1, next_state, state))

                if min_f[0] is None or f <= min_f[0]:
                    min_f[0] = f
                    min_f[1] = next_state

            else:
                pass

        # goal has not been found
        return False


    def path_finder(goal):
        current = 0                         # keep track of node resource
        start_time = time.time()            # keep track of time resource

        path_found = False
        while time_limit(start_time, limit=25) is True:
        # while node_limit(current, limit=50) is True:
            # run node_expander i number of times before checking time elapsed
            i = 1000
            while not fringe_nodes.empty() and i > 0 and (path_found is False or path_found[0] < min_f[0]):

                path_found = node_expander(goal)

                if path_found is not False:
                    print("# Path found")
                    node = Formatting.tuple_to_string(path_found[1])

                i -= 1
            current += 1

        # if goal not found, must have reached resource limit
        if path_found is False:
            print("# Resource limit")
            node = Formatting.tuple_to_string(min_f[1])

        path = []
        while node != "root":
            path.append(node)
            node = explored_states[node]
        path.reverse()

        return path


    def dict_to_matrix(board):
        size = board_radius * 2 + 1
        # board_matrix = [size][size]
        keys = board.keys()

        for key in keys:
            coord = Formatting.string_to_tuple(key)
            q, r, s = coord

            board_matrix[q][r] = board[key]

        return board_matrix


    def node_limit(current, limit):
        if current <= limit:
            return True
        else:
            return False


    def time_limit(start_time, limit):
        if (time.time() - start_time) >= limit:
            print("# Time Elapsed: ", time.time()-start_time)
            return False
        else:
            return True