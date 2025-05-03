import os 
import numpy as np
import pyarrow as pa

from dora import DoraStatus
from ultralytics import YOLO


class Operator:
    """
    Infering object from images
    """

    def __init__(self,):
        self.model = YOLO("yolov8n.pt")
        self.camera_width = int(os.environ.get("CAMERA_WIDTH", 960))
        self.camera_height = int(os.environ.get("CAMERA_HEIGHT", 960))

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event['type'] == "INPUT":
            frame = dora_event['value'].to_numpy().reshape(
                (self.camera_width, self.camera_height, 3))
            frame = frame[:, :, ::-1] # BGR to RGB
            results = self.model(frame, verbose=False)  # includes NMS
            boxes = np.array(results[0].boxes.xyxy.cpu())
            conf = np.array(results[0].boxes.conf.cpu())
            label = np.array(results[0].boxes.cls.cpu())

            arrays = np.concatenate((boxes, conf[:, None], label[:, None]), axis=1)
            send_output("bbox", pa.array(arrays.ravel()), dora_event["metadata"])
        
        return DoraStatus.CONTINUE