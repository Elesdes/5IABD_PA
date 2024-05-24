import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering, DBSCAN


def butter_lowpass(cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def lowpass_filter(data, cutoff=20, fs=1000, order=4):
    b, a = butter_lowpass(cutoff, fs, order)
    y = filtfilt(b, a, data, axis=0)
    return y


def preprocess_emg_data(data, cutoff=20, fs=1000, window_size=50):
    # Filtrage des données
    filtered_data = lowpass_filter(data, cutoff, fs)
    # Rectification
    rectified_data = np.abs(filtered_data)
    # Smoothing (lissage)
    smoothed_data = np.array([np.convolve(signal, np.ones(window_size)/window_size, mode='valid') for signal in rectified_data.T]).T
    return smoothed_data


def segment_signal(data, labels, window_size, overlap):
    segments = []
    segment_labels = []
    for start in range(0, len(data) - window_size, window_size - overlap):
        segment = data[start:start + window_size]
        segment_label = labels[start:start + window_size]
        segments.append(segment)
        segment_labels.append(segment_label[0])
    return np.array(segments), np.array(segment_labels)


def extract_features(segment):
    features = []
    features.append(np.mean(segment, axis=0))
    features.append(np.var(segment, axis=0))
    features.append(np.max(segment, axis=0))
    features.append(np.min(segment, axis=0))
    return np.concatenate(features)


# TODO: il faudra certainement séparer les bonnes données. On fera nos gestes par "Vagues". Genre 2sec rien, 2sec mouvement, 2sec rien etc...
if __name__ == '__main__':
    seed = 42
    window_size = [150, 200, 450]
    overlap = [50]
    cutoff = [10, 20]
    fs = [100, 200]
    order = 4
    np.random.seed(seed)
    final_results = []
    for w_s in window_size:
        for ol in overlap:
            for coff in cutoff:
                for f_s in fs:
                    print(f"Starting:\nWindow Size: {w_s} | Overlap: {ol} | Cutoff: {coff} | fs: {f_s}")
                    df = pd.read_csv("../calib_rec_tool/outputV2.csv")
                    df = df.drop(df.columns[0], axis=1)

                    features_to_keep = ["sensor1", "sensor2", "sensor3", "sensor4", "sensor5", "sensor6", "sensor7", "sensor8"]

                    X, y = df[features_to_keep], df.label
                    X = X.to_numpy()
                    y = y.to_numpy()
                    preprocessed_emg_data = preprocess_emg_data(X, cutoff=coff, fs=f_s, window_size=w_s)
                    segments, segment_labels = segment_signal(preprocessed_emg_data, y, w_s, ol)
                    features = np.array([extract_features(segment) for segment in segments])

                    X_train, X_test, y_train, y_test = train_test_split(features, segment_labels, test_size=0.4, random_state=seed)

                    clf = xgb.XGBClassifier()
                    #clf = AgglomerativeClustering(n_clusters=32, ).fit(X_train)
                    le = LabelEncoder()
                    y_train = le.fit_transform(y_train)
                    clf.fit(X_train, y_train)

                    y_pred = clf.predict(X_train)
                    accuracy = accuracy_score(y_train, y_pred)

                    print(f"Accuracy train: {accuracy * 100:.2f}%")

                    y_pred = clf.predict(X_test)
                    accuracy = accuracy_score(y_test, y_pred)

                    print(f"Accuracy test: {accuracy * 100:.2f}%")

                    df_validation = pd.read_csv("../calib_rec_tool/data_files/validation_moove_0.csv")
                    df_validation = df_validation.drop(df_validation.columns[0], axis=1)

                    features_to_keep = ["sensor1", "sensor2", "sensor3", "sensor4", "sensor5", "sensor6", "sensor7", "sensor8"]

                    X, y = df_validation[features_to_keep], df_validation.label
                    X = X.to_numpy()
                    y = y.to_numpy()
                    preprocessed_emg_data = preprocess_emg_data(X)
                    segments, segment_labels = segment_signal(preprocessed_emg_data, y, w_s, ol)
                    features = np.array([extract_features(segment) for segment in segments])

                    X_train, X_test, y_train, y_test = train_test_split(features, segment_labels, test_size=0.9, random_state=seed)
                    y_pred = clf.predict(X_test)
                    accuracy = accuracy_score(y_test, y_pred)

                    print(f"Accuracy validation (full class 19): {accuracy * 100:.2f}%")
                    final_results.append(([w_s, ol, coff, f_s], round(accuracy * 100, 2)))

                    df_validation = pd.read_csv("../calib_rec_tool/data_files/validation_moove_19.csv")
                    df_validation = df_validation.drop(df_validation.columns[0], axis=1)

                    features_to_keep = ["sensor1", "sensor2", "sensor3", "sensor4", "sensor5", "sensor6", "sensor7",
                                        "sensor8"]

                    X, y = df_validation[features_to_keep], df_validation.label
                    X = X.to_numpy()
                    y = y.to_numpy()
                    preprocessed_emg_data = preprocess_emg_data(X)
                    segments, segment_labels = segment_signal(preprocessed_emg_data, y, w_s, ol)
                    features = np.array([extract_features(segment) for segment in segments])

                    X_train, X_test, y_train, y_test = train_test_split(features, segment_labels, test_size=0.9,
                                                                        random_state=seed)
                    y_pred = clf.predict(X_test)
                    accuracy = accuracy_score(y_test, y_pred)

                    print(f"Accuracy validation (full class 11): {accuracy * 100:.2f}%")
    final_results = sorted(final_results, key=lambda x: x[1], reverse=True)
    for params, result in final_results:
        print(f"Params: {params}, Result: {result}")
