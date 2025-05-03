import os 
import time 

import cv2
import numpy as np
import pyarrow as pa 

from dora import DoraStatus 


CI = os.environ.get("CI")

CAMERA_WIDTH = int(os.environ.get("CAMERA_WIDTH", 960))
CAMERA_HEIGHT = int(os.environ.get("CAMERA_HEIGHT", 540))
CAMERA_INDEX = int(os.environ.get("CAMERA_INDEX", 2))


class Operator:
    """
    Sending image from webcam to the dataflow
    """

    def __init__(self):
        self.video_cap = cv2.VideoCapture(CAMERA_INDEX)
        self.start_time = time.time()
        self.video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event['type'] == "INPUT":
            ret, frame = self.video_cap.read()
            if ret: 
                frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
            else:
                # if camera is not available return error image
                frame = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), dtype=np.uint8)
                cv2.putText(frame, 
                    "No Webcam was found at index %d" % (CAMERA_INDEX),
                    (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, 1)
                
                if CI != "true":
                    return DoraStatus.CONTINUE

            send_output("image", pa.array(frame.ravel()), dora_event['metadata'])

        elif dora_event['type'] == "STOP":
            print("received stop")
        else:
            print("received unexpected event: ", dora_event['type'])

        if time.time() - self.start_time < 10000:
            return DoraStatus.CONTINUE
        else:
            return DoraStatus.STOP

    def __del__(self):
        self.video_cap.release()


if __name__ == "__main__":
    op = Operator()
    op.on_event(
        {"type": "INPUT", "id": "tick", "value": pa.array([0]), "metadata": []}, print
    )