import tensorflow as tf
from tf_agents.networks import actor_distribution_network
from tf_agents.agents.ppo import ppo_agent
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.networks.value_network import ValueNetwork


def create_ppo_agent(train_env):
    actor_net = actor_distribution_network.ActorDistributionNetwork(
        train_env.observation_spec(),
        train_env.action_spec(),
        fc_layer_params=(128, 128),
    )

    value_net = ValueNetwork(train_env.observation_spec(), fc_layer_params=(128, 128))

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)

    train_step_counter = tf.Variable(0)

    tf_agent = ppo_agent.PPOAgent(
        train_env.time_step_spec(),
        train_env.action_spec(),
        optimizer,
        actor_net=actor_net,
        value_net=value_net,
        num_epochs=10,
        train_step_counter=train_step_counter,
    )

    tf_agent.initialize()

    return tf_agent, train_step_counter


def create_replay_buffer(agent, train_env):
    return tf_uniform_replay_buffer.TFUniformReplayBuffer(
        data_spec=agent.collect_data_spec,
        batch_size=train_env.batch_size,
        max_length=10000,
    )


def collect_step(environment, policy, buffer):
    time_step = environment.current_time_step()
    action_step = policy.action(time_step)
    next_time_step = environment.step(action_step.action)
    traj = trajectory.from_transition(time_step, action_step, next_time_step)
    buffer.add_batch(traj)
