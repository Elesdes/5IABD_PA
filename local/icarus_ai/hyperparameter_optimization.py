import optuna
import tensorflow as tf
from tf_agents.environments import gym_wrapper
from tf_agents.environments import tf_py_environment
from tf_agents.networks import actor_distribution_network
from tf_agents.agents.ppo import ppo_agent
from tf_agents.policies import random_tf_policy
from tf_agents.networks.value_network import ValueNetwork

from environment import ProstheticHandEnv
from ppo_agent import create_replay_buffer, collect_step

train_py_env = gym_wrapper.GymWrapper(ProstheticHandEnv())
eval_py_env = gym_wrapper.GymWrapper(ProstheticHandEnv())

train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)


def objective(trial):
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-3)
    num_epochs = trial.suggest_int("num_epochs", 5, 50)
    fc_layer_params = (
        trial.suggest_int("fc1", 64, 256),
        trial.suggest_int("fc2", 64, 256),
    )

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    actor_net = actor_distribution_network.ActorDistributionNetwork(
        train_env.observation_spec(),
        train_env.action_spec(),
        fc_layer_params=fc_layer_params,
    )

    value_net = ValueNetwork(
        train_env.observation_spec(), fc_layer_params=fc_layer_params
    )

    train_step_counter = tf.Variable(0)

    tf_agent = ppo_agent.PPOAgent(
        train_env.time_step_spec(),
        train_env.action_spec(),
        optimizer,
        actor_net=actor_net,
        value_net=value_net,
        num_epochs=num_epochs,
        train_step_counter=train_step_counter,
    )

    tf_agent.initialize()

    replay_buffer = create_replay_buffer(tf_agent, train_env)
    random_policy = random_tf_policy.RandomTFPolicy(
        train_env.time_step_spec(), train_env.action_spec()
    )

    for _ in range(1000):
        collect_step(train_env, random_policy, replay_buffer)
        experience, _ = next(
            iter(
                replay_buffer.as_dataset(
                    num_parallel_calls=3, sample_batch_size=64, num_steps=2
                )
            )
        )
        tf_agent.train(experience)

    avg_return = compute_avg_return(eval_env, tf_agent.policy, num_episodes=5)
    return avg_return


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


if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=100)
    print(study.best_trial)
