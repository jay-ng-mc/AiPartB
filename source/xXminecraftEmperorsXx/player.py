from xXminecraftEmperorsXx.board import Board
from xXminecraftEmperorsXx.algorithm import Algorithm

q, r, s = 0, 1, 2   # axes
_GOALS = {
    "r":(q,3),
    "g":(r,3),
    "b":(s,3)
}

class MinecraftPlayer:

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
        self.goal = _GOALS[color[0]]
        self.my_pieces = Board.get_start(color)
        self.explored_states = {}   # set of explored states in form of tuple holding pieces
        self.algorithm = Algorithm()

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        """
        # TODO: Decide what action to take.

        next_move = Algorithm.get_next_move(
            self.board.get(),
            tuple(self.my_pieces),
            self.goal,
            self.explored_states
        )

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
