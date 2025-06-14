"""
The MIT License (MIT)
Copyright (c) 2020 PerlinWarp
Copyright (c) 2014 Danny Zhu

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

	Original by dzhu
		https://github.com/dzhu/myo-raw

	Edited by Fernando Cosentino
		http://www.fernandocosentino.net/pyoconnect

	Edited by Alvaro Villoslada (Alvipe)
		https://github.com/Alvipe/myo-raw

	Edited by PerlinWarp
		https://github.com/PerlinWarp/pyomyo

Warning, when using this library in a multithreaded way,
know that any function called on Myo_Raw, may try to use the serial port,
in windows if this is tried from a seperate thread you will get a permission error
"""

import enum
import re
import struct
import sys
import threading

import serial
from serial.tools.list_ports import comports


def pack(fmt, *args):
    """
    Packs data according to the given format.

    Parameters
    ----------
    fmt : str
        The format string.
    *args : tuple
        The values to pack.

    Returns
    -------
    bytes
        The packed data.
    """
    return struct.pack("<" + fmt, *args)


def unpack(fmt, *args):
    """
    Unpacks data according to the given format.

    Parameters
    ----------
    fmt : str
        The format string.
    *args : tuple
        The values to unpack.

    Returns
    -------
    tuple
        The unpacked data.
    """
    return struct.unpack("<" + fmt, *args)


def multichr(ords):
    """
    Converts a list of ordinal values to a byte string.

    Parameters
    ----------
    ords : list of int
        The ordinal values.

    Returns
    -------
    bytes or str
        The byte string or string.
    """
    if sys.version_info[0] >= 3:
        return bytes(ords)
    else:
        return "".join(map(chr, ords))


def multiord(b):
    """
    Converts a byte string to a list of ordinal values.

    Parameters
    ----------
    b : bytes or str
        The byte string or string.

    Returns
    -------
    list of int
        The ordinal values.
    """
    if sys.version_info[0] >= 3:
        return list(b)
    else:
        return map(ord, b)


class emg_mode(enum.Enum):
    NO_DATA = 0  # Do not send EMG data
    PREPROCESSED = 1  # Sends 50Hz rectified and band pass filtered data
    FILTERED = 2  # Sends 200Hz filtered but not rectified data
    RAW = 3  # Sends raw 200Hz data from the ADC ranged between -128 and 127


class Arm(enum.Enum):
    UNKNOWN = 0
    RIGHT = 1
    LEFT = 2


class XDirection(enum.Enum):
    UNKNOWN = 0
    X_TOWARD_WRIST = 1
    X_TOWARD_ELBOW = 2


class Pose(enum.Enum):
    REST = 0
    FIST = 1
    WAVE_IN = 2
    WAVE_OUT = 3
    FINGERS_SPREAD = 4
    THUMB_TO_PINKY = 5
    UNKNOWN = 255


class Packet(object):
    """
    Represents a packet of data.
    """

    def __init__(self, ords):
        """
        Initializes a Packet instance.

        Parameters
        ----------
        ords : list of int
            The ordinal values of the packet.
        """
        self.typ = ords[0]
        self.cls = ords[2]
        self.cmd = ords[3]
        self.payload = multichr(ords[4:])

    def __repr__(self):
        """
        Returns a string representation of the Packet.

        Returns
        -------
        str
            The string representation.
        """
        return "Packet(%02X, %02X, %02X, [%s])" % (
            self.typ,
            self.cls,
            self.cmd,
            " ".join("%02X" % b for b in multiord(self.payload)),
        )


class BT(object):
    """
    Implements the non-Myo-specific details of the Bluetooth protocol.
    """

    def __init__(self, tty):
        """
        Initializes a BT instance.

        Parameters
        ----------
        tty : str
            The serial port to use.
        """
        self.ser = serial.Serial(port=tty, baudrate=9600, dsrdtr=1)
        self.buf = []
        self.lock = threading.Lock()
        self.handlers = []

    def recv_packet(self):
        """
        Receives a packet from the serial port.

        Returns
        -------
        Packet or None
            The received packet or None if no packet was received.
        """
        n = self.ser.inWaiting()  # Windows fix

        while True:
            c = self.ser.read()
            if not c:
                return None

            ret = self.proc_byte(ord(c))
            if ret:
                if ret.typ == 0x80:
                    self.handle_event(ret)
                    # Windows fix
                    if n >= 5096:
                        print("Clearning", n)
                        self.ser.flushInput()
                    # End of Windows fix
                return ret

    def proc_byte(self, c):
        """
        Processes a byte of data.

        Parameters
        ----------
        c : int
            The byte to process.

        Returns
        -------
        Packet or None
            The processed packet or None if the packet is incomplete.
        """
        if not self.buf:
            if c in [
                0x00,
                0x80,
                0x08,
                0x88,
            ]:  # [BLE response pkt, BLE event pkt, wifi response pkt, wifi event pkt]
                self.buf.append(c)
            return None
        elif len(self.buf) == 1:
            self.buf.append(c)
            self.packet_len = 4 + (self.buf[0] & 0x07) + self.buf[1]
            return None
        else:
            self.buf.append(c)

        if self.packet_len and len(self.buf) == self.packet_len:
            p = Packet(self.buf)
            self.buf = []
            return p
        return None

    def handle_event(self, p):
        """
        Handles an event packet.

        Parameters
        ----------
        p : Packet
            The event packet.
        """
        for h in self.handlers:
            h(p)

    def add_handler(self, h):
        """
        Adds a handler for event packets.

        Parameters
        ----------
        h : function
            The handler function.
        """
        self.handlers.append(h)

    def remove_handler(self, h):
        """
        Removes a handler for event packets.

        Parameters
        ----------
        h : function
            The handler function.
        """
        try:
            self.handlers.remove(h)
        except ValueError:
            pass

    def wait_event(self, cls, cmd):
        """
        Waits for a specific event packet.

        Parameters
        ----------
        cls : int
            The class of the event.
        cmd : int
            The command of the event.

        Returns
        -------
        Packet
            The received event packet.
        """
        res = [None]

        def h(p):
            if p.cls == cls and p.cmd == cmd:
                res[0] = p

        self.add_handler(h)
        while res[0] is None:
            self.recv_packet()
        self.remove_handler(h)
        return res[0]

    def connect(self, addr):
        """
        Connects to a device with the given address.

        Parameters
        ----------
        addr : list of int
            The address of the device.

        Returns
        -------
        Packet
            The response packet.
        """
        return self.send_command(6, 3, pack("6sBHHHH", multichr(addr), 0, 6, 6, 64, 0))

    def get_connections(self):
        """
        Gets the list of connections.

        Returns
        -------
        Packet
            The response packet.
        """
        return self.send_command(0, 6)

    def discover(self):
        """
        Starts device discovery.

        Returns
        -------
        Packet
            The response packet.
        """
        return self.send_command(6, 2, b"\x01")

    def end_scan(self):
        """
        Ends device discovery.

        Returns
        -------
        Packet
            The response packet.
        """
        return self.send_command(6, 4)

    def disconnect(self, h):
        """
        Disconnects a device.

        Parameters
        ----------
        h : int
            The handle of the connection.

        Returns
        -------
        Packet
            The response packet.
        """
        return self.send_command(3, 0, pack("B", h))

    def read_attr(self, con, attr):
        """
        Reads an attribute.

        Parameters
        ----------
        con : int
            The connection handle.
        attr : int
            The attribute handle.

        Returns
        -------
        Packet
            The response packet.
        """
        self.send_command(4, 4, pack("BH", con, attr))
        return self.wait_event(4, 5)

    def write_attr(self, con, attr, val):
        """
        Writes to an attribute.

        Parameters
        ----------
        con : int
            The connection handle.
        attr : int
            The attribute handle.
        val : bytes
            The value to write.

        Returns
        -------
        Packet
            The response packet.
        """
        self.send_command(4, 5, pack("BHB", con, attr, len(val)) + val)
        return self.wait_event(4, 1)

    def send_command(self, cls, cmd, payload=b"", wait_resp=True):
        """
        Sends a command.

        Parameters
        ----------
        cls : int
            The class of the command.
        cmd : int
            The command.
        payload : bytes, optional
            The payload (default is b'').
        wait_resp : bool, optional
            Whether to wait for a response (default is True).

        Returns
        -------
        Packet
            The response packet.
        """
        s = pack("4B", 0, len(payload), cls, cmd) + payload
        self.ser.write(s)

        while True:
            p = self.recv_packet()
            # no timeout, so p won't be None
            if p.typ == 0:
                return p
            # not a response: must be an event
            self.handle_event(p)


class Myo(object):
    """
    Implements the Myo-specific communication protocol.
    """

    def __init__(self, tty=None, mode=1):
        """
        Initializes a Myo instance.

        Parameters
        ----------
        tty : str, optional
            The serial port to use (default is None).
        mode : int, optional
            The EMG mode (default is 1).
        """
        if tty is None:
            tty = self.detect_tty()
        if tty is None:
            raise ValueError("Myo dongle not found!")

        self.bt = BT(tty)
        self.conn = None
        self.emg_handlers = []
        self.imu_handlers = []
        self.arm_handlers = []
        self.pose_handlers = []
        self.battery_handlers = []
        self.mode = mode

    def detect_tty(self):
        """
        Detects the serial port for the Myo dongle.

        Returns
        -------
        str or None
            The serial port or None if not found.
        """
        print(comports())
        for p in comports():
            print(p)
            if re.search(r"PID=2458:0*1", p[2]):
                print("using device:", p[0])
                return p[0]

        return None

    def run(self):
        """
        Receives packets from the Myo device.
        """
        self.bt.recv_packet()

    def connect(self, addr=None):
        """
        Connects to a Myo device.

        Parameters
        ----------
        addr : list of int, optional
            The MAC address (default is None).
        """
        # stop everything from before
        self.bt.end_scan()
        self.bt.disconnect(0)
        self.bt.disconnect(1)
        self.bt.disconnect(2)

        # start scanning
        if addr is None:
            print("scanning...")
            self.bt.discover()
            while True:
                p = self.bt.recv_packet()
                print("scan response:", p)

                if p.payload.endswith(
                    b"\x06\x42\x48\x12\x4A\x7F\x2C\x48\x47\xB9\xDE\x04\xA9\x01\x00\x06\xD5"
                ):
                    addr = list(multiord(p.payload[2:8]))
                    break
            self.bt.end_scan()
        # connect and wait for status event
        conn_pkt = self.bt.connect(addr)
        self.conn = multiord(conn_pkt.payload)[-1]
        self.bt.wait_event(3, 0)

        # get firmware version
        fw = self.read_attr(0x17)
        _, _, _, _, v0, v1, v2, v3 = unpack("BHBBHHHH", fw.payload)
        print("firmware version: %d.%d.%d.%d" % (v0, v1, v2, v3))

        self.old = v0 == 0

        if self.old:
            # don't know what these do; Myo Connect sends them, though we get data
            # fine without them
            self.write_attr(0x19, b"\x01\x02\x00\x00")
            # Subscribe for notifications from 4 EMG data channels
            self.write_attr(0x2F, b"\x01\x00")
            self.write_attr(0x2C, b"\x01\x00")
            self.write_attr(0x32, b"\x01\x00")
            self.write_attr(0x35, b"\x01\x00")

            # enable EMG data
            self.write_attr(0x28, b"\x01\x00")
            # enable IMU data
            self.write_attr(0x1D, b"\x01\x00")

            # Sampling rate of the underlying EMG sensor, capped to 1000. If it's
            # less than 1000, emg_hz is correct. If it is greater, the actual
            # framerate starts dropping inversely. Also, if this is much less than
            # 1000, EMG data becomes slower to respond to changes. In conclusion,
            # 1000 is probably a good value.
            C = 1000
            emg_hz = 50
            # strength of low-pass filtering of EMG data
            emg_smooth = 100

            imu_hz = 50

            # send sensor parameters, or we don't get any data
            self.write_attr(
                0x19,
                pack(
                    "BBBBHBBBBB", 2, 9, 2, 1, C, emg_smooth, C // emg_hz, imu_hz, 0, 0
                ),
            )

        else:
            name = self.read_attr(0x03)
            print("device name: %s" % name.payload)

            # enable IMU data
            self.write_attr(0x1D, b"\x01\x00")
            # enable on/off arm notifications
            self.write_attr(0x24, b"\x02\x00")
            # enable EMG notifications
            if self.mode == emg_mode.PREPROCESSED:
                # Send the undocumented filtered 50Hz.
                print("Starting filtered, 0x01")
                self.start_filtered()  # 0x01
            elif self.mode == emg_mode.FILTERED:
                print("Starting raw filtered, 0x02")
                self.start_raw()  # 0x02
            elif self.mode == emg_mode.RAW:
                print("Starting raw, unfiltered, 0x03")
                self.start_raw_unfiltered()  # 0x03
            else:
                print("No EMG mode selected, not sending EMG data")
            # Stop the Myo Disconnecting
            self.sleep_mode(1)

            # enable battery notifications
            self.write_attr(0x12, b"\x01\x10")

        # add data handlers
        def handle_data(p):
            if (p.cls, p.cmd) != (4, 5):
                return

            c, attr, typ = unpack("BHB", p.payload[:4])
            pay = p.payload[5:]

            if attr == 0x27:
                # Unpack a 17 byte array, first 16 are 8 unsigned shorts, last one an unsigned char
                vals = unpack("8HB", pay)
                # not entirely sure what the last byte is, but it's a bitmask that
                # seems to indicate which sensors think they're being moved around or
                # something
                emg = vals[:8]
                moving = vals[8]
                self.on_emg(emg, moving)
            # Read notification handles corresponding to the for EMG characteristics
            elif attr == 0x2B or attr == 0x2E or attr == 0x31 or attr == 0x34:
                """According to http://developerblog.myo.com/myocraft-emg-in-the-bluetooth-protocol/
                each characteristic sends two sequential readings in each update,
                so the received payload is split in two samples. According to the
                Myo BLE specification, the data type of the EMG samples is int8_t.
                """
                emg1 = struct.unpack("<8b", pay[:8])
                emg2 = struct.unpack("<8b", pay[8:])
                self.on_emg(emg1, 0)
                self.on_emg(emg2, 0)
            # Read IMU characteristic handle
            elif attr == 0x1C:
                vals = unpack("10h", pay)
                quat = vals[:4]
                acc = vals[4:7]
                gyro = vals[7:10]
                self.on_imu(quat, acc, gyro)
            # Read classifier characteristic handle
            elif attr == 0x23:
                typ, val, xdir, _, _, _ = unpack("6B", pay)

                if typ == 1:  # on arm
                    self.on_arm(Arm(val), XDirection(xdir))
                elif typ == 2:  # removed from arm
                    self.on_arm(Arm.UNKNOWN, XDirection.UNKNOWN)
                elif typ == 3:  # pose
                    self.on_pose(Pose(val))
            # Read battery characteristic handle
            elif attr == 0x11:
                battery_level = ord(pay)
                self.on_battery(battery_level)
            else:
                print("data with unknown attr: %02X %s" % (attr, p))

        self.bt.add_handler(handle_data)

    def write_attr(self, attr, val):
        """
        Writes to an attribute.

        Parameters
        ----------
        attr : int
            The attribute handle.
        val : bytes
            The value to write.
        """
        if self.conn is not None:
            self.bt.write_attr(self.conn, attr, val)

    def read_attr(self, attr):
        """
        Reads an attribute.

        Parameters
        ----------
        attr : int
            The attribute handle.

        Returns
        -------
        Packet
            The response packet.
        """
        if self.conn is not None:
            return self.bt.read_attr(self.conn, attr)
        return None

    def disconnect(self):
        """
        Disconnects from the Myo device.
        """
        if self.conn is not None:
            self.bt.disconnect(self.conn)

    def sleep_mode(self, mode):
        """
        Sets the sleep mode.

        Parameters
        ----------
        mode : int
            The sleep mode.
        """
        self.write_attr(0x19, pack("3B", 9, 1, mode))

    def power_off(self):
        """
        Powers off the Myo armband.

        This function puts the Myo into deep sleep.
        """
        self.write_attr(0x19, b"\x04\x00")

    def start_raw(self):
        """
        Sends 200Hz, non-rectified EMG signal.

        Subscribes to the four EMG notification characteristics and sends
        the corresponding commands to the Myo device.
        """
        self.write_attr(0x2C, b"\x01\x00")  # Subscribe to EmgData0Characteristic
        self.write_attr(0x2F, b"\x01\x00")  # Subscribe to EmgData1Characteristic
        self.write_attr(0x32, b"\x01\x00")  # Subscribe to EmgData2Characteristic
        self.write_attr(0x35, b"\x01\x00")  # Subscribe to EmgData3Characteristic
        self.write_attr(0x19, b"\x01\x03\x02\x01\x01")

    def start_filtered(self):
        """
        Sends 50Hz filtered and rectified EMG signal.

        Subscribes to the EMG notification characteristics and sends
        the corresponding commands to the Myo device.
        """
        self.write_attr(0x28, b"\x01\x00")
        self.write_attr(0x19, b"\x01\x03\x01\x01\x00")

    def start_raw_unfiltered(self):
        """
        Sends raw, unfiltered EMG signal.

        Subscribes to the four EMG notification characteristics and sends
        the corresponding commands to the Myo device.
        """
        self.write_attr(0x2C, b"\x01\x00")  # Subscribe to EmgData0Characteristic
        self.write_attr(0x2F, b"\x01\x00")  # Subscribe to EmgData1Characteristic
        self.write_attr(0x32, b"\x01\x00")  # Subscribe to EmgData2Characteristic
        self.write_attr(0x35, b"\x01\x00")  # Subscribe to EmgData3Characteristic
        self.write_attr(0x19, b"\x01\x03\x03\x01\x00")

    def mc_start_collection(self):
        """
        Starts data collection for Myo Connect.
        """
        self.write_attr(0x28, b"\x01\x00")  # Subscribe to EMG notifications
        self.write_attr(0x1D, b"\x01\x00")  # Subscribe to IMU notifications
        self.write_attr(0x24, b"\x02\x00")  # Subscribe to classifier indications
        self.write_attr(
            0x19, b"\x01\x03\x01\x01\x01"
        )  # Set EMG and IMU, payload size = 3, EMG on, IMU on, classifier on
        self.write_attr(0x28, b"\x01\x00")  # Subscribe to EMG notifications
        self.write_attr(0x1D, b"\x01\x00")  # Subscribe to IMU notifications
        self.write_attr(
            0x19, b"\x09\x01\x01\x00\x00"
        )  # Set sleep mode, payload size = 1, never go to sleep, don't know, don't know
        self.write_attr(0x1D, b"\x01\x00")  # Subscribe to IMU notifications
        self.write_attr(
            0x19, b"\x01\x03\x00\x01\x00"
        )  # Set EMG and IMU, payload size = 3, EMG off, IMU on, classifier off
        self.write_attr(0x28, b"\x01\x00")  # Subscribe to EMG notifications
        self.write_attr(0x1D, b"\x01\x00")  # Subscribe to IMU notifications
        self.write_attr(
            0x19, b"\x01\x03\x01\x01\x00"
        )  # Set EMG and IMU, payload size = 3, EMG on, IMU on, classifier off

    def mc_end_collection(self):
        """
        Ends data collection for Myo Connect.
        """
        self.write_attr(0x28, b"\x01\x00")
        self.write_attr(0x1D, b"\x01\x00")
        self.write_attr(0x24, b"\x02\x00")
        self.write_attr(0x19, b"\x01\x03\x01\x01\x01")
        self.write_attr(0x19, b"\x09\x01\x00\x00\x00")
        self.write_attr(0x1D, b"\x01\x00")
        self.write_attr(0x24, b"\x02\x00")
        self.write_attr(0x19, b"\x01\x03\x00\x01\x01")
        self.write_attr(0x28, b"\x01\x00")
        self.write_attr(0x1D, b"\x01\x00")
        self.write_attr(0x24, b"\x02\x00")
        self.write_attr(0x19, b"\x01\x03\x01\x01\x01")

    def vibrate(self, length):
        """
        Vibrates the Myo device.

        Parameters
        ----------
        length : int
            The length of the vibration (1, 2, or 3).
        """
        if length in range(1, 4):
            self.write_attr(0x19, pack("3B", 3, 1, length))

    def set_leds(self, logo, line):
        """
        Sets the LEDs of the Myo device.

        Parameters
        ----------
        logo : list of int
            The RGB values for the logo LED.
        line : list of int
            The RGB values for the line LED.
        """
        self.write_attr(0x19, pack("8B", 6, 6, *(logo + line)))

    def add_emg_handler(self, h):
        """
        Adds an EMG handler.

        Parameters
        ----------
        h : function
            The handler function.
        """
        self.emg_handlers.append(h)

    def add_imu_handler(self, h):
        """
        Adds an IMU handler.

        Parameters
        ----------
        h : function
            The handler function.
        """
        self.imu_handlers.append(h)

    def add_pose_handler(self, h):
        """
        Adds a pose handler.

        Parameters
        ----------
        h : function
            The handler function.
        """
        self.pose_handlers.append(h)

    def add_arm_handler(self, h):
        """
        Adds an arm handler.

        Parameters
        ----------
        h : function
            The handler function.
        """
        self.arm_handlers.append(h)

    def add_battery_handler(self, h):
        """
        Adds a battery handler.

        Parameters
        ----------
        h : function
            The handler function.
        """
        self.battery_handlers.append(h)

    def on_emg(self, emg, moving):
        """
        Calls the EMG handlers.

        Parameters
        ----------
        emg : list of int
            The EMG data.
        moving : int
            The moving flag.
        """
        for h in self.emg_handlers:
            h(emg, moving)

    def on_imu(self, quat, acc, gyro):
        """
        Calls the IMU handlers.

        Parameters
        ----------
        quat : list of int
            The quaternion data.
        acc : list of int
            The acceleration data.
        gyro : list of int
            The gyroscope data.
        """
        for h in self.imu_handlers:
            h(quat, acc, gyro)

    def on_pose(self, p):
        """
        Calls the pose handlers.

        Parameters
        ----------
        p : Pose
            The pose data.
        """
        for h in self.pose_handlers:
            h(p)

    def on_arm(self, arm, xdir):
        """
        Calls the arm handlers.

        Parameters
        ----------
        arm : Arm
            The arm data.
        xdir : XDirection
            The x-direction data.
        """
        for h in self.arm_handlers:
            h(arm, xdir)

    def on_battery(self, battery_level):
        """
        Calls the battery handlers.

        Parameters
        ----------
        battery_level : int
            The battery level.
        """
        for h in self.battery_handlers:
            h(battery_level)


if __name__ == "__main__":
    m = Myo(sys.argv[1] if len(sys.argv) >= 2 else None, mode=emg_mode.RAW)

    def proc_emg(emg, moving, times=[]):
        print(emg)

    m.add_emg_handler(proc_emg)
    m.connect()

    m.add_arm_handler(lambda arm, xdir: print("arm", arm, "xdir", xdir))
    m.add_pose_handler(lambda p: print("pose", p))
    # m.add_imu_handler(lambda quat, acc, gyro: print('quaternion', quat))
    m.sleep_mode(1)
    m.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs
    m.vibrate(1)
    print(f"{'*'* 10}Connected{'*'* 10}")

    buffer = []

    try:
        while True:
            m.run()

    except KeyboardInterrupt:
        m.disconnect()
        quit()
