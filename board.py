import numpy as np

from move import Move

from typing import Optional, Tuple

#<editor-fold> Exceptions
class ControlError(Exception):
    pass

class NoPieceError(Exception):
    pass

class PathError(Exception):
    pass

class TurnError(Exception):
    pass

class SizeError(Exception):
    pass

class GameOver(Exception):
    pass
#</editor-fold> Exceptions

class AmazonsBoard(object):
    def __init__(self, n : int = 10, **kwargs):
        if n == 1:
            raise SizeError(f"Board cannot be of size 1")
        elif n == 2 and kwargs.get("starting_positions") is None:
            raise SizeError(f"Board cannot be of size 2 without custom starting positions")
        self.__n = n

        # Useful members for checking pieces later on
        self.__up = (0, -1)
        self.__down = (0, 1)
        self.__left = (-1, 0)
        self.__right = (1, 0)
        self.__up_right = (1, -1)
        self.__up_left = (-1, -1)
        self.__down_right = (1, 1)
        self.__down_left = (-1, 1)
        self.__dirs = [self.__up, self.__down, self.__left, self.__right, self.__up_left, self.__up_right, self.__down_left, self.__down_right]

        self.reset(**kwargs)

    #<editor-fold> Properties
    @property
    def shape(self):
        return self.__board.shape

    @property
    def n(self):
        return self.__n

    @property
    def done(self):
        return self.__done

    @property
    def winner(self):
        return self.__winner

    @property
    def moves(self):
        return self.__moves
    #</editor-fold> Properties

    def __str__(self):
        return_string = ""
        for index, row in enumerate(self.__board):
            for item in row:
                if item == -1:
                    return_string += "X"
                else:
                    return_string += str(item)
                return_string += " "
            if index + 1 != self.n:
                return_string += "\n"

        return return_string

    def make_move(self, m : Move, **kwargs):
        '''
            Check the move, apply to the board, check if the game is over
        '''
        if self.done:
            raise GameOver(f"The game is currently over. Please reset the board to play again")
        if kwargs.get("print_move", False) not in [False, None]:
            print(m)
        self.check_move(m)
        self.apply_move(m)
        self.__moves.append(m)
        self.check_done()

    def apply_move(self, m : Move) -> None:
        '''
            Add the move to the board
        '''
        self.__board[m.start] = 0
        self.__board[m.end] = m.id
        self.__board[m.attack] = -1
        self.__last_player = m.id

    def bounds_check(self, position : Tuple[int, int]) -> bool:
        '''
            Check that the position of the piece/attack is inside the board
        '''
        x, y = position
        if x >= self.n or x < 0 or y >= self.n or y < 0:
            return False
        return True

    def player_has_control(self, m : Move) -> bool:
        '''
            Check if the player can move the piece it's trying to move
        '''
        if self.__board[m.start] != m.id:
            return False
        return True

    def is_piece(self, m : Move) -> bool:
        '''
            Check if the item at the location is actually a movable piece
        '''
        if self.__board[m.start] == 0 or self.__board[m.start] == -1:
            return False
        return True

    def check_trajectory(self, start : Tuple[int, int], end : Tuple[int, int]) -> bool:
        '''
            Check that the piece at start can move to the location at end
        '''
        x, y = start
        u, v = end
        x_diff = u - x
        y_diff = v - y
        dir_x = np.sign(x_diff)
        dir_y = np.sign(y_diff)

        # Check there isn't something there first
        if self.__board[end] != 0:
            return False
        # Check there are no pieces in that direction
        while x < u and y < v:
            x += dir_x
            y += dir_y
            if self.__board[x, y] != 0:
                return False

        # If either are 0, the move can be made
        if x_diff == 0 or y_diff == 0:
            return True
        # Make sure it's a multiple of its' movement
        else:
            return abs(x_diff) == abs(y_diff)

    def reset(self, **kwargs) -> None:
        '''
            Reset the board to the starting configuration
        '''
        self.__board = np.zeros((self.n, self.n), dtype = int)
        self.__done = False
        self.__last_player = -1
        self.__winner = -1
        self.__moves = []

        # Custom starting positions
        if (starting_positions := kwargs.get("starting_positions")) is not None:
            for key, value in starting_positions.items():
                if not self.bounds_check(key):
                    raise IndexError(f"Starting position {key} for Player {value} is out of bounds on board {self.shape}")
                self.__board[key] = value
        # Default starting configuration
        else:
            pos = self.n // 2
            if self.n % 2 == 0:
                # Player 1
                self.__board[0, pos - 2] = 1
                self.__board[0, pos + 1] = 1
                self.__board[pos - 2, 0] = 1
                self.__board[pos - 2, self.n - 1] = 1

                # Player 2
                self.__board[pos + 1, 0] = 2
                self.__board[pos + 1, self.n - 1] = 2
                self.__board[self.n - 1, pos - 2] = 2
                self.__board[self.n - 1, pos + 1] = 2

            else:
                # Player 1
                self.__board[0, pos - 1] = 1
                self.__board[0, pos + 1] = 1
                self.__board[pos - 1, 0] = 1
                self.__board[pos -1, self.n - 1] = 1

                # Player 2
                self.__board[pos + 1, 0] = 2
                self.__board[pos + 1, self.n - 1] = 2
                self.__board[self.n - 1, pos - 1] = 2
                self.__board[self.n - 1, pos + 1] = 2

    def check_move(self, m : Move) -> None:
        '''
            Perform all checks on the move, if there's a problem it will raise an exception
        '''
        # Make sure the move has an id
        if m.id == 0 or m.id == -1:
            raise ControlError(f"Move attempting to be made has no owner")

        # Make sure the same player doesn't play twice
        if self.__last_player == m.id:
            raise TurnError(f"It is not player {m.id}'s turn'")

        # Make sure the player is trying to move a piece
        if not self.is_piece(m):
            raise NoPieceError(f"No player piece at {m.start}")

        # Make sure the player has control of the piece
        if not self.player_has_control(m):
            raise ControlError(f"Player {m.id} does not have control of piece at {m.start}")

        # Check the bounds for each step of the move
        if not self.bounds_check(m.start):
            raise IndexError(f"Invalid Move starting position {m.start} on board {self.shape}")

        if not self.bounds_check(m.end):
            raise IndexError(f"Invalid Move ending position {m.end} on board {self.shape}")

        if not self.bounds_check(m.attack):
            raise IndexError(f"Invalid Move attack position {m.attack} on board {self.shape}")

        # Check if the piece can actually move to the correct location
        if not self.check_trajectory(m.start, m.end):
            raise PathError(f"Move from {m.start} -> {m.end} is invalid")

        # The player can always shoot where it just came from
        if m.start != m.attack:
            # Make sure the piece can attack where the spot is
            if not self.check_trajectory(m.end, m.attack):
                raise PathError(f"Attack from {m.end} -> {m.attack} is invalid")

    def check_done(self) -> None:
        '''
            Check if the game is over
        '''
        # Check if the next player has moves
        next_player = 2 if self.__last_player == 1 else 1
        if not self.check_if_player_has_moves(next_player):
            self.__winner = self.__last_player
            self.__done = True
        # Check if the player that just moved has turns left
        elif not self.check_if_player_has_moves(self.__last_player):
            self.__winner = next_player
            self.__done = True

    def check_if_player_has_moves(self, id : int) -> bool:
        '''
            See if a specific player has any locations it can move to
        '''
        return len(self.populate_all_movements(id)) != 0

    def populate_all_movements(self, id : int) -> list[Tuple[Tuple[int,int], Tuple[int,int]]]:
        '''
            Given a player id, generate all places their pieces can move to

            Output looks like [
                ((piece location), (ending location)),
                ((piece location), (ending location)),
                ...
                ]
        '''
        potential_moves = []
        piece_locations = np.where(self.__board == id)
        for piece in zip(piece_locations[0], piece_locations[1]):
            for div_x, div_y in self.__dirs:
                x, y = piece
                x, y = x + div_x, y + div_y
                while x >= 0 and x < self.n and y >= 0 and y < self.n:
                    # Check if the piece can move there
                    if self.__board[x, y] == 0:
                        potential_moves.append((piece, (x, y)))
                    # Otherwise break since we don't need to check further
                    else:
                        break
                    x, y = x + div_x, y + div_y

        return potential_moves

    def populate_all_attacks_for_move(self, start : Tuple[int, int], end : Tuple[int, int]) -> list[Tuple[int, int]]:
        '''
            Given a starting position and ending position, generate all places the piece can attack

            Output looks like [
                (attack location),
                (attack location),
                ...
                ]
        '''
        # Can always attack where we just moved from
        potential_attacks = [start]
        for div_x, div_y in self.__dirs:
            x, y = end
            x, y = x + div_x, y + div_y
            while x >= 0 and x < self.n and y >= 0 and y < self.n:
                if self.__board[x, y] == 0:
                    potential_attacks.append((x,y))
                else:
                    break
                x, y = x + div_x, y + div_y

        return potential_attacks

    def pop_last_move(self) -> None:
        '''
            Undo the last move from the board
        '''
        # Make sure there is a move to undo
        if len(self.__moves):
            last_move = self.__moves.pop()

            # Return everything to the previous board state
            self.__board[last_move.attack] = 0
            self.__board[last_move.end] = 0
            self.__board[last_move.start] = self.__last_player

            # Check if this was the first move ever
            if len(self.__moves) == 0:
                self.__last_player = -1
            # Swap the previous player
            else:
                self.__last_player = 2 if self.__last_player == 1 else 1

            if self.__done:
                self.__done = not self.__done

    def print_moves(self) -> None:
        '''
            Print all moves in the order they were taken
        '''
        for m in self.__moves:
            print(m)
