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
dqn.load_weights("dqn_tic_tac_toe_weights_fast.h5f")

gym = TicTacToeGym()
gym.reset()

dqn.test(gym, nb_episodes=5, visualize=True)


# while True:
#     # AI move
#     action = dqn.forward(gym.board)
#     row = action // 3
#     col = action % 3
#     while gym.board[row][col] != 0:
#         print("Agent wants to take illegal action row {} col {}".format(row, col))
#         row = int(input("Enter alternative row: "))
#         col = int(input("Enter alternative col: "))
#     gym.board[row][col] = 1
#     gym.render()
#     gameOver, winner = gym.isGameOver()
#     if gameOver:
#         winner_string = "you"
#         if winner == 0:
#             winner_string = "tie"
#         if winner == 1:
#             winner_string = "ai"
#         print("Game over winner is {}".format(winner_string))
#         gym.reset()
#         continue

#     # Your move
#     row = int(input("Enter your move's row: "))
#     col = int(input("Enter your move's col: "))
#     while gym.board[row][col] != 0:
#         print("Your move is illegal action row {} col {}".format(row, col))
#         row = int(input("Enter your move's row: "))
#         col = int(input("Enter your move's col: "))
#     gym.board[row][col] = -1
#     gameOver, winner = gym.isGameOver()
#     if gameOver:
#         winner_string = "you"
#         if winner == 0:
#             winner_string = "tie"
#         if winner == 1:
#             winner_string = "ai"
#         print("Game over winner is {}".format(winner_string))
#         gym.reset()
#         continue
