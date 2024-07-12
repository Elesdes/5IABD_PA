from typing import Union
import os
from stable_baselines3 import SAC
import tensorflow as tf


def load_model(model_path: str) -> Union[SAC, tf.keras.Model]:
    """
    Load either a Stable-Baselines3 model (e.g., SAC) or a TensorFlow H5 model.

    Args:
    model_path (str): Path to the model file.

    Returns:
    Union[SAC, tf.keras.Model]: Loaded model object.

    Raises:
    ValueError: If the model type is not recognized or the file doesn't exist.
    """
    if not os.path.exists(model_path):
        raise ValueError(f"Model file not found: {model_path}")

    match file_extension := os.path.splitext(model_path)[1].lower():
        case ".zip":
            try:
                model = SAC.load(model_path)
                print(f"Loaded Stable-Baselines3 model from {model_path}")
                return model
            except Exception as e:
                raise ValueError(f"Error loading Stable-Baselines3 model: {str(e)}")
        case (".h5" | ".hdf5"):
            try:
                model = tf.keras.models.load_model(model_path)
                print(f"Loaded TensorFlow H5 model from {model_path}")
                return model
            except Exception as e:
                raise ValueError(f"Error loading TensorFlow H5 model: {str(e)}")
        case _:
            raise ValueError(f"Unsupported model format: {file_extension}")
