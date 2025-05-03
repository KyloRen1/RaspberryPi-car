import os
import time

import cv2
import numpy as np
import pyarrow as pa

from dora import DoraStatus


class Operator:
    """
    Sending image from webcam to the dataflow
    """

    def __init__(self):
        self.CI = os.environ.get("CI")# TODO
        self.CAMERA_WIDTH = 960 # TODO
        self.CAMERA_HEIGHT = 540# TODO
        self.CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", 0))

        self.video_capture = cv2.VideoCapture(self.CAMERA_INDEX)
        self.start_time = time.time()
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAMERA_WIDTH)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAMERA_HEIGHT)

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if  dora_event["type"] == "INPUT":
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.resize(frame, (self.CAMERA_WIDTH, self.CAMERA_HEIGHT))
            else:
                frame = np.zeros((self.CAMERA_HEIGHT, self.CAMERA_WIDTH, 3), dtype=np.uint8)
                cv2.putText(frame,
                    "No Webcam was found at index %d" % (self.CAMERA_INDEX),
                    (int(30), int(30)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (255, 255, 255), 2, 1)
                if self.CI != "true":
                    return DoraStatus.CONTINUE
            send_output("image", pa.array(frame.ravel()), dora_event["metadata"])
        elif  dora_event["type"] == "STOP":
            print("received stop")
        else:
            print("received unexpected event:",  dora_event["type"])

        if time.time() - self.start_time < 10000:
            return DoraStatus.CONTINUE
        else:
            return DoraStatus.STOP

    def __del__(self):
        self.video_capture.release()
