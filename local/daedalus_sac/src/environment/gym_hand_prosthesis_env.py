import gym
from gym import spaces
import numpy as np


class ProstheticHandEnv(gym.Env):
    def __init__(self, emg_data, target_angles, seed: int = None):
        super(ProstheticHandEnv, self).__init__()
        self.seed(seed)
        self.emg_data = emg_data
        self.target_angles = target_angles
        self.current_step = 0

        # Action and observation space
        self.action_space = spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(emg_data.shape[1] + 5,), dtype=np.float32
        )

        self.finger_ranges = [
            (0, 140),  # Index
            (0, 140),  # Middle
            (0, 140),  # Ring
            (0, 140),  # Pinky
            (0, 80),  # Thumb
        ]

        self.max_steps = len(emg_data)
        self.current_angles = np.zeros(5)

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def step(self, action):
        for i, (angle, (min_angle, max_angle)) in enumerate(
            zip(action, self.finger_ranges)
        ):
            self.current_angles[i] = min_angle + angle * (max_angle - min_angle)

        current_emg = self.emg_data[self.current_step]
        current_target = self.target_angles[self.current_step]

        reward = self._calculate_reward(self.current_angles, current_target)

        self.current_step += 1
        done = self.current_step >= self.max_steps

        obs = np.concatenate([current_emg, self.current_angles])

        info = {
            "current_angles": self.current_angles,
            "target_angles": current_target,
            "emg_data": current_emg,
        }

        return obs, reward, done, info

    def reset(self):
        self.current_step = 0
        self.current_angles = np.zeros(5)
        initial_emg = self.emg_data[0]
        return np.concatenate([initial_emg, self.current_angles])

    def _calculate_reward(self, current_angles, target_angles):
        errors = np.abs(current_angles - target_angles)
        normalized_errors = errors / np.array(
            [max_angle - min_angle for min_angle, max_angle in self.finger_ranges]
        )
        reward = -np.sum(normalized_errors)
        if np.all(normalized_errors < 0.1):
            reward += 10
        return reward

    def render(self, mode="human"):
        if mode == "human":
            print(f"Step: {self.current_step}")
            print(f"Current angles: {self.current_angles}")
            print(f"Target angles: {self.target_angles[self.current_step]}")
            print(f"EMG data: {self.emg_data[self.current_step]}")
        else:
            super(ProstheticHandEnv, self).render(mode=mode)
