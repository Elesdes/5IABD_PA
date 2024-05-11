# Run Simulation on Local

## Install Requirements

Run the following command in the `local` directory to install the required packages:

```bash
pip install -r requirements.txt
```

## Make PyBullet Work

```bash
yes | sudo apt update && sudo apt upgrade
sudo ln -s /usr/lib/wsl/lib/libcuda.so.1 /usr/local/cuda/lib64/libcuda.so
yes | sudo apt-get install xorg-dev libgl1-mesa-dri libgl1-mesa-glx mesa-utils libglu1-mesa-dev freeglut3-dev mesa-common-dev
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
export MESA_GL_VERSION_OVERRIDE=3.3
export MESA_GLSL_VERSION_OVERRIDE=330
sudo ln -sf /opt/bin/nvidia-smi /usr/bin/nvidia-smi
```

You can then check if PyBullet works by running the notebook `notebooks/pybullet/pybullet_hello_world.ipynb`.

## Run EMG Recording

### Running EMG Recording on Windows

Run the script located in `emg/emg_recording.py` to record EMG data.

### Running EMG Recording on WSL

Follow this link to install the latest version of package [usbipd-win](https://github.com/dorssel/usbipd-win/releases).

Next steps must be run on an Administrator PowerShell :

- To see the list of available devices :

```pwsh
usbipd list
```

You must be able to see the device you want to bind to WSL.

- To bind the device to WSL :

```pwsh
usbipd bind --busid <busid>
usbipd attach --wsl --busid <busid>
```

Now, open your WSL distro and run the following command to make sure that it's binded :

```bash
lsusb
```

Finally, you can run the script located in `emg/emg_recording.py` to record EMG data.

## Run the Prosthesis Simulation

TODO