from dataclasses import dataclass


@dataclass
class TrainingSchema:
    total_timesteps: int = 100_000
    eval_freq: int = 500
