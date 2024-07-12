from config.global_config import Config
import click
from decorators.click_decorators import mutually_exclusive_options
from utils.seed_utils import set_global_seeds
from services.training_pipeline import train
from services.load_dataset import load_dataset
from services.preprocessing import EMGPreprocessor


@click.command()
@click.option(
    "--train-autoencoder",
    type=bool,
    is_flag=True,
    default=False,
    help="Train the autoencoder.",
)
@click.option(
    "--autoencoder-pretrained",
    type=str,
    default="",
    help="Full path to the pre-trained autoencoder.",
)
@click.option(
    "--train-regression",
    type=bool,
    is_flag=True,
    default=False,
    help="Train the regression model.",
)
@click.option(
    "--regression-pretrained",
    type=str,
    default="",
    help="Full path to the pre-trained regression model.",
)
@click.option(
    "--custom-config",
    type=str,
    default="",
    help="Full path to your custom configuration. Formats available: JSON.",
)
@mutually_exclusive_options(
    ("train_autoencoder", "autoencoder_pretrained"),
    ("train_regression", "regression_pretrained"),
)
def main(
    train_autoencoder: bool = False,
    autoencoder_pretrained: str = "",
    train_regression: bool = False,
    regression_pretrained: str = "",
    custom_config: str = "",
):
    config = Config.from_json(custom_config) if custom_config else Config()

    set_global_seeds(config.seed)

    x_train, y_train = load_dataset(filename=config.path_dataset_to_load)

    x_train_preprocessed = EMGPreprocessor(config).preprocess(emg_data=x_train)

    train(
        x_train_preprocessed,
        y_train,
        config,
        train_autoencoder,
        autoencoder_pretrained,
        train_regression,
        regression_pretrained,
    )


if __name__ == "__main__":
    main()
