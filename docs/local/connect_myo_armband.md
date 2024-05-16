# Connect Myo Armband

Before following any of these steps, make sure that you have the Myo Armband and the USB dongle plugged into your computer.

## Windows

Nothing more to do, the Myo Armband should be automatically detected by the Windows system.

## WSL2 / Linux (Ubuntu)

Follow this link to install the latest version of package [usbipd-win](https://github.com/dorssel/usbipd-win/releases).

Next steps must be run on an **Administrator** PowerShell :

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

Now, open your WSL distro and run the following command to make sure that it's binded:

```bash
lsusb
```
