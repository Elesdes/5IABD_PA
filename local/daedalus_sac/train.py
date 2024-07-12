import click
import yaml
import os
import shutil
from datetime import datetime
from types import SimpleNamespace
from seed_utils import set_global_seeds
from models import Autoencoder, create_regression_model
from environment import ProstheticHandEnv
from stable_baselines3 import SAC
from utils import TensorboardCallback, load_data
from local.daedalus_sac.preprocessing import EMGPreprocessor
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping
from stable_baselines3.common.callbacks import (
    EvalCallback,
    BaseCallback,
    StopTrainingOnNoModelImprovement,
)


def dict_to_namespace(d):
    namespace = SimpleNamespace()
    for key, value in d.items():
        if isinstance(value, dict):
            setattr(namespace, key, dict_to_namespace(value))
        else:
            setattr(namespace, key, value)
    return namespace


def load_config(config_path):
    with open(config_path, "r") as f:
        config_dict = yaml.safe_load(f)
    return dict_to_namespace(config_dict)


def namespace_to_dict(namespace):
    return {
        k: namespace_to_dict(v) if isinstance(v, SimpleNamespace) else v
        for k, v in vars(namespace).items()
    }


def create_run_directories(config):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(config.paths.base_log_dir, f"run_{timestamp}")

    # Create main run directory
    os.makedirs(run_dir, exist_ok=True)

    # Create subdirectories
    subdirs = ["models", "tensorboard", "logs", "configs"]
    for subdir in subdirs:
        os.makedirs(os.path.join(run_dir, subdir), exist_ok=True)

    # Create a new config object with updated paths
    new_config = SimpleNamespace(**vars(config))
    new_config.paths = SimpleNamespace(**vars(config.paths))

    # Update new_config with run-specific paths
    new_config.paths.run_dir = run_dir
    new_config.paths.models_dir = os.path.join(run_dir, "models")
    new_config.paths.tensorboard_dir = os.path.join(run_dir, "tensorboard")
    new_config.paths.log_path = os.path.join(run_dir, "logs")
    new_config.paths.configs_dir = os.path.join(run_dir, "configs")

    # Set paths for individual models and their tensorboard logs
    new_config.paths.autoencoder_weights = os.path.join(
        new_config.paths.models_dir, "autoencoder_weights.h5"
    )
    new_config.paths.regression_weights = os.path.join(
        new_config.paths.models_dir, "regression_weights.h5"
    )
    new_config.paths.sac_model = os.path.join(
        new_config.paths.models_dir, "sac_model.zip"
    )

    new_config.paths.tensorboard_log_autoencoder = os.path.join(
        new_config.paths.tensorboard_dir, "autoencoder"
    )
    new_config.paths.tensorboard_log_regression = os.path.join(
        new_config.paths.tensorboard_dir, "regression"
    )
    new_config.paths.tensorboard_log_sac = os.path.join(
        new_config.paths.tensorboard_dir, "sac"
    )

    new_config.paths.run_config_path = os.path.join(
        new_config.paths.configs_dir, "config.yaml"
    )

    return new_config


@click.command()
@click.option("--train-autoencoder", is_flag=True, help="Train the autoencoder")
@click.option("--train-regression", is_flag=True, help="Train the regression model")
@click.option("--train-sac", is_flag=True, help="Train the SAC model")
@click.option(
    "--config-path",
    default="local/daedalus_sac/config.yaml",
    help="Path to the configuration file",
)
def main(train_autoencoder, train_regression, train_sac, config_path):
    original_config = load_config(config_path)
    run_config = create_run_directories(original_config)

    set_global_seeds(run_config.global_config.seed)

    # Load and preprocess data
    emg_data, target_angles = load_data(run_config.data.data_path)
    preprocessor = EMGPreprocessor(run_config.preprocessing)
    emg_data_preprocessed = preprocessor.preprocess(emg_data)

    # Create environment
    env = ProstheticHandEnv(
        emg_data_preprocessed, target_angles, seed=run_config.global_config.seed
    )

    # Autoencoder
    input_dims = emg_data_preprocessed.shape[1:]
    autoencoder = Autoencoder(input_dims)

    if train_autoencoder or not os.path.exists(run_config.paths.autoencoder_weights):
        click.echo("Training autoencoder...")
        autoencoder.compile(optimizer="adam", loss="mse")
        tensorboard_callback = TensorBoard(
            log_dir=run_config.paths.tensorboard_log_autoencoder
        )
        early_stopping = EarlyStopping(
            monitor="val_loss", patience=10, restore_best_weights=True
        )
        autoencoder.fit(
            emg_data_preprocessed,
            emg_data_preprocessed,
            epochs=run_config.autoencoder.epochs,
            batch_size=run_config.autoencoder.batch_size,
            validation_split=0.2,
            callbacks=[tensorboard_callback, early_stopping],
        )
        autoencoder.save_weights(run_config.paths.autoencoder_weights)
    else:
        click.echo("Loading pre-trained autoencoder...")
        autoencoder.load_weights(run_config.paths.autoencoder_weights)

    # Regression model
    regression_model = create_regression_model(
        autoencoder.encoding_dim, env.action_space.shape[0]
    )

    if train_regression or not os.path.exists(run_config.paths.regression_weights):
        click.echo("Training regression model...")
        encoded_emg = autoencoder.encoder(emg_data_preprocessed).numpy()
        tensorboard_callback = TensorBoard(
            log_dir=run_config.paths.tensorboard_log_regression
        )
        early_stopping = EarlyStopping(
            monitor="val_loss", patience=10, restore_best_weights=True
        )
        regression_model.fit(
            encoded_emg,
            target_angles,
            epochs=run_config.regression.epochs,
            batch_size=run_config.regression.batch_size,
            validation_split=0.2,
            callbacks=[tensorboard_callback, early_stopping],
        )
        regression_model.save_weights(run_config.paths.regression_weights)
    else:
        click.echo("Loading pre-trained regression model...")
        regression_model.load_weights(run_config.paths.regression_weights)

    # SAC
    if train_sac or not os.path.exists(run_config.paths.sac_model):
        click.echo("Training SAC model...")
        model = SAC(
            "MlpPolicy",
            env,
            **vars(run_config.sac),
            tensorboard_log=run_config.paths.tensorboard_log_sac,
        )

        eval_callback = EvalCallback(
            env,
            best_model_save_path=run_config.paths.models_dir,
            log_path=run_config.paths.log_path,
            eval_freq=run_config.training.eval_freq,
            deterministic=True,
            render=False,
        )

        tensorboard_callback = TensorboardCallback(run_config.paths.tensorboard_log_sac)

        # Early stopping for SAC
        stop_train_callback = StopTrainingOnNoModelImprovement(
            max_no_improvement_evals=5, min_evals=20, verbose=1
        )
        eval_callback = EvalCallback(
            env,
            callback_on_new_best=stop_train_callback,
            eval_freq=10000,
            best_model_save_path=run_config.paths.models_dir,
            verbose=1,
        )

        model.learn(
            total_timesteps=run_config.training.total_timesteps,
            callback=[tensorboard_callback, eval_callback],
        )

        model.save(run_config.paths.sac_model)
    else:
        click.echo("Loading pre-trained SAC model...")
        model = SAC.load(run_config.paths.sac_model, env=env)

    click.echo("Training complete!")


if __name__ == "__main__":
    main()
