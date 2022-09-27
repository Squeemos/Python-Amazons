from move import Move
from board import AmazonsBoard

from typing import Optional, Tuple

import random
from copy import deepcopy

class Player(object):
    def __init__(self, id : int):
        assert id in set((1, 2)), "Id Error: Player Id must be either 1 or 2"
        self.__id = id

        self.reset()

    @property
    def id(self):
        return self.__id

    @property
    def moves(self):
        return self.__moves

    def make_move(self, m : Move, b : AmazonsBoard, **kwargs) -> None:
        '''
            How the player interacts with the board
        '''
        m.id = self.id
        b.make_move(m, **kwargs)

    def reset(self) -> None:
        pass

    def make_random_move(self, b : AmazonsBoard, **kwargs) -> None:
        '''
            Generate a random piece to move to a random location, then pick a random place to attack
        '''
        # From all pieces, pick a random starting and ending point (valid ending point no matter the starting point)
        next_move = random.choice(b.populate_all_movements(self.id))
        # From the next move, pick a random place to attack
        next_attack = random.choice(b.populate_all_attacks_for_move(*next_move))
        # Take the random move
        self.make_move(Move(*next_move, next_attack, self.id), b, **kwargs)

    def make_min_opponent_move(self, b : AmazonsBoard, **kwargs) -> None:
        '''
            Calculate the move that leaves the opponent with the least number of moves
        '''
        # Generate all moves we can take
        all_moves = self.generate_all_moves(b)
        move_values = {}
        other_player_id = 2 if self.id == 1 else 1
        for m in all_moves:
            # Make the move on the board
            self.make_move(m, b, print_move = False)
            # Calculate how many moves the other player can take
            move_values[m] = len(b.populate_all_movements(other_player_id))
            # Undo the move we just made
            b.pop_last_move()

        # Get the move with the lowest number of moves the other player can take, and make it
        best_move = min(move_values, key = move_values.get)
        self.make_move(best_move, b, **kwargs)

    def make_max_self_move(self, b : AmazonsBoard, **kwargs) -> None:
        '''
            Calculate the move that leaves us with the most number of moves after taking this move
        '''
        # Generate all moves we can take
        all_moves = self.generate_all_moves(b)
        move_values = {}
        for m in all_moves:
            # Make the move on the board
            self.make_move(m, b, print_move = False)
            # Calculate how many moves we can take after this move
            move_values[m] = len(b.populate_all_movements(self.id))
            # Undo the move we just made
            b.pop_last_move()

        # Get the move with the most number of moves we can take after this move, and make it
        best_move = max(move_values, key = move_values.get)
        self.make_move(best_move, b, **kwargs)

    def make_minmax_move(self, b : AmazonsBoard, **kwargs) -> None:
        '''
            Calculate the move that leaves the opponent with the least number of moves and us with the most number of moves

            To find this move, we take max(# of moves we can make / # of moves our opponent can make)
        '''
        # Generate all moves we can take
        all_moves = self.generate_all_moves(b)
        move_values = {}
        other_player_id = 2 if self.id == 1 else 1
        for m in all_moves:
            # Make the move on the board
            self.make_move(m, b, print_move = False)
            # Calculate the number of moves this leaves our opponent with
            other_player_moves = len(b.populate_all_movements(other_player_id))
            # Calculate the number of moves we can make after this move
            self_moves = len(b.populate_all_movements(self.id))
            try:
                # Set the value
                move_values[m] = self_moves / other_player_moves
            except ZeroDivisionError:
                # In the case where this is zero, take this move since it wins us the game (it's already on the board)
                return
            # Undo the last move
            b.pop_last_move()

        # Get the move that has the highest ratio of our moves to opponent moves, and make it
        best_move = max(move_values, key = move_values.get)
        self.make_move(best_move, b, **kwargs)

    def generate_all_moves(self, b : AmazonsBoard) -> list[Move]:
        '''
            Generate all moves we can take on the board
        '''
        all_moves = []
        # Generate all places we can move to
        all_movements = b.populate_all_movements(self.id)
        for movement in all_movements:
            # Generate all places this move can attack
            all_attacks = b.populate_all_attacks_for_move(*movement)
            # Add these moves to the list
            all_moves.extend([Move(*movement, attack, self.id) for attack in all_attacks])

        return all_moves

    def prompt_human_move(self, b : AmazonsBoard, **kwargs) -> None:
        piece = input("Which piece would you like to move? ")
        location = input("Where would you like to move that piece to? ")
        attack = input("Where would you like the piece to attack? ")
        piece = tuple([int(x) for x in piece.split(",")])
        location = tuple([int(x) for x in location.split(",")])
        attack = tuple([int(x) for x in attack.split(",")])
        self.make_move(Move(piece, location, attack), b, **kwargs)

    def make_mcts_move(self, b : AmazonsBoard, times_play : int, **kwargs) -> None:
        '''
            Make a move using a pseudo-pure Monte Carlo Tree Search
        '''
        opponent_id = 1 if self.id == 2 else 2
        self.make_move(self.mcts(b, opponent_id, times_play, mode = kwargs.get("mode")), b, **kwargs)

    def mcts(self, b : AmazonsBoard, opponent_id : int, times_play : int, mode : Optional[str] = None) -> Move:
        '''
            Find the best move using a MCTS
        '''
        all_moves = self.generate_all_moves(b)
        move_dict = {}
        for m in all_moves:
            # Copy the board to keep the original intact
            new_board = deepcopy(b)
            # Make the move of all possible moves
            self.make_move(m, new_board, print_move = False)
            # Simulate the game "times_play" number of times
            outcomes = [self.play_full_game(new_board, opponent_id, mode) for _ in range(times_play)]
            # Find the ones that win
            winning_outcomes = [x for x in outcomes if x[0] == True]

            # If we find a winning move, get the one that takes the least moves
            if len(winning_outcomes):
                move_dict[m] = min(winning_outcomes, key = lambda t : t[1])
            # Otherwise there's no way to win with this move, just return false
            else:
                move_dict[m] = (False, 0)

        # Get all moves that won
        winning_moves = {k:v for k,v in move_dict.items() if v[0] == True}

        # Found winning moves
        if len(winning_moves):
            # Find the move that took the least total turns to win
            best_move = min(winning_moves.items(), key = lambda k : k[1])
            return best_move[0]
        # Did not find any winnings moves
        else:
            # Take a random move
            return random.choice(self.generate_all_moves(b))

    def play_full_game(self, b : AmazonsBoard, opponent_id : int, mode : Optional[str] = None) -> Tuple[bool, int]:
        '''
            Play a game out til a player wins taking actions for each player
        '''
        other_player = Player(opponent_id)
        # Only run random moves when the game isn't over
        while not b.done:
            match mode:
                case None:
                    other_player.make_random_move(b)
                case "random":
                    other_player.make_random_move(b)
                case "min":
                    other_player.make_min_opponent_move(b)
                case _:
                    raise Exception("Invalid type passed to play_full_game")

            if b.done:
                break

            # Take a random move for self
            self.make_random_move(b)
            if b.done:
                break
        # If the game was already over after taking the previous move, see if we won and how many moves it took
        return (b.winner == self.id, len(b.moves))
