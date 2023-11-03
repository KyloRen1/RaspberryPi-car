import time
from smbus2 import SMBus

class Car:

    def __init__(self, address=0x18):
        self.address = address # address of the device to talk to over i2c/smbus

        # open i2c bus connection
        self.bus = SMBus(bus=1)
        self.bus.open(bus=1)

        # manually selected mapping (by trial and error)
        # usually indicated in product documentation
        self.cmd_map = {
            'servo_wheels': 0,
            'servo_camera_horizontal': 1,
            'servo_camera_vertical': 2,
            'motor_right': 4,
            'motor_left': 5,
            'motor_direction_right': 6,
            'motor_direction_left': 7,
            'buzzer': 8, 
            'rgbled_io1': 9,
            'rgbled_io2': 10, 
            'rgbled_io3': 11,
            'sonic': 12
        }


    def write2register(self, command: str, value: int):
        command = self.cmd_map[command]

        self.bus.write_i2c_block_data(
            i2c_addr = self.address, 
            register = command,
            data = [value>>8, value&0xff]
        )