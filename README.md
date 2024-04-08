# ICARUS - 5AIBD Annual Project 2023-2024

ICARUS is an open-source student project aimed at developing a system for controlling a non-invasive 3D-printed hand prosthesis through EMG signals using deep reinforcement learning algorithms, thereby exploring the interactions between technology and the human body by leveraging concepts related to human-machine interactions.

## Architecture

![Architecture](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&layers=1&nav=1#G1LHZJae9Cc4FhaZvyflEOcjzSfZXzGHtx)

## Project Setup

### Install WSL Distribution

In a Windows terminal, run the following commands to install WSL and set it up:

```pwsh
wsl --install -d Ubuntu
wsl -s Ubuntu
```

#### From here, all commands are run in WSL

### Install Anaconda

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
```

After running the above commands, reboot WSL.

### Prepare Conda Environment

Before this step, you need to access the project's root directory with WSL.

```bash
conda update --all -y
conda create -n ICARUS python=3.11 -y
conda activate ICARUS
yes | pip install -r requirements.txt
```

### Make PyBullet Work

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

## How To Run Locally

### Run EMG Recording

TODO

### Run the Prosthesis Simulation

TODO

### Run FastAPI Local Server

Execute the code in `api/src/main.py`.

## Work Based On

This project has been influenced by the following works:

- [TactHand](https://github.com/pslade2/TactHand) (Open source model of a 3D-printed hand prosthesis)
- [PyBullet](https://github.com/bulletphysics/bullet3) (Open source physics engine)

We would like to express our gratitude to these authors for their groundbreaking work and contributions to the open-source community.

## Authors

- [Erwan DUPREY](https://github.com/ErwanDuprey)
- [Enzo LEONARDO](https://github.com/Leonardeaux)
- [Juan MAUBRAS](https://github.com/Elesdes)
