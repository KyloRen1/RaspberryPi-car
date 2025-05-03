import os
import time
import numpy as np
import pyarrow as pa
import sounddevice as sd 
import requests

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
                # TODO read command 
                command = None
                send_output('', pa.array([command]), dora_event['metadata'])
            elif dora_event['id'] == 'image':
                image = pa.serialize(dora_event['value']).to_buffer()
                image_bytes = image.to_pybytes()
                # TODO send frame
                self.client_socket.sendall(image_bytes)
                


    