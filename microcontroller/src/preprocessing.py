import numpy as np
from scipy.signal import butter, filtfilt


def butter_lowpass(cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a


def lowpass_filter(data, cutoff=20, fs=1000, order=4):
    b, a = butter_lowpass(cutoff, fs, order)
    y = filtfilt(b, a, data, axis=0)
    return y


def preprocess_emg_data(data, cutoff=20, fs=1000, window_size=50):
    features_to_keep = [
        "sensor1",
        "sensor2",
        "sensor3",
        "sensor4",
        "sensor5",
        "sensor6",
        "sensor7",
        "sensor8",
    ]

    data = data[features_to_keep].to_numpy()

    # Filtrage des données
    filtered_data = lowpass_filter(data, cutoff, fs)
    # Rectification
    rectified_data = np.abs(filtered_data)
    # Smoothing (lissage)
    smoothed_data = np.array(
        [
            np.convolve(signal, np.ones(window_size) / window_size, mode="valid")
            for signal in rectified_data.T
        ]
    ).T
    return smoothed_data


def segment_signal(data, window_size, overlap):
    segments = []

    for start in range(0, len(data) - window_size, window_size - overlap):
        segment = data[start : start + window_size]
        segments.append(segment)
    return np.array(segments)


def extract_features(segment):
    features = []
    features.append(np.mean(segment, axis=0))
    features.append(np.var(segment, axis=0))
    features.append(np.max(segment, axis=0))
    features.append(np.min(segment, axis=0))
    return np.concatenate(features)
