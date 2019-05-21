import random

_STARTING_HEXES = {
    'r': {(-3,3), (-3,2), (-3,1), (-3,0)},
    'g': {(0,-3), (1,-3), (2,-3), (3,-3)},
    'b': {(3, 0), (2, 1), (1, 2), (0, 3)},
}

# only used by algorithm.py but kept here with starting hexes for cohesion
_GOAL_HEXES = {
    'r': {(3,-3), (3,-2), (3,-1), (3,0)},
    'g': {(-3,3), (-2,3), (-1,3), (0,3)},
    'b': {(-3,0),(-2,-1),(-1,-2),(0,-3)},
}


class Board:
    RADIUS = 3

    def __init__(self):
        self.num_pieces = {
            "r":4,
            "g":4,
            "b":4
        }
        self.exits = {
            "r": 0,
            "g": 0,
            "b": 0
        }

        # initialize blank board
        self.board_dict = {}
        coord_range = range(-Board.RADIUS, Board.RADIUS+1)
        for coord in [(q, r) for q in coord_range for r in coord_range if -q-r in coord_range]:
            self.board_dict[coord] = ""

        # add colored pieces, code taken from referee\game.py
        for color in "rgb":
            for coord in _STARTING_HEXES[color]:
                self.board_dict[coord] = color

    def replace_board(self, board):
        self.board_dict = {}
        self.board_dict.update(board)

    def update(self, color, action):
        aType, aArgs = action

        if aType == "MOVE":
            qr1, qr2 = aArgs
            self.board_dict[qr1] = ""
            self.board_dict[qr2] = color[0]
        elif aType == "JUMP":
            (q1, r1), (q2, r2) = qr1, qr2 = aArgs
            jump_pad = (q1+q2)//2, (r1+r2)//2
            self.board_dict[qr1] = ""
            self.board_dict[qr2] = color[0]
            victim_color = self.board_dict[jump_pad]
            self.board_dict[jump_pad] = color[0]
            self.num_pieces[color[0]] += 1
            self.num_pieces[victim_color[0]] -= 1
        elif aType == "EXIT":
            qr1 = aArgs
            self.board_dict[qr1] = ""
            self.num_pieces[color[0]] -= 1
            self.exits[color[0]] += 1

    def get(self):
        return self.board_dict

    def copy(self):
        projected_board = {}
        projected_board.update(self.board_dict)
        return projected_board

    def radius(self):
        return self.RADIUS

    @staticmethod
    def get_goal(color):
        return _GOAL_HEXES[color[0]]

    @staticmethod
    def get_start():
        player_pieces = {}
        player_pieces.update(_STARTING_HEXES)
        # this makes a new copy of the dictionary to avoid interfering with _STARTING_HEXES
        return player_pieces
    
    @staticmethod
    def get_random_board(empty_char=""):

        num_pieces_on_board = {
            "r":0,
            "g":0,
            "b":0
        }

        random_board = {}
        coord_range = range(-Board.RADIUS, Board.RADIUS+1)
        coord_list = [(q, r) for q in coord_range for r in coord_range if -q-r in coord_range]
        for coord in coord_list:
            random_board[coord] = empty_char

        # generate max number of pieces for each colour
        for key in num_pieces_on_board:
            num_pieces_on_board[key] = random.randint(0, 4 + 1)

        # for each colour, choose a random position on the board. 
        for col in "rgb":
            for _ in range(num_pieces_on_board[col]):
                random_board[random.choice(coord_list)] = col

            # TODO make sure that it's not already taken tho 
        
        # once all pieces are settled, return the board
        return random_board

        



