import gym
import gym.spaces

import numpy as np


class TicTacToeGym(gym.Env):
    def __init__(self):
        self.metadata = {'render.modes': ['human']}

        # Board is 3 x 3, map action space to 3 * r + c, which looks like
        #
        # 0 1 2
        # 3 4 5
        # 6 7 8
        self.action_space = gym.spaces.MultiDiscrete(
            [2, 2, 2, 2, 2, 2, 2, 2, 2])

        # -1 is opponents piece, 1 is our piece, 0 is empty
        self.observation_space = gym.spaces.Box(
            low=-1, high=1, shape=(3, 3), dtype=int)

    # Returns (observation, reward, done)
    # Returns a reward of -1 for an illegal move
    # Returns 100 for a victory -100 for a loss and 0 for a tie
    def step(self, action):
        info = {"items": []}
        #print("HELLO ACTION")
        # print(action)

        row = action // 3
        col = action % 3
        if self.board[row][col] != 0:
            return (self.board, -5, False, info)

        self.board[row][col] = 1
        isGameOver, winner = self.isGameOver()
        if isGameOver:
            return (self.board, winner * 100, True, info)

        self.performOpponentMoveSingleLookahead()
        isGameOver, winner = self.isGameOver()
        # (observation, score, isDone, info)
        return (self.board, winner * 100, isGameOver, info)

    def reset(self):
        self.board = np.zeros((3, 3))
        #print("Reset: ")
        # print(self.board)
        # Choose who goes first randomly
        if np.random.random() > 0.5:
            self.performOpponentMoveRandom()
        return self.board

    def render(self, mode='human'):
        def getPiece(val):
            if val == 1:
                return 'X'
            if val == -1:
                return 'O'
            return ' '
        if mode is 'human':
            print('______')
            for r in range(3):
                print('|' + ' '.join([getPiece(v) for v in self.board[r]]))
        else:
            super(TicTacToeGym, self).render(mode=mode)

    # Returns tuple (gameOver bool, winner int) where winner is -1 for opponent, 1 for you, and 0 for a tie
    def isGameOver(self):
        b = self.board
        # Check if there is a winner
        lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)],
        ]
        for l in lines:
            if b[l[0]] == 1 and b[l[1]] == 1 and b[l[2]] == 1:
                return (True, 1)
            if b[l[0]] == -1 and b[l[1]] == -1 and b[l[2]] == -1:
                return (True, -1)

        # Check if there are no open square, in which case its a tie
        for r in range(3):
            for c in range(3):
                if b[r][c] == 0:
                    return (False, 0)
        return (True, 0)

    # For now this just moves into a random spot
    def performOpponentMoveRandom(self):
        while True:
            row = np.random.randint(0, 3)
            column = np.random.randint(0, 3)
            if self.board[row][column] == 0:
                self.board[row][column] = -1
                return

    def performOpponentMoveSingleLookahead(self):
        lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)],
        ]
        # Opponent looks for a win
        for l in lines:
            opp_piece_count = len([(r, c)
                                   for (r, c) in l if self.board[r][c] == -1])
            if opp_piece_count != 2:
                continue
            open_r, open_c = [(r, c)
                              for (r, c) in l if self.board[r][c] != 1][0]
            if self.board[open_r][open_c] == 0:
                self.board[open_r][open_c] = -1
                return
        # Opponent looks for lines where ai has two pieces and the third spot is open
        for l in lines:
            ai_piece_count = len([(r, c)
                                  for (r, c) in l if self.board[r][c] == 1])
            if ai_piece_count != 2:
                continue
            open_r, open_c = [(r, c)
                              for (r, c) in l if self.board[r][c] != 1][0]
            if self.board[open_r][open_c] == 0:
                self.board[open_r][open_c] = -1
                return
        # Opponent looks for lines where they have one piece and both other spots are open
        for l in lines:
            opp_piece_count = len([(r, c)
                                   for (r, c) in l if self.board[r][c] == -1])
            if opp_piece_count != 1:
                continue
            open_spots = [(r, c)
                          for (r, c) in l if self.board[r][c] == 0]
            if len(open_spots) != 2:
                continue
            index = 0
            if np.random.random() > 0.5:
                index = 1
            open_r, open_c = open_spots[index]
            self.board[open_r][open_c] = -1
            return
        # Otherwise pick any open spot
        self.performOpponentMoveRandom()
