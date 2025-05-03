import os
import numpy as np
import pyarrow as pa
import sounddevice as sd 

from dora import DoraStatus

class Operator:
    """
    Microphone operator that records the audio
    """

    def __init__(self):
        self.sample_rate = int(os.environ.get("SAMPLE_RATE", 16_000))
        self.max_duration = int(os.environ.get("MAX_RECORDING_DURATION", 10))

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event['type'] == 'INPUT':
            audio_data = sd.rec(
                self.sample_rate * self.max_duration,
                samplerate=self.sample_rate,
                channels=1, 
                dtype=np.int16, 
                blocking=True
            )
            audio_data = audio_data.ravel().astype(np.float32) / 32768.0
            if len(audio_data) > 0:
                send_output("audio", pa.array(audio_data), dora_event['metadata'])
        elif dora_event["type"] == "INPUT":
            print("Microphone is not recording", dora_event["value"][0].as_py())
        
        return DoraStatus.CONTINUE