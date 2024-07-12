from dataclasses import asdict, dataclass
import os
from datetime import datetime


@dataclass
class ImmutablePaths:
    # Base dirs
    root: str = os.path.abspath(os.path.join("local", "daedalus_sac"))
    data: str = os.path.join(root, "data")
    logs: str = os.path.join(root, "logs")

    ## Data
    dataset: str = os.path.join(data, "dataset")

    ## Logs
    run_name = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_log_dir: str = os.path.join(logs, run_name)

    ### Logs Subdirs & Files
    tensorboard_log_dir: str = os.path.join(run_log_dir, "tensorboard")
    models_log_dir: str = os.path.join(run_log_dir, "models")
    json_config_copy_path: str = os.path.join(run_log_dir, "config.json")

    #### Tensorboard logs
    tensorboard_log_autoencoder = os.path.join(tensorboard_log_dir, "autoencoder")
    tensorboard_log_regression = os.path.join(tensorboard_log_dir, "regression")
    tensorboard_log_sac = os.path.join(tensorboard_log_dir, "sac")

    #### Models name
    autoencoder_weights_path: str = os.path.join(
        models_log_dir, "autoencoder_weights.h5"
    )
    regression_weights_path: str = os.path.join(models_log_dir, "regression_weights.h5")
    sac_model_path: str = os.path.join(models_log_dir, "sac_model.zip")


@dataclass
class PathsSchema(ImmutablePaths):
    path_dataset_to_load: str = ""
