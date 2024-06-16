from dataclasses import dataclass


@dataclass
class TD3Config:
    learning_rate: float = 1e-3
    fc_layer_params: tuple = (256, 256)
    batch_size: int = 100
    buffer_size: int = 1000000
    num_episodes: int = 1000
    num_steps_per_episode: int = 200
    tau: float = 0.005
    gamma: float = 0.99
    policy_delay: int = 2
    noise_clip: float = 0.5
    exploration_noise: float = 0.1
    num_parallel_calls: int = 3
    sample_batch_size: int = 64
    num_steps: int = 2


td3_config = TD3Config()
