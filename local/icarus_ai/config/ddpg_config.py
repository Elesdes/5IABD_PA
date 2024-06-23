from dataclasses import dataclass


@dataclass
class DDPGConfig:
    learning_rate: float = 1e-3
    fc_layer_params: tuple = (400, 300)
    batch_size: int = 64
    buffer_size: int = 1000000
    num_episodes: int = 1000
    num_steps_per_episode: int = 200
    tau: float = 0.005
    gamma: float = 0.99
    actor_update_freq: int = 1
    critic_update_freq: int = 1
    num_parallel_calls: int = 3
    sample_batch_size: int = 64
    num_steps: int = 2


ddpg_config = DDPGConfig()
