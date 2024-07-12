from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any, Dict, List, Literal, Tuple, Type
from schemas.paths_schema import PathsSchema
from schemas.models_schema import AutoencoderSchema, RegressionModelSchema, SacSchema
from schemas.preprocessing_schema import PreprocessingSchema
from schemas.training_schema import TrainingSchema
import os
import json


class Config(
    PathsSchema,
    PreprocessingSchema,
    AutoencoderSchema,
    RegressionModelSchema,
    SacSchema,
    TrainingSchema,
):
    def __init__(
        self,
        seed: int = 42,
        path_dataset_to_load: str = "complete_dataset.csv",
        sampling_rate: int = 1000,
        bandpass_low: int = 20,
        bandpass_high: int = 450,
        filter_order: int = 4,
        envelope_window: float = 0.2,
        ae_encoding_dim: int = 16,
        ae_epochs: int = 100,
        ae_batch_size: int = 32,
        ae_hidden_layers: List[int] = [128, 64, 32],
        ae_activation: Literal["relu", "tanh", "sigmoid", "elu", "selu"] = "relu",
        ae_output_activation: Literal["sigmoid", "tanh", "linear"] = "sigmoid",
        ae_learning_rate: float = 1e-3,
        regression_epochs: int = 100,
        regression_batch_size: int = 32,
        sac_policy: str = "MlpPolicy",
        sac_learning_rate: float = 3e-4,
        sac_buffer_size: float = 1_000_000,
        sac_learning_starts: int = 100,
        sac_batch_size: int = 32,
        sac_tau: float = 5e-3,
        sac_gamma: float = 0.99,
        sac_train_freq: int = 1,
        sac_gradient_steps: int = 1,
        sac_ent_coef: Literal["auto"] = "auto",
        sac_target_update_interval: int = 1,
        sac_target_entropy: Literal["auto"] = "auto",
        sac_use_sde: bool = False,
        sac_sde_sample_freq: int = -1,
        sac_use_sde_at_warmup: bool = False,
        total_timesteps: int = 100_000,
        eval_freq: int = 500,
    ):
        # Seed
        self.seed: int = seed

        # Paths
        self.path_dataset_to_load: str = os.path.join(
            self.dataset, path_dataset_to_load
        )

        # Preprocessing
        self.sampling_rate: int = sampling_rate
        self.bandpass_low: int = bandpass_low
        self.bandpass_high: int = bandpass_high
        self.filter_order: int = filter_order
        self.envelope_window: float = envelope_window

        # Models
        ## Autoencoder
        self.ae_encoding_dim: int = ae_encoding_dim
        self.ae_epochs: int = ae_epochs
        self.ae_batch_size: int = ae_batch_size
        self.ae_hidden_layers: List[int] = [128, 64, 32]
        self.ae_activation: Literal[
            "relu", "tanh", "sigmoid", "elu", "selu"
        ] = ae_activation
        self.ae_output_activation: Literal[
            "sigmoid", "tanh", "linear"
        ] = ae_output_activation
        self.ae_learning_rate: float = ae_learning_rate

        ## Regression
        self.regression_epochs: int = regression_epochs
        self.regression_batch_size: int = regression_batch_size

        ## SAC
        self.sac_policy: str = sac_policy
        self.sac_learning_rate: float = sac_learning_rate
        self.sac_buffer_size: float = sac_buffer_size
        self.sac_learning_starts: int = sac_learning_starts
        self.sac_batch_size: int = sac_batch_size
        self.sac_tau: float = sac_tau
        self.sac_gamma: float = sac_gamma
        self.sac_train_freq: int = sac_train_freq
        self.sac_gradient_steps: int = sac_gradient_steps
        self.sac_ent_coef: Literal["auto"] = sac_ent_coef
        self.sac_target_update_interval: int = sac_target_update_interval
        self.sac_target_entropy: Literal["auto"] = sac_target_entropy
        self.sac_use_sde: bool = sac_use_sde
        self.sac_sde_sample_freq: int = sac_sde_sample_freq
        self.sac_use_sde_at_warmup: bool = sac_use_sde_at_warmup

        # Training
        self.total_timesteps: int = total_timesteps
        self.eval_freq: int = eval_freq

        # Utils
        self.__generate_file_tree()
        self.__save_to_json()

    @classmethod
    def from_json(cls, json_file_path: str) -> "Config":
        with open(json_file_path, "r") as f:
            data = json.load(f)

        flat_data = cls._flatten_dict(data)

        return cls(**flat_data)

    @staticmethod
    def _flatten_dict(nested_dict: Dict[str, Any]) -> Dict[str, Any]:
        flat_dict = {}
        for inner_dict in nested_dict.values():
            flat_dict.update(inner_dict)
        return flat_dict

    def __get_dataclass_values(self, dataclass_type: Type[Any]) -> Dict[str, Any]:
        result = {}
        for field in fields(dataclass_type):
            if hasattr(self, field.name):
                result[field.name] = getattr(self, field.name)
        return result

    def __generate_file_tree(self):
        dict_dataclass_vars = self.__get_dataclass_values(dataclass_type=PathsSchema)

        for path in dict_dataclass_vars.values():
            if not bool(Path(path).suffix):
                os.makedirs(name=path, exist_ok=True)

    def __to_dict(self):
        result = {}
        added_vars = set()

        for base in self.__class__.__bases__:
            if base != object:
                class_name = base.__name__
                result[class_name] = {}

                if is_dataclass(base):
                    for field in fields(base):
                        if hasattr(self, field.name) and field.name not in added_vars:
                            result[class_name][field.name] = getattr(self, field.name)
                            added_vars.add(field.name)
                else:
                    for name, value in base.__dict__.items():
                        if (
                            not name.startswith("__")
                            and not callable(value)
                            and hasattr(self, name)
                            and name not in added_vars
                        ):
                            result[class_name][name] = getattr(self, name)
                            added_vars.add(name)

        result["Config"] = {}
        for name, value in vars(self).items():
            if (
                not name.startswith("__")
                and not callable(value)
                and name not in added_vars
            ):
                result["Config"][name] = value

        # Remove empty classes
        result = {k: v for k, v in result.items() if v}

        return result

    def __save_to_json(self):
        with open(self.json_config_copy_path, "w") as f:
            json.dump(self.__to_dict(), f, indent=4)
