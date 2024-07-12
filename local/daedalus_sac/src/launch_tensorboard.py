from tensorboard import program
import click
import os
from config.global_config import Config
import subprocess

COMPONENTS: str = ["autoencoder", "regression", "sac"]


def open_browser(url):
    try:
        subprocess.run(["cmd.exe", "/c", "start", url], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to open browser. Please manually visit: {url}")


@click.command()
@click.option(
    "--run", type=str, required=True, help="Run number (e.g., 20240710_232601)"
)
def main(run: str, config: Config = Config()):
    tb = program.TensorBoard()

    logdir_spec = ",".join(
        [
            f"{component}:{os.path.join(config.logs, f'run_{run}', 'tensorboard', component)}"
            for component in COMPONENTS
        ]
    )

    tb_args = [None, "--logdir_spec", logdir_spec]

    tb.configure(argv=tb_args)
    url = tb.launch()
    print(f"TensorBoard started at {url}")

    open_browser(url)

    input("Press Enter to quit TensorBoard...")


if __name__ == "__main__":
    main()
