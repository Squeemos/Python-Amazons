from board import AmazonsBoard
from player import Player
from move import Move

import time
import numpy as np

def play_game(board_size, player_1, player_2, **kwargs):
    b = AmazonsBoard(board_size, starting_positions = kwargs.get("starting_positions"))
    p = Player(1)
    q = Player(2)

    print_board = kwargs.get("print_board", False)

    if print_board is not False:
        print(b, "\n")

    while not b.done:
        match player_1:
            case "Random":
                p.make_random_move(b, print_move = kwargs.get("print_move"))
            case "Human":
                p.prompt_human_move(b)
            case "Min":
                p.make_min_opponent_move(b, print_move = kwargs.get("print_move"))
            case "Max":
                p.make_max_self_move(b, print_move = kwargs.get("print_move"))
            case "MinMax":
                p.make_minmax_move(b, print_move = kwargs.get("print_move"))
            case "MCTS":
                p.make_mcts_move(b, kwargs.get("n_mcts_games"), print_move = kwargs.get("print_move"), mode = kwargs.get("mcts_mode"))
            case other:
                print(f"Some other case tried: {other}")
                break
        if print_board is not False:
            print(b, "\n")
        if b.done:
            break

        match player_2:
            case "Random":
                q.make_random_move(b, print_move = kwargs.get("print_move"))
            case "Human":
                q.prompt_human_move(b)
            case "Min":
                q.make_min_opponent_move(b, print_move = kwargs.get("print_move"))
            case "Max":
                q.make_max_self_move(b, print_move = kwargs.get("print_move"))
            case "MinMax":
                q.make_minmax_move(b, print_move = kwargs.get("print_move"))
            case other:
                print(f"Some other case tried: {other}")
                break
        if print_board is not False:
            print(b, "\n")
        if b.done:
            break
    if kwargs.get("print_end", False) is not False:
        print(f"Player {b.winner} won! Game took {len(b.moves)} turns.")

    return b.winner, len(b.moves)


def main():
    size = 4
    n_games = 1

    games = [play_game(size,
        player_1 = "MCTS",
        player_2 = "Min",
        print_move = False,
        print_end = True,
        n_mcts_games = 100,
        mcts_mode = "minmax",
        print_board = True,
        )
    for _ in range(n_games)]

    winners = {1 : 0, 2 : 0}
    lengths = {1 : [], 2 : []}
    for winner, length in games:
        winners[winner] += 1
        lengths[winner].append(length)

    for key in lengths:
        lengths[key] = np.mean(lengths[key])

    print(winners)
    print(lengths)

    return 0

if __name__ == '__main__':
    SystemExit(main())
