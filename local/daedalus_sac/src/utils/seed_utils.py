import numpy as np
import tensorflow as tf
import random
import gym


def set_global_seeds(seed):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    random.seed(seed)
    tf.keras.utils.set_random_seed(seed)
    gym.utils.seeding.np_random(seed)
