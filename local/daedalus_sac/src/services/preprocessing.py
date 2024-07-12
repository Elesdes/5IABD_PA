import numpy as np
from scipy import signal


class EMGPreprocessor:
    def __init__(self, config):
        self.sampling_rate = config.sampling_rate
        self.bandpass_low = config.bandpass_low
        self.bandpass_high = config.bandpass_high
        self.filter_order = config.filter_order
        self.envelope_window = config.envelope_window

    def preprocess(self, emg_data):
        # Apply bandpass filter
        emg_filtered = self._bandpass_filter(emg_data)

        # Rectify the signal
        emg_rectified = np.abs(emg_filtered)

        # Apply envelope detection
        emg_envelope = self._envelope_detection(emg_rectified)

        return self._normalize(emg_envelope)

    def _bandpass_filter(self, emg_data):
        nyquist = 0.5 * self.sampling_rate
        low = self.bandpass_low / nyquist
        high = self.bandpass_high / nyquist
        b, a = signal.butter(self.filter_order, [low, high], btype="band")
        return signal.filtfilt(b, a, emg_data, axis=0)

    def _envelope_detection(self, emg_rectified):
        window_size = int(self.envelope_window * self.sampling_rate)
        return np.apply_along_axis(
            lambda x: np.convolve(x, np.ones(window_size) / window_size, mode="same"),
            axis=0,
            arr=emg_rectified,
        )

    def _normalize(self, emg_data):
        return (emg_data - np.mean(emg_data, axis=0)) / np.std(emg_data, axis=0)
