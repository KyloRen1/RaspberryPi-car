import os 
import whisper 
import pyarrow as pa 

from dora import DoraStatus

class Operator:
    """
    OpenAI Whisper to transform speech to text
    """

    def __init__(self):
        model_name = os.environ.get('WHISPER_MODEL_NAME', "base.en")
        self.model = whisper.load_model(model_name)
        print(f'Model {model_name} loaded')

    def on_event(self, dora_event, send_output) -> DoraStatus:
        
        if dora_event['type'] == 'INPUT':
            audio = dora_event['value'].to_numpy()
            audio = whisper.pad_or_trim(audio)
            result = self.model.transcribe(audio, language="en")
            send_output("text", pa.array([result["text"].strip()]), dora_event["metadata"])
        
        return DoraStatus.CONTINUE