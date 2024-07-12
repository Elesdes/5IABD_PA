import tensorflow as tf
from tensorflow.keras import layers
from config.global_config import Config


class Autoencoder(tf.keras.Model):
    def __init__(self, config: Config):
        super(Autoencoder, self).__init__()
        self.config = config
        self.input_dims = (config.sampling_rate,)
        self.encoding_dim = config.ae_encoding_dim
        self.hidden_layers = config.ae_hidden_layers
        self.activation = config.ae_activation
        self.output_activation = config.ae_output_activation

        self.encoder = self.__build_encoder()
        self.decoder = self.__build_decoder()

    def __build_encoder(self):
        encoder = tf.keras.Sequential(
            [layers.InputLayer(input_shape=self.input_dims), layers.Flatten()]
        )
        for units in self.hidden_layers:
            encoder.add(layers.Dense(units, activation=self.activation))
        encoder.add(layers.Dense(self.encoding_dim, activation=self.activation))
        return encoder

    def __build_decoder(self):
        decoder = tf.keras.Sequential(
            [layers.InputLayer(input_shape=(self.encoding_dim,))]
        )
        for units in reversed(self.hidden_layers):
            decoder.add(layers.Dense(units, activation=self.activation))
        decoder.add(
            layers.Dense(
                tf.math.reduce_prod(self.input_dims), activation=self.output_activation
            )
        )
        decoder.add(layers.Reshape(self.input_dims))
        return decoder

    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

    def compile(self, optimizer=None, loss=None):
        if optimizer is None:
            optimizer = tf.keras.optimizers.Adam(
                learning_rate=self.config.ae_learning_rate
            )
        if loss is None:
            loss = tf.keras.losses.MeanSquaredError()
        super(Autoencoder, self).compile(optimizer=optimizer, loss=loss)
