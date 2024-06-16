import tensorflow as tf
from tf_agents.agents.ppo import ppo_agent
from tf_agents.networks import actor_distribution_network, value_network
from agents.base_agent import BaseAgent
from config.ppo_config import ppo_config


class PPOAgent(BaseAgent):
    def __init__(
        self,
        train_env,
        learning_rate: float = ppo_config.learning_rate,
        fc_layer_params=ppo_config.fc_layer_params,
        num_epochs=ppo_config.num_epochs,
        entropy_regularization: float = ppo_config.entropy_regularization,
        value_loss_weight: float = ppo_config.value_loss_weight,
        use_gae: bool = ppo_config.use_gae,
        normalize_observations: bool = ppo_config.normalize_observations,
        normalize_rewards: bool = ppo_config.normalize_rewards,
        gradient_clipping: float = ppo_config.gradient_clipping,
        value_clipping: float = ppo_config.value_clipping,
        num_parallel_calls: int = ppo_config.num_parallel_calls,
        sample_batch_size: int = ppo_config.sample_batch_size,
        num_steps: int = ppo_config.num_steps,
    ):
        super().__init__(train_env)

        self.actor_net = actor_distribution_network.ActorDistributionNetwork(
            train_env.observation_spec(),
            train_env.action_spec(),
            fc_layer_params=fc_layer_params,
        )
        self.value_net = value_network.ValueNetwork(
            train_env.observation_spec(), fc_layer_params=fc_layer_params
        )
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        self.tf_agent = ppo_agent.PPOAgent(
            train_env.time_step_spec(),
            train_env.action_spec(),
            optimizer=self.optimizer,
            actor_net=self.actor_net,
            value_net=self.value_net,
            num_epochs=num_epochs,
            entropy_regularization=entropy_regularization,
            value_pred_loss_coef=value_loss_weight,
            use_gae=use_gae,
            normalize_observations=normalize_observations,
            normalize_rewards=normalize_rewards,
            gradient_clipping=gradient_clipping,
            value_clipping=value_clipping,
            train_step_counter=tf.Variable(0),
        )
        self.tf_agent.initialize()
        self.num_parallel_calls = num_parallel_calls
        self.sample_batch_size = sample_batch_size
        self.num_steps = num_steps

    def action(self, time_step):
        action_step = self.tf_agent.collect_policy.action(time_step)
        action = action_step.action
        # print(f"Action from policy: {action.numpy()}")
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
