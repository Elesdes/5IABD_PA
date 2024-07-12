import pandas as pd


def load_dataset(*, filename: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = pd.read_csv(
        filepath_or_buffer=filename,
        sep=",",
        usecols=[
            "timestamp",
            "sensor1",
            "sensor2",
            "sensor3",
            "sensor4",
            "sensor5",
            "sensor6",
            "sensor7",
            "sensor8",
            "label",
        ],
    )

    emg_data = data.drop(columns=["label"])
    labels = data["label"]

    return emg_data, labels
