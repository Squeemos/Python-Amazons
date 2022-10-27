# Python Amazons
A simple implementation of the board game [Amazons](https://en.wikipedia.org/wiki/Game_of_the_Amazons)

## To get started
[game.py](./game.py) has a demo at the bottom. Otherwise, here's to to create a board and play against an AI opponent.
```python
from game import play_game

def main():
	# 10x10 board
	board_size = 10
	player_1 = "Human" # Prompts you to play moves
	player_2 = "Random" # Has the opponent take random moves
	play_game(
		board_size,
		player_1,
		player_2,
	)
	return 0

if __name__ == '__main__':
    SystemExit(main())
```

## Features
This implementation is very basic, but it contains a few novel features to play around with.
#### Different AI Modes
- Random moves
	- Populates a list of all possible moves the player can take, and then takes one at random
- "Min" moves
	- Populates a list of all possible moves the player can take, then tries each move out on the board. It then records how many moves the opponent has after it takes each move, and takes the move that minimizes the number of moves the opponent ends up with
- "Max" moves
	- Populates a list of all possible moves the player can take, then tries each move out on the board. It then records how many moves it can make after each move, and then takes the move that maximizes the number of moves the player ends up with
- "MinMax" moves
	- A combination of the min and max idea.
	- It populates a list of all possible moves the player can take, then tries each move out on the board. It then records how many moves the opponent ends up with and how many moves the player ends up with. It then chooses the move that maximizes the number of moves the player can make divided by the number of moves the opponent can make, and takes that move
- "MCTS" moves
	- A semi-pure implementation of a MCTS
	- It first calculates how many moves it can make on the current board. For each possible move, clone the board. On the clone, make the move. Then, simulate an entire game until the end of the game. The player will always take random actions, but the opponent can be chosen to take other types of moves (min, max, minmax, mcts). Do this for some chosen number of times. Evaluate the winner as the board
	- Then, check to see if there are any moves that lead to a winning board. If there are, find the move that took the least number of moves to win in, and take that move. If there are no winners found from the simulation, take a random move instead

Example of a "MCTS" AI playing a "Min" AI
```python
from game import play_game

def main():
	# 10x10 board
	board_size = 10
	player_1 = "MCTS" # MCTS player
	player_2 = "Min" # Min opponent

	# MCTS parameters
	n_mcts_games = 100 # Have the MCTS play 100 simulations of each board
	mcts_mode = "random" # Method the simulated opponent plays moves. Can be min, random, max, minmax
	play_game(
		board_size,
		player_1,
		player_2,
		n_mcts_games = n_mcts_games,
		mcts_mode = mcts_mode,
	)
	return 0

if __name__ == '__main__':
    SystemExit(main())
```