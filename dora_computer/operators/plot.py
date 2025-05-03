import os
import cv2
from dora import DoraStatus

CI = os.environ.get("CI")

CAMERA_WIDTH = 960
CAMERA_HEIGHT = 540

FONT = cv2.FONT_HERSHEY_SIMPLEX


class Operator:
    """
    Plot image and bounding box
    """

    def on_event(self, dora_event, send_output):
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == "image":

                image = dora_event['value'].to_numpy().reshape(
                    (CAMERA_HEIGHT, CAMERA_WIDTH, 3)).copy()

                if CI != "true":
                    cv2.imshow("frame", image)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        return DoraStatus.STOP

        return DoraStatus.CONTINUE