from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class HyperparameterOptimizationConfig:
    learning_rate: Tuple[float, float] = (1e-5, 1e-1)
    fc_layer_params: List[Tuple[int]] = field(
        default_factory=lambda: [(128, 128), (256, 256), (64, 64, 64)]
    )
    num_epochs: Tuple[int, int] = (1, 50)
    tau: Tuple[float, float] = (0.001, 0.1)
    gamma: Tuple[float, float] = (0.9, 0.999)
    policy_delay: Tuple[int, int] = (1, 5)
    noise_clip: Tuple[float, float] = (0.1, 0.5)
    exploration_noise: Tuple[float, float] = (0.1, 0.5)
    buffer_size: int = 1000000
    num_iterations: int = 1000
    n_trials: int = 100


@dataclass
class TrainingConfig:
    num_iterations: int = 10000
    save_interval: int = 1000
    buffer_size: int = 1000000


# Instantiate the configuration objects
hyperparameter_optimization_config = HyperparameterOptimizationConfig()
training_config = TrainingConfig()
