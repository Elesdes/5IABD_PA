# Setup ROS 2

This guide was heavily based on the [official ROS2 installation guide](https://docs.ros.org/en/iron/Tutorials/Advanced/Simulators/Webots/Installation-Windows.html) but simplified a little bit here and there. If you encounter any problem, please refer to the official guide.

## System Setup

### Set locale

Make sure you have a locale which supports `UTF-8`. If you are in a minimal environment (such as a docker container), the locale may be something minimal like `POSIX`. We test with the following settings. However, it should be fine if you’re using a different UTF-8 supported locale.

```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings
```

### Enable required repositories

You will need to add the ROS 2 apt repository to your system.

First ensure that the [Ubuntu Universe](https://help.ubuntu.com/community/Repositories/Ubuntu) repository is enabled.

```bash
sudo apt install software-properties-common -y
sudo add-apt-repository universe -y
```

Now add the ROS 2 GPG key with apt.

```bash
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
```

Then add the repository to your sources list.

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_
```

## Install development tools (not optional here)

```bash
sudo apt update && sudo apt install ros-dev-tools -y
```

## Setup ROS 2

Update your apt repository caches after setting up the repositories.

```bash
sudo apt update
```

ROS 2 packages are built on frequently updated Ubuntu systems. It is always recommended that you ensure your system is up to date before installing new packages.

```bash
sudo apt upgrade
```

### Desktop Install

```bash
sudo apt install ros-iron-desktop
```

### Setup environment

```bash
echo "source /opt/ros/iron/setup.sh" >> ~/.bashrc
```

## Install Webots

Run the following command in a terminal.

```bash
sudo apt-get install ros-iron-webots-ros2
```

## Test If Everything Works

WSL doesn’t support hardware acceleration (yet). Therefore, Webots should be started on Windows, while the ROS part is running inside WSL. To do so, the following commands must be run inside the WSL environment.

Setting the `WEBOTS_HOME` environment variable allows you to start a specific Webots installation (e.g. `C:\Program Files\Webots`). Use the mount point *“/mnt”* to refer to a path on native Windows.

```bash
export WEBOTS_HOME=/mnt/c/Program\ Files/Webots
```

Use the ROS 2 launch command to start demo packages (e.g. `webots_ros2_universal_robot`).

```bash
ros2 launch webots_ros2_universal_robot multirobot_launch.py
```