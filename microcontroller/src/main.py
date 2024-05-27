import pandas as pd
import time
import sys
from predict_model import predict
from prosthesis_management.hand import Hand
from emg_recorder import Myo, emg_mode


if __name__ == "__main__":

    hand = Hand()

    hand.reset()

    print("Hand reset done")

    model = pd.read_pickle(
        "/home/enzol/Documents/5IABD_PA/microcontroller/src/models/xgb-150-50-20-100.pkl"
    )

    print("Model loaded")

    m = Myo(sys.argv[1] if len(sys.argv) >= 2 else None, mode=emg_mode.RAW)

    myo_data = []

    def proc_emg(emg, moving, times=[]):
        myo_data.append(emg)

    m.add_emg_handler(proc_emg)
    m.connect()

    m.add_arm_handler(lambda arm, xdir: print("arm", arm, "xdir", xdir))
    m.add_pose_handler(lambda p: print("pose", p))

    m.sleep_mode(1)
    m.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs
    m.vibrate(1)
    print(f"{'*'* 10}Connected{'*'* 10}")


    myo_cols = ["sensor1", "sensor2", "sensor3", "sensor4", "sensor5", "sensor6", "sensor7", "sensor8"]
    chunk_size = 300

    try:
        while True:
            m.run()

            if len(myo_data) == chunk_size:
                data = pd.DataFrame(myo_data, columns=myo_cols)
                prediction = predict(model, data)

                print(prediction)
                myo_data = []

                hand.moveFromCategoricalList(prediction)

    except KeyboardInterrupt:
        m.disconnect()
        quit()
