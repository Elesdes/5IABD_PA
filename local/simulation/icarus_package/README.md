# Create conda env with python == 3.10 in wsl2

## Install Requirements

Run the following command 

```bash
pip install -r requirements.txt
```

```bash
conda install -c conda-forge libstdcxx-ng
```

## Install dependencies

```bash
sudo apt install ros-iron-gazebo-ros-pkgs
```

```bash
sudo apt install ros-iron-joint-state-publisher
```

```bash
sudo apt install ros-iron-joint-state-publisher-gui
```

## Build colcon in icarus_package

```bash
colcon build
```


## Source 

```bash
source install/setup.bash
```

## Launch rviz visualization

```bash
ros2 launch icarus_package display.launch.py
```
