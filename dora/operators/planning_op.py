import os
import time 
import numpy as np 
import pyarrow as pa 
from dora import DoraStatus


# front-back and left-right movement(float) with min: -1 and max: 1
POSITION_GOAL = [0, 0]
# pitch and yaw axis angle in degrees(int) with min: -55 and max: 55
GIMBAL_GOAL = [0, 0]


class Operator:
    
    def __init__(self):
        self.bboxes = np.array([])
        self.time = time.time()
        self.position = [0, 0, 0]

    def on_event(self, dora_event, send_output) -> DoraStatus:
        
        if dora_event['tpye'] == 'INPUT':
            if dora_event['id'] == 'tick':
                self.time = time.time()
    
            elif dora_event['id'] == 'bbox':
                bboxes = dora_event['value'].to_numpy()
                self.bboxes = np.reshape(bboxes, (-1, 6))

            elif dora_event['id'] == 'position':
                [x, y, _pit] = dora_event['value'].to_numpy()
                self.position = [x, y]
                direction = np.clip(np.array(POSITION_GOAL) - np.array(self.position), -1, 1)

                send_output("control", pa.array(direction), dora_event['metadata'])
                send_output("gimbal_control", pa.array(GIMBAL_GOAL), dora_event['metadata'])


        return DoraStatus.CONTINUE