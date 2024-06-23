import tensorflow as tf
from tf_agents.agents.ddpg import ddpg_agent
from tf_agents.networks import actor_distribution_network, q_network
from agents.base_agent import BaseAgent
from config.ddpg_config import ddpg_config


class DDPGAgent(BaseAgent):
    def __init__(
        self,
        train_env,
        learning_rate: float = ddpg_config.learning_rate,
        fc_layer_params=ddpg_config.fc_layer_params,
        tau: float = ddpg_config.tau,
        gamma: float = ddpg_config.gamma,
        num_parallel_calls: int = ddpg_config.num_parallel_calls,
        sample_batch_size: int = ddpg_config.sample_batch_size,
        num_steps: int = ddpg_config.num_steps,
    ):
        super().__init__(train_env)
        self.actor_net = actor_distribution_network.ActorDistributionNetwork(
            train_env.observation_spec(),
            train_env.action_spec(),
            fc_layer_params=fc_layer_params,
        )
        self.critic_net = q_network.QNetwork(
            (train_env.observation_spec(), train_env.action_spec()),
            observation_fc_layer_params=(fc_layer_params[0],),
            action_fc_layer_params=None,
            joint_fc_layer_params=(fc_layer_params[1],),
        )
        self.actor_optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        self.critic_optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        self.tf_agent = ddpg_agent.DdpgAgent(
            train_env.time_step_spec(),
            train_env.action_spec(),
            actor_network=self.actor_net,
            critic_network=self.critic_net,
            actor_optimizer=self.actor_optimizer,
            critic_optimizer=self.critic_optimizer,
            td_errors_loss_fn=tf.keras.losses.MeanSquaredError(),
            gamma=gamma,
            target_update_tau=tau,
        )
        self.tf_agent.initialize()
        self.num_parallel_calls = num_parallel_calls
        self.sample_batch_size = sample_batch_size
        self.num_steps = num_steps

    def train(self, replay_buffer):
        experience, _ = next(
            iter(
                replay_buffer.as_dataset(
                    num_parallel_calls=self.num_parallel_calls,
                    sample_batch_size=self.sample_batch_size,
                    num_steps=self.num_steps,
                )
            )
        )
        return self.tf_agent.train(experience).loss
