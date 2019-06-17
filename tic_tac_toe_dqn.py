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


def get_dqn():
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(nb_actions, activation='softmax'))
    print(model.summary())

    # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
    # even the metrics!
    memory = SequentialMemory(limit=200000, window_length=1)
    policy = BoltzmannQPolicy()
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10000,
                   target_model_update=3e-3, policy=policy)
    dqn.compile(Adam(lr=3e-4), metrics=['mae'])
    return dqn


# Next, we build a very simple model.
dqn = get_dqn()


# Create spell metrics callback
reward_avg_100 = 0
reward_avg_1000 = 0
epochs = 0

if __name__ == "__main__":
    def handleEpochEnd(epoch, logs):
        global reward_avg_100
        global reward_avg_1000
        global epochs
        reward_avg_100 += logs['episode_reward']
        reward_avg_1000 += logs['episode_reward']
        epochs += 1
        if epochs % 100 == 0:
            metrics.send_metric("reward_last_100", reward_avg_100 / 100)
            reward_avg_100 = 0
        if epochs % 1000 == 0:
            metrics.send_metric("reward_last_1000", reward_avg_1000 / 1000)
            reward_avg_1000 = 0

    metrics_callback = LambdaCallback(
        on_epoch_end=lambda epoch, logs: handleEpochEnd(epoch, logs))

    # Okay, now it's time to learn something! We visualize the training here for show, but this
    # slows down training quite a lot. You can always safely abort the training prematurely using
    # Ctrl + C.
    dqn.fit(env, nb_steps=200000, visualize=False,
            verbose=1, callbacks=[metrics_callback])

    # After training is done, we save the final weights.
    dqn.save_weights('dqn_tic_tac_toe_weights.h5f', overwrite=True)

    # Finally, evaluate our algorithm for 5 episodes.
    #dqn.test(env, nb_episodes=5, visualize=True)
