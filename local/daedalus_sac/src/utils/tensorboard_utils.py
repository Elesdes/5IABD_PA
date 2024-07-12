import tensorflow as tf
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np


class TensorboardCallback(BaseCallback):
    def __init__(self, log_dir: str, n_steps: int = 1_000):
        super(TensorboardCallback, self).__init__()
        self.log_dir = log_dir
        self.writer = None
        self.n_steps = n_steps

    def _on_training_start(self):
        self.writer = tf.summary.create_file_writer(self.log_dir)

    def _on_step(self):
        if self.n_calls % self.steps == 0:
            with self.writer.as_default():
                if len(self.model.ep_info_buffer) > 0:
                    ep_reward = np.mean(
                        [ep_info["r"] for ep_info in self.model.ep_info_buffer]
                    )
                    ep_length = np.mean(
                        [ep_info["l"] for ep_info in self.model.ep_info_buffer]
                    )
                    tf.summary.scalar("reward", ep_reward, step=self.n_calls)
                    tf.summary.scalar("episode_length", ep_length, step=self.n_calls)
        return True

    def _on_training_end(self):
        self.writer.close()


class StopTrainingOnNoImprovement(BaseCallback):
    def __init__(self, max_no_improvement_evals=5, min_evals=20, verbose=0):
        super(StopTrainingOnNoImprovement, self).__init__(verbose)
        self.max_no_improvement_evals = max_no_improvement_evals
        self.min_evals = min_evals
        self.best_mean_reward = -np.inf
        self.no_improvement_evals = 0
        self.n_evals = 0

    def _on_step(self) -> bool:
        if self.n_evals < self.min_evals:
            return True

        if self.parent is not None and self.parent.best_mean_reward is not None:
            if self.parent.best_mean_reward > self.best_mean_reward:
                self.best_mean_reward = self.parent.best_mean_reward
                self.no_improvement_evals = 0
            else:
                self.no_improvement_evals += 1
                if self.no_improvement_evals > self.max_no_improvement_evals:
                    if self.verbose > 0:
                        print(
                            f"Stopping training due to no improvement for {self.no_improvement_evals} evaluations"
                        )
                    return False
        self.n_evals += 1
        return True
