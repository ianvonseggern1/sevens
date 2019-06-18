from tic_tac_toe_dqn import get_dqn
from TicTacToeGym import TicTacToeGym
import numpy as np

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--layer1', type=int, dest='layer1', default=512)
parser.add_argument('--layer2', type=int, dest='layer2', default=64)
parser.add_argument('--layer3', type=int, dest='layer3', default=64)
parser.add_argument('--dropout', type=float, dest='dropout', default=0.3)
args = parser.parse_args()

dqn = get_dqn(args.layer1, args.layer2, args.layer3, args.dropout)
dqn.load_weights("dqn_tic_tac_toe_weights_1193.h5f")

gym = TicTacToeGym()
gym.reset()

#dqn.test(gym, nb_episodes=5, visualize=True)


while True:
    # AI move
    state = dqn.memory.get_recent_state(gym.board)
    q_values = dqn.compute_q_values(state)
    print("Q Values:")
    to_print = ""
    for i, q in enumerate(q_values):
        to_print += " " + str(q)
        if i % 3 == 2:
            print(to_print)
            to_print = ""

    action = dqn.forward(gym.board)
    row = action // 3
    col = action % 3
    if gym.board[row][col] != 0:
        gym.render()
        print("Agent wanted to take illegal action row {} col {}".format(row, col))
        open_spots = []
        for r in range(3):
            for c in range(3):
                if gym.board[r][c] == 0:
                    open_spots.append((r, c))
        max_q_value = -1000000
        max_q_row = -1
        max_q_col = -1
        for spot in open_spots:
            r = spot[0]
            c = spot[1]
            if q_values[r * 3 + c] > max_q_value:
                max_q_value = q_values[r * 3 + c]
                max_q_row = r
                max_q_col = c
        row = max_q_row
        col = max_q_col
        print("Instead selected best available q value row {} col {} q-value {}".format(row, col, max_q_value))
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
