from TicTacToeGym import TicTacToeGym
import numpy as np
import gym

from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import spell.metrics as metrics

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--steps', type=int, dest='steps', default=200000)
parser.add_argument('--learning_rate', type=float,
                    dest='learning_rate', default=0.0003)
parser.add_argument('--target_model_update', type=float,
                    dest='target_model_update', default=0.003)
parser.add_argument('--layer1', type=int, dest='layer1', default=512)
parser.add_argument('--layer2', type=int, dest='layer2', default=64)
parser.add_argument('--layer3', type=int, dest='layer3', default=64)
parser.add_argument('--dropout', type=float, dest='dropout', default=0.3)
args = parser.parse_args()

# Concept taken from https://github.com/keras-rl/keras-rl/blob/master/examples/dqn_cartpole.py

# Get the environment and extract the number of actions.
env = TicTacToeGym()
np.random.seed(1234)
env.seed(1234)
nb_actions = 9  # env.action_space.n


def get_dqn(layer1, layer2, layer3, dropout):
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
    model.add(Dense(layer1, activation='relu'))
    model.add(Dense(layer2, activation='relu'))
    model.add(Dense(layer3, activation='relu'))
    model.add(Dropout(dropout))
    model.add(Dense(nb_actions, activation='softmax'))
    print(model.summary())

    # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
    # even the metrics!
    memory = SequentialMemory(limit=200000, window_length=1)
    policy = BoltzmannQPolicy()
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10000,
                   target_model_update=args.target_model_update, policy=policy)
    dqn.compile(Adam(lr=args.learning_rate), metrics=['mae'])
    return dqn


# Next, we build a very simple model.
dqn = get_dqn(args.layer1, args.layer2, args.layer3, args.dropout)


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
    dqn.fit(env, nb_steps=args.steps, visualize=False,
            verbose=1, callbacks=[metrics_callback])

    # After training is done, we save the final weights.
    dqn.save_weights('dqn_tic_tac_toe_weights.h5f', overwrite=True)

    # Finally, evaluate our algorithm for 5 episodes.
    #dqn.test(env, nb_episodes=5, visualize=True)
