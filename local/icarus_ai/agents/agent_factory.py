from agents.ppo_agent import PPOAgent
from agents.td3_agent import TD3Agent
from agents.ddpg_agent import DDPGAgent
from config.pipeline_config import hyperparameter_optimization_config


def get_agent(agent_type, train_env):
    match agent_type:
        case "ppo":
            return PPOAgent(train_env)
        case "td3":
            return TD3Agent(train_env)
        case "ddpg":
            return DDPGAgent(train_env)
        case _:
            raise ValueError(f"Unsupported agent type: {agent_type}")


def create_agent(agent_type, train_env, trial=None):
    if trial is None:
        return get_agent(agent_type, train_env)

    learning_rate = trial.suggest_float(
        "learning_rate",
        hyperparameter_optimization_config.learning_rate[0],
        hyperparameter_optimization_config.learning_rate[1],
        log=True,
    )
    fc_layer_params = trial.suggest_categorical(
        "fc_layer_params", hyperparameter_optimization_config.fc_layer_params
    )
    num_epochs = trial.suggest_int(
        "num_epochs",
        hyperparameter_optimization_config.num_epochs[0],
        hyperparameter_optimization_config.num_epochs[1],
    )

    match agent_type:
        case "ppo":
            return PPOAgent(train_env, learning_rate, fc_layer_params, num_epochs)
        case "td3":
            tau = trial.suggest_float(
                "tau",
                hyperparameter_optimization_config.tau[0],
                hyperparameter_optimization_config.tau[1],
            )
            gamma = trial.suggest_float(
                "gamma",
                hyperparameter_optimization_config.gamma[0],
                hyperparameter_optimization_config.gamma[1],
            )
            policy_delay = trial.suggest_int(
                "policy_delay",
                hyperparameter_optimization_config.policy_delay[0],
                hyperparameter_optimization_config.policy_delay[1],
            )
            noise_clip = trial.suggest_float(
                "noise_clip",
                hyperparameter_optimization_config.noise_clip[0],
                hyperparameter_optimization_config.noise_clip[1],
            )
            exploration_noise = trial.suggest_float(
                "exploration_noise",
                hyperparameter_optimization_config.exploration_noise[0],
                hyperparameter_optimization_config.exploration_noise[1],
            )
            return TD3Agent(
                train_env,
                learning_rate,
                fc_layer_params,
                tau=tau,
                gamma=gamma,
                policy_delay=policy_delay,
                noise_clip=noise_clip,
                exploration_noise=exploration_noise,
            )
        case "ddpg":
            tau = trial.suggest_float(
                "tau",
                hyperparameter_optimization_config.tau[0],
                hyperparameter_optimization_config.tau[1],
            )
            gamma = trial.suggest_float(
                "gamma",
                hyperparameter_optimization_config.gamma[0],
                hyperparameter_optimization_config.gamma[1],
            )
            return DDPGAgent(
                train_env, learning_rate, fc_layer_params, tau=tau, gamma=gamma
            )
        case _:
            raise ValueError(f"Unsupported agent type: {agent_type}")
