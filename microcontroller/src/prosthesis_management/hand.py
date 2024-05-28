import time
import random
from typing import Final
from adafruit_servokit import ServoKit


MIN_IMP: Final = [500, 500, 500, 500, 500]
MAX_IMP: Final = [2500, 2500, 2500, 2500, 2500]
MIN_ANGLE: Final = [0, 0, 0, 0, 0]
MAX_ANGLE: Final = [80, 140, 140, 140, 140]


# Fingers order
# thumb, index, middle, ring, pinky


class Hand:
    def __init__(self):
        self.pca = ServoKit(channels=16)

        self.nbServo = 5

        for i in range(self.nbServo):
            self.pca.servo[i].set_pulse_width_range(MIN_IMP[i], MAX_IMP[i])

        self.servos = [self.pca.servo[servo_idx] for servo_idx in range(self.nbServo)]

    def move(self, servoId: int, angle: int):
        if angle < MIN_ANGLE[servoId] or angle > MAX_ANGLE[servoId]:
            raise ValueError(f"Angle {angle} is out of range for servo {servoId}")

        self.servos[servoId].angle = angle

    def moveAll(self, angles: list):
        for i in range(self.nbServo):
            if angles[i] < MIN_ANGLE[i] or angles[i] > MAX_ANGLE[i]:
                raise ValueError(f"Angle {angles[i]} is out of range for servo {i}")

            self.servos[i].angle = angles[i]

    def moveRandom(self):
        angles = [
            random.randint(MIN_ANGLE[servo_idx], MAX_ANGLE[servo_idx])
            for servo_idx in range(self.nbServo)
        ]
        self.moveAll(angles)

    def moveAllToMin(self):
        self.moveAll([MIN_ANGLE[i] for i in range(self.nbServo)])

    def moveAllToMax(self):
        self.moveAll([MAX_ANGLE[i] for i in range(self.nbServo)])

    def moveFromCategoricalList(self, categorical: list):
        angles = [
            MIN_ANGLE[i] if categorical[i] == 0 else MAX_ANGLE[i]
            for i in range(self.nbServo)
        ]
        self.moveAll(angles)

    def reset(self):
        self.moveAllToMin()
        time.sleep(2)
        self.moveAllToMax()
        time.sleep(2)
        self.moveAllToMin()


if __name__ == "__main__":
    hand = Hand()
    hand.reset()
