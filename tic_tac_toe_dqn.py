from TicTacToeGym import TicTacToeGym
import numpy as np
import gym

from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import spell.metrics as metrics


# Concept taken from https://github.com/keras-rl/keras-rl/blob/master/examples/dqn_cartpole.py

# Get the environment and extract the number of actions.
env = TicTacToeGym()
np.random.seed(1234)
env.seed(1234)
nb_actions = 9  # env.action_space.n

# Next, we build a very simple model.
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(81))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('softmax'))
print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=1000,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Create spell metrics callback
total_reward = 0
epochs = 0


def handleEpochEnd(epoch, logs):
    global total_reward
    global epochs
    total_reward += logs['episode_reward']
    epochs += 1
    if epochs == 100:
        metrics.send_metric("reward", total_reward / 100)
        epochs = 0
        total_reward = 0


metrics_callback = LambdaCallback(
    on_epoch_end=lambda epoch, logs: handleEpochEnd(epoch, logs))

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=5000000, visualize=False,
        verbose=1, callbacks=[metrics_callback])

# After training is done, we save the final weights.
dqn.save_weights('dqn_tic_tac_toe_weights.h5f', overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
#dqn.test(env, nb_episodes=5, visualize=True)
