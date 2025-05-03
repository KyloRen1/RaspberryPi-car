import os
import numpy as np
import pyarrow as pa 

from dora import DoraStatus


class Operator:
    """
    Robot contol
    """

    def __init__(self):
        
        
        self.gimbal_position = [0, 0]
        self.robot_position = [0, 0]

        # Led color
        self.rgb = [0, 0, 0]
        self.brightness = 0

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event['type'] == 'INPUT':

            if dora_event['id'] == 'tick':
                send_output("position", pa.array(self.position + self.gimbal_position),
                    dora_event['metadata'])
            
            elif dora_event['id'] == 'gimbal_control':
                gimbal_pitch, gimbal_yaw = dora_event['value'].to_numpy()

                # update gimbal position
                if self.gimbal_position != [gimbal_pitch, gimbal_yaw]:
                    self.event = None # TODO move robot
                    self.gimbal_position[0] = gimbal_pitch
                    self.gimbal_position[1] = gimbal_yaw

            elif dora_event['id'] == 'control':
                x, y = dora_event['value'].to_numpy()

                if abs(x) > 0.1 or abs(y) > 0.1:
                    self.event = None # TODO move robot
                    self.position[0] += x 
                    self.position[1] += y

            elif dora_event['id'] == 'led':
                rgb = dora_event['value'].tp_numpy()
                
                if rgb != self.rgb:
                    self.event = None # TODO change led color
                    self.rgb = rgb

            elif dora_event['id'] == 'blaster':
                brightness = dora_event['value'].to_numpy()
                if brightness != self.brightness:
                    self.event = None # TODO change brightness
                    self.brightness = brightness

        return DoraStatus.CONTINUE