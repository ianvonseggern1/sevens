import numpy as np
import drop7Gym

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, concatenate
from keras.optimizers import Adam
from keras.utils import plot_model

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from rl.processors import MultiInputProcessor

# Inspired by https://gist.github.com/bklebel/e3bd43ce228a53d27de119c639ac61ee

# Get the environment and extract the number of actions.
#env = gym.make(ENV_NAME)
#np.random.seed(123)
#env.seed(123)
nb_actions = 7#env.action_space.n
env = drop7Gym.drop7Gym()

# Next, we build a very simple model.
model_board = Sequential()
model_board.add(Flatten(input_shape=(7,7), name='board'))
model_board_input = Input(shape=(7,7), name='board')
model_board_encoded = model_board(model_board_input)

model_nextPiece = Sequential()
model_nextPiece.add(Flatten(input_shape=(1, 1), name='nextPiece'))
model_nextPiece_input = Input(shape=(1, 1), name='nextPiece')
model_nextPiece_encoded = model_nextPiece(model_nextPiece_input)

model_piecesInRound = Sequential()
model_piecesInRound.add(Flatten(input_shape=(1,1), name='piecesInRound'))
model_piecesInRound_input = Input(shape=(1,1), name='piecesInRound')
model_piecesInRound_encoded = model_piecesInRound(model_piecesInRound_input)

con = concatenate([model_board_encoded, model_nextPiece_encoded, model_piecesInRound_encoded])

hidden = Dense(16, activation='relu')(con)
for _ in range(2): 
	hidden = Dense(16, activation='relu')(hidden)
output = Dense(nb_actions, activation='linear')(hidden)
model_final = Model(inputs=[model_board_input, model_nextPiece_input, model_piecesInRound_input], outputs=output)
print(model_final.summary())
#plot_model(model_final, to_file='model.png')

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model_final, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
               target_model_update=1e-2, policy=policy)
dqn.processor = MultiInputProcessor(3)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=20000, visualize=False, verbose=2)

# After training is done, we save the final weights.
dqn.save_weights('dqn_drop7_weights.h5f', overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=5, visualize=True)
