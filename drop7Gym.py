import gym
import gym.spaces
import drop7

class drop7Gym(gym.Env):
    def __init__(self):
        self.game = drop7.Game()

        self.metadata = {'render.modes': ['human']}

        self.actionSpace = gym.spaces.Discrete(7)
        # Board is 7, 7 grid of pieces which are
        #
        # -2 is double gray piece
        # -1 is single gray
        # 0 is empty
        # 1-7 are themselves
        self.observationSpace = gym.spaces.Dict({
                "nextPiece": gym.spaces.Discrete(7), 
                "board": gym.spaces.Box(low=-2, high=7, shape=(7,7), dtype=int),
                "piecesInRound": gym.spaces.Discrete(5)}) 

    # Returns (observation, reward, done)
    def step(self, action):
        if not self.game.canMove(action):
            observation = {
                "nextPiece": self.game.nextPiece,
                "board": self.game.board,
                "piecesInRound": self.game.piecesInRound }
            return (observation, 0, False)

        score_before = self.game.score
        self.game.move(action)
        observation = {
            "nextPiece": self.game.nextPiece,
            "board": self.game.board,
            "piecesInRound": self.game.piecesInRound }
        return (observation, self.game.score - score_before, self.game.isGameOver())

    def reset(self):
        self.game = drop7.Game()
        return {
            "nextPiece": self.game.nextPiece,
            "board": self.game.board,
            "piecesInRound": self.game.piecesInRound }

    def render(self, mode='human'):
        if mode is 'human':
            self.print()
        else:
            super(drop7Gym, self).render(mode=mode)
