import tensorflow as tf
from tensorflow.keras import layers
from config.global_config import Config


class RegressionModel(tf.keras.Model):
    def __init__(self, config: Config, autoencoder: tf.keras.Model):
        super(RegressionModel, self).__init__()
        self.config = config
        self.autoencoder = autoencoder
        self.regression_layers = self.__build_regression_layers()

    def __build_regression_layers(self):
        regression_layers = tf.keras.Sequential()
        for units in self.config.regression_hidden_layers:
            regression_layers.add(
                layers.Dense(units, activation=self.config.regression_activation)
            )
        regression_layers.add(
            layers.Dense(
                self.config.regression_output_dim,
                activation=self.config.regression_output_activation,
            )
        )
        return regression_layers

    def call(self, x):
        encoded = self.autoencoder.encoder(x)
        regression_output = self.regression_layers(encoded)
        return regression_output

    def compile(self, optimizer=None, loss=None, metrics=None):
        if optimizer is None:
            optimizer = tf.keras.optimizers.Adam(
                learning_rate=self.config.regression_learning_rate
            )
        if loss is None:
            loss = tf.keras.losses.MeanSquaredError()
        if metrics is None:
            metrics = [tf.keras.metrics.MeanAbsoluteError()]
        super(RegressionModel, self).compile(
            optimizer=optimizer, loss=loss, metrics=metrics
        )

    def fit(self, x, y, **kwargs):
        kwargs.setdefault("epochs", self.config.regression_epochs)
        kwargs.setdefault("batch_size", self.config.regression_batch_size)
        return super(RegressionModel, self).fit(x, y, **kwargs)

    def predict(self, x, **kwargs):
        return super(RegressionModel, self).predict(x, **kwargs)
