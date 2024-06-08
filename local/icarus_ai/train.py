import tensorflow as tf
from tf_agents.environments import gym_wrapper
from tf_agents.environments import tf_py_environment
from tf_agents.policies import random_tf_policy

from environment import ProstheticHandEnv
from ppo_agent import create_ppo_agent, create_replay_buffer, collect_step

train_py_env = gym_wrapper.GymWrapper(ProstheticHandEnv())
eval_py_env = gym_wrapper.GymWrapper(ProstheticHandEnv())

train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

tf_agent, train_step_counter = create_ppo_agent(train_env)
replay_buffer = create_replay_buffer(tf_agent, train_env)
random_policy = random_tf_policy.RandomTFPolicy(
    train_env.time_step_spec(), train_env.action_spec()
)

num_iterations = 10000
collect_steps_per_iteration = 1
log_interval = 200

for _ in range(num_iterations):
    for _ in range(collect_steps_per_iteration):
        collect_step(train_env, random_policy, replay_buffer)

    experience, _ = next(
        iter(
            replay_buffer.as_dataset(
                num_parallel_calls=3, sample_batch_size=64, num_steps=2
            )
        )
    )
    train_loss = tf_agent.train(experience).loss

    if _ % log_interval == 0:
        print(f"Step {_}: loss = {train_loss}")


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
    avg_return = compute_avg_return(eval_env, tf_agent.policy, num_episodes=10)
    print(f"Average Return: {avg_return}")
