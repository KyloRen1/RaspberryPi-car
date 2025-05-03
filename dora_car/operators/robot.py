import os
import time
import numpy as np
import pyarrow as pa
import sounddevice as sd 
from .raspi_car import Car

from dora import DoraStatus

class Operator:
    """
    Operator that controls robot
    """

    def __init__(self):
        self.car = Car()

    
    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event['tpye'] == 'INPUT':
            if dora_event['id'] == 'lights':
                [r, g, b] = dora_event['value'].to_numpy()
                self.car.write2register('rgbled_io1', r)
                self.car.write2register('rgbled_io2', g)
                self.car.write2register('rgbled_io3', b)

            elif dora_event['id'] == 'buzzer':
                volume = dora_event['value'].to_numpy()
                self.car.write2register('buzzer', volume)
                time.sleep(0.5)
                self.car.write2register('buzzer', 0)

            elif dora_event['id'] == 'stop':
                speed_delta = self.car.speed // 100
                speed_values = list(range(0, self.car.speed + speed_delta, speed_delta))[::-1]

                self.car.speed = 0
                for i in speed_values:  
                    self.car.write2register('motor_right', i)
                    self.car.write2register('motor_left', i)
                    time.sleep(0.005)
            
            elif dora_event['id'] == 'move':
                [speed, direction] = dora_event['value'].to_numpy()

                speed_delta = speed // 100
                speed_values = list(range(0, speed + speed_delta, speed_delta))
                direction = int(direction == 'backward')

                self.car.speed = speed

                self.car.write2register('motor_direction_right', direction)
                self.car.write2register('motor_direction_left', direction)
                for i in speed_values:  
                    self.car.write2register('motor_right', i)
                    self.car.write2register('motor_left', i)
                    time.sleep(0.005)

            elif dora_event['id'] == 'turn':
                direction = dora_event['value'].to_numpy()

                if direction == 'left':
                    degrees = list(range(90, 140, 1))
                else:
                    degrees = list(range(90, 50, -1))

                for i in degrees:   
                    self.car.write2register('servo_wheels', self.car.degrees2us(i))
                    time.sleep(0.005)

                # reset position
                time.sleep(0.5)
                self.car.write2register('servo_wheels',  self.car.degrees2us(90))

        return DoraStatus.CONTINUE