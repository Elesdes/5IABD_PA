import os


def get_device_id():
    print(os.path.join(os.path.dirname(__file__)))
    device_config_path = os.path.join(os.path.dirname(__file__), "../id_device.cfg")

    with open(device_config_path, "r") as f:
        id_device = f.read()

    return id_device


test = get_device_id()
print(test)