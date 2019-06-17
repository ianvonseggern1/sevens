from tic_tac_toe_dqn import get_dqn
from TicTacToeGym import TicTacToeGym
import numpy as np

dqn = get_dqn()
dqn.load_weights("dqn_tic_tac_toe_weights_large_layers.h5f")

gym = TicTacToeGym()
gym.reset()


while True:
    # AI move
    action = dqn.forward(gym.board)
    row = action // 3
    col = action % 3
    while gym.board[row][col] != 0:
        print("Agent wants to take illegal action row {} col {}".format(row, col))
        row = int(input("Enter alternative row: "))
        col = int(input("Enter alternative col: "))
    gym.board[row][col] = 1
    gym.render()
    gameOver, winner = gym.isGameOver()
    if gameOver:
        winner_string = "you"
        if winner == 0:
            winner_string = "tie"
        if winner == 1:
            winner_string = "ai"
        print("Game over winner is {}".format(winner_string))
        gym.reset()
        continue

    # Your move
    row = int(input("Enter your move's row: "))
    col = int(input("Enter your move's col: "))
    while gym.board[row][col] != 0:
        print("Your move is illegal action row {} col {}".format(row, col))
        row = int(input("Enter your move's row: "))
        col = int(input("Enter your move's col: "))
    gym.board[row][col] = -1
    gameOver, winner = gym.isGameOver()
    if gameOver:
        winner_string = "you"
        if winner == 0:
            winner_string = "tie"
        if winner == 1:
            winner_string = "ai"
        print("Game over winner is {}".format(winner_string))
        gym.reset()
        continue
