from dataclasses import asdict, dataclass


@dataclass
class PreprocessingSchema:
    sampling_rate: int = 1_000  # Hz
    bandpass_low: int = 20  # Hz
    bandpass_high: int = 450  # Hz
    filter_order: int = 4
    envelope_window: float = 0.2  # seconds
