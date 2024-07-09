def get_device_id():
    device_config_path = "/home/enzol/Documents/5IABD_PA/microcontroller/id_device.cfg"

    with open(device_config_path, "r") as f:
        id_device = f.read()

    return id_device