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

    board_dict = {}
    num_pieces = {
        "r":4,
        "g":4,
        "b":4
    }

    def init(self):
        # initialize blank board
        self.board_dict = {}
        coord_range = range(-Board.RADIUS, Board.RADIUS+1)
        for coord in [(q, r) for q in coord_range for r in coord_range if -q-r in coord_range]:
            self.board_dict[coord] = ""

        # add colored pieces, code taken from referee\game.py
        for color in "rgb":
            for coord in _STARTING_HEXES[color]:
                self.board_dict[coord] = color

    def update(self, color, action):
        aType, aArgs = action

        if aType == "MOVE":
            qr1, qr2 = aArgs
            self.board_dict[qr1] = ""
            self.board_dict[qr2] = color
        elif aType == "JUMP":
            (q1, r1), (q2, r2) = qr1, qr2 = aArgs
            jump_pad = q1+q2//2, r1+r2//2
            self.board_dict[qr1] = ""
            self.board_dict[qr2] = color
            self.board_dict[jump_pad] = color
        elif aType == "EXIT":
            qr1 = aArgs
            self.board_dict[qr1] = ""
            self.num_pieces[color[0]] -= 1

    def get(self):
        return self.board_dict

    def radius(self):
        return self.RADIUS

    @staticmethod
    def get_goal(color):
        return _GOAL_HEXES[color[0]]

    @staticmethod
    def get_start(color):
        return _STARTING_HEXES[color[0]]


