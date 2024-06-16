class BaseAgent:
    def __init__(self, train_env):
        self.train_env = train_env

    def train(self, replay_buffer):
        raise NotImplementedError("This method should be overridden by subclasses.")
