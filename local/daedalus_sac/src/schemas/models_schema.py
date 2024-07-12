from dataclasses import dataclass
from typing import Literal, Tuple


@dataclass
class AutoencoderSchema:
    ae_encoding_dim: int = 16
    ae_epochs: int = 100
    ae_batch_size: int = 32
    ae_hidden_layers: Tuple[int, ...] = (128, 64, 32)
    ae_activation: Literal["relu", "tanh", "sigmoid", "elu", "selu"] = ("relu",)
    ae_output_activation: Literal["sigmoid", "tanh", "linear"] = ("sigmoid",)


@dataclass
class RegressionModelSchema:
    regression_epochs: int = 100
    regression_batch_size: int = 32


@dataclass
class SacSchema:
    sac_policy: str = "MlpPolicy"
    sac_learning_rate: float = 3e-4
    sac_buffer_size: float = 1_000_000
    sac_learning_starts: int = 100
    sac_batch_size: int = 32
    sac_tau: float = 5e-3
    sac_gamma: float = 0.99
    sac_train_freq: int = 1
    sac_gradient_steps: int = 1
    sac_ent_coef: Literal["auto"] = "auto"
    sac_target_update_interval: int = 1
    sac_target_entropy: Literal["auto"] = "auto"
    sac_use_sde: bool = False
    sac_sde_sample_freq: int = -1
    sac_use_sde_at_warmup: bool = False
