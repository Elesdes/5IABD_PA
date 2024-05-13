### DISCLAIMER ###
# THIS SCRIPT ONLY RUNS ON WINDOWS.
# NEW VERSION SOON TO BE RELEASED TO BE HANDLED ON LINUX.
### DISCLAIMER ###

import pybullet as p
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import logging
import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=f"local/logs/environment_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log",
    force=True
)


urdf_file = (
    "local/simulation/environment/robot_description/urdf/prosthesis_v2_copy.urdf"
)
full_path = os.path.abspath(urdf_file)


def connect_to_bullet():
    if not p.isConnected():
        connection_id = p.connect(p.GUI)
        if connection_id == -1:
            logging.warning("Failed to connect to PyBullet.")
            raise Exception("Failed to establish a connection with the physics server.")
        logging.info(f"Connected to PyBullet with connection ID: {connection_id}")
        p.resetSimulation()
        p.setGravity(0, 0, 0)
        p.setTimeStep(1 / 240)
    else:
        logging.info("Already connected to PyBullet.")


def load_robot():
    connect_to_bullet()
    p.resetSimulation()
    p.setGravity(0, 0, 0)
    robot_id = p.loadURDF(full_path, useFixedBase=True)
    logging.info(f"Robot loaded from {full_path}.")
    return robot_id


def reload_robot():
    p.disconnect()
    robot_id = load_robot()
    set_initial_camera_view(robot_id)
    joint_params = setup_joint_control(robot_id)
    return robot_id, joint_params


def visualize_joint_axes(robot_id: int) -> None:
    for joint_index in range(p.getNumJoints(robot_id)):
        link_state = p.getLinkState(robot_id, joint_index)
        joint_pos = link_state[0]
        p.addUserDebugLine(
            joint_pos,
            [joint_pos[0] + 0.1, joint_pos[1], joint_pos[2]],
            [1, 0, 0],
            parentObjectUniqueId=robot_id,
            parentLinkIndex=joint_index,
        )


def set_initial_camera_view(robot_id: int) -> None:
    base_position = p.getBasePositionAndOrientation(robot_id)[0]
    camera_target_position = [base_position[0], base_position[1], base_position[2]]
    camera_distance = 0.25
    camera_yaw = 0
    camera_pitch = -50
    p.resetDebugVisualizerCamera(
        cameraDistance=camera_distance,
        cameraYaw=camera_yaw,
        cameraPitch=camera_pitch,
        cameraTargetPosition=camera_target_position,
    )
    logging.info("Initial camera view set.")


def setup_joint_control(robot_id: int) -> list[tuple[int, int]]:
    joint_names = [
        "Revolute_0",
        "Revolute_4",
        "Revolute_7",
        "Revolute_10",
        "Revolute_13",
    ]
    joint_params = []
    for joint_index in range(p.getNumJoints(robot_id)):
        joint_info = p.getJointInfo(robot_id, joint_index)
        joint_name = joint_info[1].decode("utf-8")
        if joint_name in joint_names:
            joint_range = joint_info[8:10]
            param_id = p.addUserDebugParameter(
                joint_name, joint_range[0], joint_range[1], 0
            )
            joint_params.append((joint_index, param_id))
    return joint_params


def control_joints(
    robot_id: int, joint_params: list[tuple[int, int]], running: bool
) -> None:
    while running.is_set():
        for joint_index, param_id in joint_params:
            target_position = p.readUserDebugParameter(param_id)
            p.setJointMotorControl2(
                robot_id,
                joint_index,
                p.POSITION_CONTROL,
                targetPosition=target_position,
            )
        p.stepSimulation()
        time.sleep(0.01)


class URDFChangeHandler(FileSystemEventHandler):
    def __init__(self, running_event):
        self.control_thread = None
        self.running = running_event

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == full_path:
            logging.warning(f"Detected change in: {event.src_path}")
            robot_id, joint_params = reload_robot()
            if self.control_thread and self.control_thread.is_alive():
                self.running.clear()
                self.control_thread.join()
            self.running.set()
            self.control_thread = threading.Thread(
                target=control_joints, args=(robot_id, joint_params, self.running)
            )
            self.control_thread.start()


def start_monitoring(running_event):
    event_handler = URDFChangeHandler(running_event)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(full_path), recursive=False)
    observer.start()
    try:
        while running_event.is_set():
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


def generate_environment() -> None:
    running_event = threading.Event()
    running_event.set()

    robot_id = load_robot()
    set_initial_camera_view(robot_id)
    joint_params = setup_joint_control(robot_id)

    monitoring_thread = threading.Thread(target=start_monitoring, args=(running_event,))
    control_thread = threading.Thread(
        target=control_joints, args=(robot_id, joint_params, running_event)
    )

    # Set threads as daemon to ensure they terminate when main thread terminates.
    monitoring_thread.daemon = True
    control_thread.daemon = True

    monitoring_thread.start()
    control_thread.start()

    try:
        # Using a loop to keep the main thread checking for the running status.
        while running_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt, shutting down...")
        running_event.clear()  # Signal to threads to stop

    # Clean-up: Wait for threads to finish gracefully.
    monitoring_thread.join()
    control_thread.join()
    logging.info("All threads have been cleanly shutdown.")


if __name__ == "__main__":
    generate_environment()
