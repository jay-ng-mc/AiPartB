import time

from referee.__main__ import play
from referee.log import StarLog
from referee.game import Chexers, IllegalActionException
from referee.player import PlayerWrapper
from referee.options import PackageSpecAction, get_options
from xXminecraftEmperorsXx.algorithm import Algorithm
from xXminecraftEmperorsXx.player import MinecraftPlayer as Player
from xXminecraftEmperorsXx.Formatting import string_to_tuple
import numpy as np

_FILE_PATH = ".\\xXminecraftEmperorsXx\\weights.txt"

def main():
    GAME_LIMIT = 10
    game_num = 0

    while game_num < GAME_LIMIT:
        file = open(_FILE_PATH, "r")
        weights_tuple = string_to_tuple(file.read())
        weights = np.array(weights_tuple)
        file.close()

        print("# New Game")
        weights = run_game(weights, False)   # True for random board or False for default starting board
        file = open(_FILE_PATH, "w")
        new_weight = np.array2string(weights, separator=',', formatter={'float_kind':lambda x: "%.10f" % x})
        print('# DEBUG weights=', weights, new_weight)
        file.write(new_weight)
        file.close()
        game_num += 1


def run_game(weights, random_board=False):
    # Code copied from __main__() in referee.py
    # Modified to allow for training
    algorithm = Algorithm()
    options = get_options()
    real_reward = {
        "r":0,
        "g":0,
        "b":0
    }

    # Create a star-log for controlling the format of output from within this
    # program
    out = StarLog(level=options.verbosity, star="*")
    out.comment("all messages printed by the referee after this begin with a *")
    out.comment("(any other lines of output must be from your Player classes).")
    out.comment()

    try:
        # Import player classes
        p_R = PlayerWrapper('red player', options.playerR_loc, options, out)
        p_G = PlayerWrapper('green player', options.playerG_loc, options, out)
        p_B = PlayerWrapper('blue player', options.playerB_loc, options, out)

        # Play the game!
        players = [p_R, p_G, p_B]
        play(players, options, out, training=True, random_board=random_board)

        exits = p_R.player.board.exits
        draw = all(exits.values()) < 4

        if not draw:
            items = exits.items()
            winner = max(items, key=lambda score: items[1])[0]
            print("# DEBUG WINNER", winner)
            for color in "rgb":
                real_reward[color] = -1
            real_reward[winner] = 1
        else:
            for color in "rgb":
                real_reward[color] = 0

        # game finished, now we update weights
        assert(len(players) > 0)
        for wrapper in players:
            features = wrapper.player.features
            rewards = wrapper.player.rewards
            print("# DEBUG", features, rewards)
            weights = algorithm.weight_update(weights, features, rewards, real_reward[wrapper.player.color[0]])

        return weights

    # In case the game ends in an abnormal way, print a clean error
    # message for the user (rather than a trace).
    except KeyboardInterrupt:
        print()  # (end the line)
        out.comment("bye!")
    except IllegalActionException as e:
        out.section("game error")
        out.print("error: invalid action!")
        out.comment(e)

#
# class Options:
#     def __init__(self):
#         self.logfile = None
#         self.verbosity = 2
#         self.delay = 0
#         self.train = 1
#         self.time = 60.0
#         self.space = 100.0


if __name__ == "__main__":
    main()
