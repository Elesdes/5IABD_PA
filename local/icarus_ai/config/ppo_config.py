from dataclasses import dataclass


@dataclass
class PPOConfig:
    learning_rate: float = 1e-4
    fc_layer_params: tuple = (64, 64)
    num_epochs: int = 10
    gamma: float = 0.99
    lambda_: float = 0.95
    clip_epsilon: float = 0.2
    entropy_regularization: float = 0.0
    value_loss_weight: float = 1.0
    use_gae: bool = True
    normalize_observations: bool = True
    normalize_rewards: bool = True
    gradient_clipping: float = None
    value_clipping: float = None
    num_parallel_calls: int = 3
    sample_batch_size: int = 64
    num_steps: int = 2


ppo_config = PPOConfig()
