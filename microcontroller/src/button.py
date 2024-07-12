import subprocess
import time
import os
from gpiozero import Button

GPIO_PIN = 17

button = Button(GPIO_PIN)

process = None

conda_activate_script = "/home/enzol/miniforge3/etc/profile.d/conda.sh"

conda_env_name = "5IABD"

script_name = f"{os.path.dirname(__file__)}/launch.py"

def start_script():
    global process
    if process is None:
        print("Starting the Python script in the Conda environment...")
        process = subprocess.Popen(
            ['bash', '-c', f'source {conda_activate_script} && conda activate {conda_env_name} && python3 {script_name}']
        )

def stop_script():
    global process
    if process is not None:
        print("Stopping the Python script...")
        process.terminate()
        process.wait()
        process = None


print("Starting the button script...")
try:
    while True:
        button_state = button.is_pressed
        print(f"Button state: {button_state}")
        if button_state:
            if process is None:
                start_script()
        else:
            if process is not None:
                stop_script()
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    if process is not None:
        stop_script()