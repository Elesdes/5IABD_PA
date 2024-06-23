import tensorflow as tf


def convert_model_to_tflite(model, save_path):
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    with open(save_path, "wb") as f:
        f.write(tflite_model)

    print(f"Model converted to TFLite and saved to {save_path}")


if __name__ == "__main__":
    model = tf.keras.models.load_model("path/to/your/model")
    convert_model_to_tflite(model, "path/to/save/model.tflite")
