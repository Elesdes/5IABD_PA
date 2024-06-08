import tensorflow as tf

policy_save_dir = "saved_policy"
loaded_policy = tf.saved_model.load(policy_save_dir)

converter = tf.lite.TFLiteConverter.from_saved_model(policy_save_dir)
tflite_model = converter.convert()

with open("policy_model.tflite", "wb") as f:
    f.write(tflite_model)
