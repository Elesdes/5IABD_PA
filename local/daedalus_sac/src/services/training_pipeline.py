from typing import Any
from config.global_config import Config
from models.autoencoder_model import Autoencoder
from models.regression_model import RegressionModel
from models.sac import load_sac_model
from tensorflow.keras.callbacks import (
    TensorBoard,
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
)
from utils.models_utils import load_model
from environment.gym_hand_prosthesis_env import ProstheticHandEnv
from utils.tensorboard_utils import TensorboardCallback
from stable_baselines3.common.callbacks import (
    EvalCallback,
    StopTrainingOnNoModelImprovement,
)


def train(
    x_train: Any,
    y_train: Any,
    config: Config,
    train_autoencoder: bool,
    autoencoder_pretrained: str,
    train_regression: bool,
    regression_pretrained: str,
):
    # Autoencoder
    if train_autoencoder:
        autoencoder = Autoencoder(config)
        autoencoder.compile()

        tensorboard_callback = TensorBoard(log_dir=config.tensorboard_log_autoencoder)
        early_stopping = EarlyStopping(
            monitor="val_loss", patience=1000, restore_best_weights=True
        )
        checkpoint = ModelCheckpoint(
            config.autoencoder_weights_path,
            save_best_only=True,
            monitor="val_loss",
        )
        reduce_lr = ReduceLROnPlateau(
            monitor="val_loss", factor=0.2, patience=100, min_lr=1e-3
        )

        autoencoder.fit(
            x_train,
            x_train,
            epochs=config.ae_epochs,
            batch_size=config.ae_batch_size,
            validation_split=0.2,
            callbacks=[tensorboard_callback, early_stopping, checkpoint, reduce_lr],
        )
    elif autoencoder_pretrained:
        autoencoder = load_model(autoencoder_pretrained)

    # Regression Model
    if train_regression:
        regression_model = RegressionModel(config, autoencoder)
        regression_model.compile()

        tensorboard_callback = TensorBoard(log_dir=config.tensorboard_log_regression)
        early_stopping = EarlyStopping(
            monitor="val_loss", patience=1000, restore_best_weights=True
        )
        checkpoint = ModelCheckpoint(
            config.regression_weights_path,
            save_best_only=True,
            monitor="val_loss",
        )
        reduce_lr = ReduceLROnPlateau(
            monitor="val_loss", factor=0.2, patience=100, min_lr=1e-3
        )

        regression_model.fit(
            x_train,
            y_train,
            epochs=config.regression_epochs,
            batch_size=config.regression_batch_size,
            validation_split=0.2,
            callbacks=[tensorboard_callback, early_stopping, checkpoint, reduce_lr],
        )
    elif regression_pretrained:
        regression_model = load_model(regression_pretrained)

    # SAC
    env = ProstheticHandEnv(x_train, y_train, seed=config.seed)

    sac_model = load_sac_model(env, config)

    stop_train_callback = StopTrainingOnNoModelImprovement(
        max_no_improvement_evals=5, min_evals=20, verbose=1
    )

    eval_callback = EvalCallback(
        env,
        best_model_save_path=config.sac_model_path,
        log_path=config.run_log_dir,
        eval_freq=1000,
        deterministic=False,
        render=False,
        callback_on_new_best=stop_train_callback,
        verbose=1,
    )

    tensorboard_callback = TensorboardCallback(config.tensorboard_log_sac)

    sac_model.learn(
        total_timesteps=config.sac_max_epochs,
        callback=[tensorboard_callback, eval_callback],
    )
