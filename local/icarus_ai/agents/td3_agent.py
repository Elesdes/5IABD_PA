import tensorflow as tf
from tf_agents.agents.td3 import td3_agent
from tf_agents.networks import actor_distribution_network, q_network
from agents.base_agent import BaseAgent
from config.td3_config import td3_config


class TD3Agent(BaseAgent):
    def __init__(
        self,
        train_env,
        learning_rate: float = td3_config.learning_rate,
        fc_layer_params=td3_config.fc_layer_params,
        tau: float = td3_config.tau,
        gamma: float = td3_config.gamma,
        policy_delay: int = td3_config.policy_delay,
        noise_clip: float = td3_config.noise_clip,
        exploration_noise: float = td3_config.exploration_noise,
        num_parallel_calls: int = td3_config.num_parallel_calls,
        sample_batch_size: int = td3_config.sample_batch_size,
        num_steps: int = td3_config.num_steps,
    ):
        super().__init__(train_env)
        self.actor_net = actor_distribution_network.ActorDistributionNetwork(
            train_env.observation_spec(),
            train_env.action_spec(),
            fc_layer_params=fc_layer_params,
        )

        self.critic_net = q_network.QNetwork(
            input_tensor_spec=(train_env.observation_spec(), train_env.action_spec()),
            action_spec=train_env.action_spec(),
            fc_layer_params=fc_layer_params,
        )

        self.actor_optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        self.critic_optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

        self.tf_agent = td3_agent.Td3Agent(
            time_step_spec=train_env.time_step_spec(),
            action_spec=train_env.action_spec(),
            actor_network=self.actor_net,
            critic_network=self.critic_net,
            actor_optimizer=self.actor_optimizer,
            critic_optimizer=self.critic_optimizer,
            target_update_tau=tau,
            target_update_period=policy_delay,
            td_errors_loss_fn=tf.keras.losses.MeanSquaredError(),
            gamma=gamma,
            policy_noise=exploration_noise,
            noise_clip=noise_clip,
            train_step_counter=tf.Variable(0),
        )
        self.tf_agent.initialize()
        self.num_parallel_calls = num_parallel_calls
        self.sample_batch_size = sample_batch_size
        self.num_steps = num_steps

    def action(self, time_step):
        action_step = self.tf_agent.collect_policy.action(time_step)
        action = action_step.action
        if tf.reduce_any(tf.math.is_nan(action)):
            raise ValueError("NaN detected in policy action.")
        return action_step

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
