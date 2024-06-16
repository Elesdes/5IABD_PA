import click
from pipelines.training_pipeline import run_pipeline, run_optimization


@click.command(
    help="""
    Run an agent pipeline or hyperparameter optimization.

    The agent type can be 'ppo', 'td3', or 'ddpg'.
    The mode can be 'train' or 'optimize'.

    By default, the agent type is 'ppo' and the mode is 'train'.

    Example:
    python local/icarus_ai/main.py --agent_type ppo --mode train
    python local/icarus_ai/main.py --agent_type td3 --mode optimize
    """
)
@click.option(
    "--agent_type",
    type=click.Choice(["ppo", "td3", "ddpg"]),
    default="ppo",
    help="Agent type to run.",
)
@click.option(
    "--mode",
    type=click.Choice(["train", "optimize"]),
    default="train",
    help="Mode to run: 'train' or 'optimize'.",
)
def run(agent_type: str = "ppo", mode: str = "train"):
    match mode:
        case "train":
            run_pipeline(agent_type)
        case "optimize":
            run_optimization(agent_type)
        case _:
            print("Unknown mode. Please use 'train' or 'optimize'.")


if __name__ == "__main__":
    run()
