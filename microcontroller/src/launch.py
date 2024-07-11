import pandas as pd
import time
import os
from call_api import download_model, send_zip_data
from predict_model import predict
from prosthesis_management.hand import Hand
from emg_recorder import Myo, emg_mode
from stable_baselines3 import PPO
from device import get_device_id

MICROCONTROLLER_PATH = os.path.dirname(__file__)

id_device = get_device_id()

model_name = download_model(id_device)

# hand = Hand()

# hand.reset()

# print("Hand reset done")

# ppo_model = PPO.load("/home/enzol/Documents/5IABD_PA/microcontroller/src/models/PPO_hand_prosthesis_model")

model = pd.read_pickle(model_name)

print("Model loaded")

# m = Myo(sys.argv[1] if len(sys.argv) >= 2 else None, mode=emg_mode.RAW)

# myo_data = []

# def proc_emg(emg, moving, times=[]):
#     myo_data.append(emg)

# m.add_emg_handler(proc_emg)
# m.connect()

# m.add_arm_handler(lambda arm, xdir: print("arm", arm, "xdir", xdir))
# m.add_pose_handler(lambda p: print("pose", p))

# m.sleep_mode(1)
# m.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs
# m.vibrate(1)
# print(f"{'*'* 10}Connected{'*'* 10}")

myo_cols = [
    "sensor1",
    "sensor2",
    "sensor3",
    "sensor4",
    "sensor5",
    "sensor6",
    "sensor7",
    "sensor8",
]
chunk_size = 300

data = pd.read_csv(f'{MICROCONTROLLER_PATH}/data/data.csv')

data = data[myo_cols]

myo_data = []
total_emg_data = []
total_predictions = []
file_index = 0
api_chunk_size = 30000

try:
    for index, row in data.iterrows():
        myo_data.append(row.tolist())
        total_emg_data.append(row.tolist())

        if len(myo_data) == chunk_size:
            df_chunk = pd.DataFrame(myo_data, columns=myo_cols)
            prediction = predict(model, df_chunk)

            print(prediction)
            myo_data = []

            total_predictions.append(str(prediction))

        if len(total_emg_data) >= api_chunk_size:
            df_emg_total = pd.DataFrame(total_emg_data, columns=myo_cols)
            df_predictions_total = pd.DataFrame(total_predictions, columns=['prediction'])
            file_index += 1
            send_zip_data(df_emg_total, df_predictions_total, id_device)
            total_emg_data = []
            total_predictions = []
            print(f"Sent {file_index} files")

except KeyboardInterrupt:
    quit()


# try:
#     while True:
#         m.run()

#         if len(myo_data) == chunk_size:
#             data = pd.DataFrame(myo_data, columns=myo_cols)
#             prediction = predict(model, data)

#             print(prediction)
#             myo_data = []

#             hand.moveFromCategoricalList(prediction)

# except KeyboardInterrupt:
#     m.disconnect()
#     quit()