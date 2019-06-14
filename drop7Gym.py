import gym
import gym.spaces
import drop7

from numpy import array


class drop7Gym(gym.Env):
    def __init__(self):
        self.game = drop7.Game()

        self.metadata = {'render.modes': ['human']}

        self.action_space = gym.spaces.Discrete(7)
        # Board is 7, 7 grid of pieces which are
        #
        # -2 is double gray piece
        # -1 is single gray
        # 0 is empty
        # 1-7 are themselves
        self.observation_space = gym.spaces.Dict({
            "nextPiece": gym.spaces.Discrete(7),
            "board": gym.spaces.Box(low=-2, high=7, shape=(7, 7), dtype=int),
            "piecesInRound": gym.spaces.Discrete(5)})

    # Returns (observation, reward, done)
    def step(self, action):
        if not self.game.canMove(action):
            observation = {
                "nextPiece": self.game.nextPiece,
                "board": array(self.game.board),
                "piecesInRound": self.game.piecesInRound}
            return (observation, 0, False)

        score_before = self.game.score
        self.game.move(action)
        observation = {
            "nextPiece": self.game.nextPiece,
            "board": array(self.game.board),
            "piecesInRound": self.game.piecesInRound}
        print("Step: ")
        print(observation)
        return (observation, self.game.score - score_before, self.game.isGameOver())

    def reset(self):
        self.game = drop7.Game()
        observation = {
            "nextPiece": self.game.nextPiece,
            "board": array(self.game.board),
            "piecesInRound": self.game.piecesInRound}
        print("Reset: ")
        print(observation)
        return observation

    def render(self, mode='human'):
        if mode is 'human':
            self.printBoard()
        else:
            super(drop7Gym, self).render(mode=mode)
