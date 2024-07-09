import requests
import time
import os
import zipfile
import pandas as pd


MICROCONTROLLER_PATH = "/home/enzol/Documents/5IABD_PA/microcontroller"

def download_model(id_device: str):
    url = "https://icarus-gcp.oa.r.appspot.com/files/" + id_device
    result_request = requests.get(url)

    while result_request.status_code != 200:
        print("Request failed, trying again error code : " + str(result_request.status_code))
        time.sleep(60)
        result_request = requests.get(url)

    print(result_request)

    if 'Content-Disposition' in result_request.headers:
        file_name = result_request.headers['Content-Disposition'].split('filename=')[1].strip('"')
    else:
        file_name = os.path.basename(url)

    print(file_name)

    # download the model in the result of the request
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    model_name = f"{MICROCONTROLLER_PATH}/src/models/xgb_{timestamp}.pkl"

    with open(model_name, "wb") as f:
        f.write(result_request.content)

    return model_name


def send_zip_data(emg: pd.DataFrame, prediction: pd.DataFrame, id_device: str):
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    zip_filename = f"data_{timestamp}.zip"
    csv_emg = f"emg_{timestamp}.csv"
    csv_prediction = f"prediction_{timestamp}.csv"

    zip_path = f'{MICROCONTROLLER_PATH}/src/tmp/{zip_filename}'
    emg_path = f'{MICROCONTROLLER_PATH}/src/tmp/{csv_emg}'
    prediction_path = f'{MICROCONTROLLER_PATH}/src/tmp/{csv_prediction}'

    emg.to_csv(emg_path, index=False)
    prediction.to_csv(prediction_path, index=False)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(emg_path, csv_emg)
        zipf.write(prediction_path, csv_prediction)

    with open(zip_path, 'rb') as f:
        response = requests.post(f"https://icarus-gcp.oa.r.appspot.com/files/upload_data/{id_device}", files={'files': f})

    print(f"Sent {zip_filename}: {response.status_code} - {response.text}")

    os.remove(emg_path)
    os.remove(prediction_path)
    os.remove(zip_path)