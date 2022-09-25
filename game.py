from board import AmazonsBoard
from player import Player
from move import Move

import time


def main():
    size = 8
    starting_positions = {
        (0, 1) : 1,
        (0, 3) : 1,
        (4, 1) : 2,
        (4, 3) : 2
    }

    other_starting_positions = {
        (0, 0) : 1,
        (size - 1, size -1) : 2
    }
    #b = AmazonsBoard()
    b = AmazonsBoard(size)
    #b = AmazonsBoard(size, starting_positions = starting_positions)
    #b = AmazonsBoard(size, starting_positions = other_starting_positions)

    p = Player(1)
    q = Player(2)

    print(b,"\n")
    print_move = True

    #player_1 = "Random"
    #player_1 = "Human"
    #player_1 = "Min"
    #player_1 = "Max"
    #player_1 = "MinMax"
    player_1 = "MCTS"

    #player_2 = "Random"
    #player_2 = "Human"
    player_2 = "Min"
    #player_2 = "Max"
    #player_2 = "MinMax"

    while True:
        match player_1:
            case "Random":
                p.make_random_move(b, print_move = print_move)
            case "Human":
                p.prompt_human_move(b)
            case "Min":
                p.make_min_opponent_move(b, print_move = print_move)
            case "Max":
                p.make_max_self_move(b, print_move = print_move)
            case "MinMax":
                p.make_minmax_move(b, print_move = print_move)
            case "MCTS":
                p.make_mcts_move(b, 10, print_move = print_move)
            case other:
                print(f"Some other case tried: {other}")
                break
        print(b, "\n")
        if b.done:
            break

        match player_2:
            case "Random":
                q.make_random_move(b, print_move = print_move)
            case "Human":
                q.prompt_human_move(b)
            case "Min":
                q.make_min_opponent_move(b, print_move = print_move)
            case "Max":
                q.make_max_self_move(b, print_move = print_move)
            case "MinMax":
                q.make_minmax_move(b, print_move = print_move)
            case other:
                print(f"Some other case tried: {other}")
                break
        print(b,"\n")
        if b.done:
            break
    print(f"Player {b.winner} won! Game took {len(b.moves)} turns.")


if __name__ == '__main__':
    main()
