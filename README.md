# ICARUS - 5AIBD Annual Project 2023-2024 (In Progress)

ICARUS is an open-source student project aimed at developing a system for controlling a non-invasive 3D-printed hand prosthesis through EMG signals using deep reinforcement learning algorithms, thereby exploring the interactions between technology and the human body by leveraging concepts related to human-machine interactions.

## Architecture

![Architecture](/docs/architecture.jpg)

## Project Global Setup

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

### If you want to run the API on your local machine, or even run the simulation, please refer to these READMEs :
- [API](/cloud/README.md)
- [Simulation](/local/README.md)

## Work Based On

This project has been influenced by the following works:

- [TactHand](https://github.com/pslade2/TactHand) (Open source model of a 3D-printed hand prosthesis)
- [InMoov](https://inmoov.fr/hand-i2/) (An other open source model of a 3D-printed hand prosthesis)
- [PyBullet](https://github.com/bulletphysics/bullet3) (Open source physics engine for Python)
- [Pyomyo](https://github.com/PerlinWarp/pyomyo) (Open source code for interfacing with Myo armbands)

We would like to express our gratitude to these authors for their groundbreaking work and contributions to the open-source community.

## Authors

- [Erwan DUPREY](https://github.com/ErwanDuprey)
- [Enzo LEONARDO](https://github.com/Leonardeaux)
- [Juan MAUBRAS](https://github.com/Elesdes)
