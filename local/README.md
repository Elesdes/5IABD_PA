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

TODO

## Run the Prosthesis Simulation

TODO