import gym
from gym import spaces
import numpy as np


class ProstheticHandEnv(gym.Env):
    def __init__(self):
        super(ProstheticHandEnv, self).__init__()
        self.action_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0]),
            high=np.array([140, 140, 140, 140, 80]),
            dtype=np.float32,
        )
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0]),
            high=np.array([140, 140, 140, 140, 80]),
            dtype=np.float32,
        )  # Servo angles
        self.state = np.zeros(5)  # Initial state: all servos at 0 degrees
        self.target_position = (
            self._generate_random_target()
        )  # Generate initial random target position

    def _generate_random_target(self):
        # Generate a random target position within the valid range for each servo
        return np.array(
            [
                np.random.uniform(0, 140),
                np.random.uniform(0, 140),
                np.random.uniform(0, 140),
                np.random.uniform(0, 140),
                np.random.uniform(0, 80),
            ]
        )

    def reset(self):
        self.state = np.zeros(5)  # Reset all servos to 0 degrees
        self.target_position = self._generate_random_target()
        return self.state

    def step(self, action):
        action = np.clip(
            action, self.observation_space.low, self.observation_space.high
        )
        self.state = action
        reward = self.compute_reward()
        done = self.is_done()
        return self.state, reward, done, {}

    def compute_reward(self):
        return -np.sum(
            np.abs(self.state - self.target_position)
        )  # Negative distance to target

    def is_done(self):
        # TODO: Define condition to end episode
        return False

    def render(self, mode="human"):
        # TODO: Implement rendering
        pass
