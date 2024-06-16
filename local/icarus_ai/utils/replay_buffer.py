from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
import numpy as np


def create_replay_buffer(agent, train_env):
    return tf_uniform_replay_buffer.TFUniformReplayBuffer(
        data_spec=agent.collect_data_spec,
        batch_size=train_env.batch_size,
        max_length=10000,
    )


def collect_step(environment, policy, buffer):
    time_step = environment.current_time_step()
    action_step = policy.action(time_step)
    # print(f"Action taken: {action_step.action.numpy()}")  # Log the action
    next_time_step = environment.step(action_step.action)
    # print(f"Reward received: {next_time_step.reward.numpy()}")  # Log the reward

    traj = trajectory.from_transition(time_step, action_step, next_time_step)

    # Add trajectory to the replay buffer
    buffer.add_batch(traj)

    # Check for NaN values
    if np.isnan(action_step.action.numpy()).any():
        raise ValueError("NaN detected in actions.")
    if np.isnan(next_time_step.reward.numpy()).any():
        raise ValueError("NaN detected in rewards.")
