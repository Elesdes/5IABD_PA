import gym
from tf_agents.environments import tf_py_environment
from tf_agents.environments import suite_gym
from environments.prosthetic_hand_env import (
    ProstheticHandEnv,
)
from utils.replay_buffer import create_replay_buffer, collect_step
from config.pipeline_config import hyperparameter_optimization_config, training_config
from agents.agent_factory import create_agent
import os
import optuna


def compute_avg_return(environment, policy, num_episodes=10):
    total_return = 0.0
    for _ in range(num_episodes):
        time_step = environment.reset()
        episode_return = 0.0
        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
        total_return += episode_return
    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]


def run_pipeline(
    agent_name, save_dir="models", save_interval=training_config.save_interval
):
    train_py_env = suite_gym.wrap_env(gym.make("ProstheticHand-v0"))
    eval_py_env = suite_gym.wrap_env(gym.make("ProstheticHand-v0"))
    train_env = tf_py_environment.TFPyEnvironment(train_py_env)
    eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

    agent = create_agent(agent_name, train_env)
    replay_buffer = create_replay_buffer(agent.tf_agent, train_env)

    for _ in range(10):  # Initial population of the replay buffer
        collect_step(train_env, agent, replay_buffer)

    num_iterations = training_config.num_iterations
    for i in range(num_iterations):
        collect_step(train_env, agent, replay_buffer)
        loss = agent.train(replay_buffer)
        if i % 200 == 0:
            print(f"Iteration {i}: Loss = {loss}")

        if i % save_interval == 0 and i > 0:
            save_path = os.path.join(save_dir, f"{agent_name}_agent_{i}")
            agent.tf_agent.policy.save(save_path)
            print(f"Model saved at iteration {i} to {save_path}")

    avg_return = compute_avg_return(eval_env, agent.tf_agent.policy, num_episodes=10)
    print(f"Average Return: {avg_return}")

    final_save_path = os.path.join(save_dir, f"{agent_name}_agent_final")
    agent.tf_agent.policy.save(final_save_path)
    print(f"Final model saved to {final_save_path}")


def objective(trial, agent_type):
    train_py_env = suite_gym.wrap_env(gym.make("ProstheticHand-v0"))
    eval_py_env = suite_gym.wrap_env(gym.make("ProstheticHand-v0"))
    train_env = tf_py_environment.TFPyEnvironment(train_py_env)
    eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

    agent = create_agent(agent_type, train_env, trial)
    replay_buffer = create_replay_buffer(
        agent.tf_agent,
        train_env,
        buffer_size=hyperparameter_optimization_config.buffer_size,
    )

    # Initial population of the replay buffer
    for _ in range(10):
        collect_step(train_env, agent.tf_agent.collect_policy, replay_buffer)

    num_iterations = hyperparameter_optimization_config.num_iterations
    for i in range(num_iterations):
        collect_step(train_env, agent.tf_agent.collect_policy, replay_buffer)
        loss = agent.train(replay_buffer)
        if i % 100 == 0:
            print(f"Iteration {i}: Loss = {loss}")

    avg_return = compute_avg_return(eval_env, agent.tf_agent.policy, num_episodes=10)
    return avg_return


def run_optimization(agent_type):
    study = optuna.create_study(direction="maximize")
    study.optimize(
        lambda trial: objective(trial, agent_type),
        n_trials=hyperparameter_optimization_config.n_trials,
    )

    print("Best trial:")
    trial = study.best_trial

    print(f"  Value: {trial.value}")
    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")
