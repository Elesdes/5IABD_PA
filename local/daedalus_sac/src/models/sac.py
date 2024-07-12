from stable_baselines3 import SAC
from config.global_config import Config


def load_sac_model(env, config: Config) -> SAC:
    return SAC(
        config.sac_policy,
        env,
        learning_rate=config.sac_learning_rate,
        buffer_size=config.sac_buffer_size,
        learning_starts=config.sac_learning_starts,
        batch_size=config.sac_batch_size,
        tau=config.sac_tau,
        gamma=config.sac_gamma,
        train_freq=config.sac_train_freq,
        gradient_steps=config.sac_gradient_steps,
        ent_coef=config.sac_ent_coef,
        target_update_interval=config.sac_target_update_interval,
        target_entropy=config.sac_target_entropy,
        use_sde=config.sac_use_sde,
        sde_sample_freq=config.sac_sde_sample_freq,
        use_sde_at_warmup=config.sac_use_sde_at_warmup,
        tensorboard_log=config.tensorboard_log_sac,
    )
