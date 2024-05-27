import pandas as pd
import numpy as np
from preprocessing import preprocess_emg_data, segment_signal, extract_features


def int_to_categorical(x, size):
    return [int(i) for i in list(format(x, f'0{size}b'))]

def predict(model, data):
    cutoff=20
    fs = 100
    ol = 50
    w_s = 150

    preprocessed_emg_data = preprocess_emg_data(data, cutoff=cutoff, fs=fs, window_size=w_s)
    segments = segment_signal(preprocessed_emg_data, w_s, ol)
    features = np.array([extract_features(segment) for segment in segments])

    return int_to_categorical(model.predict(features)[0], 5)
