import os
import time
import numpy as np
import pyarrow as pa

from dora import DoraStatus

class Operator:
    """
    Operator that controls robot
    """

    def __init__(self):
        pass 

    def on_event(self, dora_event, send_output) -> DoraStatus:

        if dora_event["type"] == 'INPUT':
            if dora_event['id'] == 'tick':
                # TODO read image
                send_output('image', pa.array(image), dora_event["metadata"])
        
            elif dora_event['id'] == 'cmd':
                image = pa.serialize(dora_event['value']).to_buffer()
                image_bytes = image.to_pybytes()
                # TODO send command

                self.client_socket.sendall(image_bytes)
                


    