import os
import re
import time 
import json 
import pylcs
import torch
import pyarrow as pa 
from dora import DoraStatus
from transformers import AutoModelForCausalLM, AutoTokenizer


CODE_MODIFIER_TEMPLATE = """
### Instruction
Respond with one block of modified code only in ```python block. No explaination.
```python
{code}
```
{user_message}
### Response:
"""


MESSAGE_SENDER_TEMPLATE = """
### Instruction
You're a json expert. Format your response as a json with a topic and a data field in a ```json block.  No explaination needed. No code needed.
The schema for those json are:
- led: Int[3] (min: 0, max: 255)
- blaster: Int (min: 0, max: 128)
- control: Int[3] (min: -1, max: 1)
- rotation: Int[2] (min: -55, max: 55)
- line: Int[4]
The response should look like this: 
```json
 [
  {{ "topic": "line", "data": [10, 10, 90, 10] }},
]
```
{user_message}
### Response:
"""

ASSISTANT_TEMPLATE = """
### Instruction
You're a helpuf assistant named dora. 
Reply with a short message. No code needed. 
User {user_message}
### Response:
"""



class Operator:
    
    def __init__(self):
        #self.MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "gpt-4-turbo-preview")
        self.MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "smallcloudai/Refact-1_6B-fim")
        self.gpt = True if 'gpt' in self.MODEL_NAME.lower() else False
        if not self.gpt:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.MODEL_NAME, use_fast=True, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.MODEL_NAME, device_map="auto", trust_remote_code=True, revision="main")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"


    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event['type'] == 'INPUT':

            if dora_event['id'] == 'code_modifier':
                input = dora_event['value'][0].as_py()

                with open(input['path'], "r", encoding="utf8") as f:
                    code = f.read()

                user_message = input['user_message']
                if self.gpt:
                    output = self.chatGPT(CODE_MODIFIER_TEMPLATE.format(code=code, user_message=user_message))
                else:
                    output = self.llm(CODE_MODIFIER_TEMPLATE.format(code=code, user_message=user_message))

                source_code = self._replace_code_in_source(code, output)
                send_output("modified_file", pa.array([{
                    "raw": source_code, "path": input['path'], "response": output, "prompt": input['user_message']}]), 
                    dora_event['metadata'])
                send_output("assistant_message", pa.array([output]), dora_event['metadata'])
                    
            
            elif dora_event['id'] == 'message_sender':
                user_message = dora_event['value'][0].as_py()
                if self.gpt:
                    output = self.chatGPT(MESSAGE_SENDER_TEMPLATE.format(user_message=user_message))
                else:
                    output = self.llm(MESSAGE_SENDER_TEMPLATE.format(user_message=user_message))
                output = self._extract_json_code_blocks(output)

                try:
                    output = json.loads(output)
                    if not isinstance(output, list):
                        output = [output]

                    # Iterate over all outputs
                    for out in output:
                        if not isinstance(out["data"], list):
                            out["data"] = [out["data"]]

                        if out["topic"] in ["led", "blaster"]:
                            send_output(out["topic"], pa.array(out["data"]), dora_event["metadata"])
                            send_output("assistant_message", pa.array([f"sent: {out}"]), dora_event["metadata"])
                        else:
                            send_output("assistant_message", pa.array([f"Could not send as topic was not available: {out}"]), dora_event["metadata"])
                except:
                    send_output("assistant_message", pa.array([f"Could not parse json: {output}"]), dora_event["metadata"])

            elif dora_event['id'] == 'assistant':
                user_message = dora_event['value'][0].as_py()
                if self.gpt:
                    output = self.chatGPT(ASSISTANT_TEMPLATE.format(user_message=user_message))
                else:
                    output = self.llm(ASSISTANT_TEMPLATE.format(user_message=user_message))
                send_output("assistant_message", pa.array([output]), dora_event['metadata'])

        return DoraStatus.CONTINUE


    def llm(self, prompt):
        ''' LLM text generation given prompt input '''
        input = self.tokenizer(prompt, return_tensors='pt')
        input_ids = input.input_ids.to(self.device)
        attention_mask = input['attention_mask']

        output = self.model.generate(
            inputs=input_ids,
            # temperature=0.7,
            do_sample=False,
            # top_p=0.95,
            # top_k=40, 
            max_new_tokens=512,
            attention_mask=attention_mask,
            eos_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)[len(prompt):]


    def chatGPT(self, prompt):
        ''' ChatGPT text generation given prompt input '''
        import openai

        response = openai.ChatCompletion.create(
            model=self.MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        answer = response.choices[0].message.content
        return answer


    def _extract_json_code_blocks(self, text):
        """
        Extracts json code blocks from the given text that are enclosed in triple backticks with a json language identifier.
        Parameters:
        - text: A string that may contain one or more json code blocks.
        Returns:
        - A list of strings, where each string is a block of json code extracted from the text.
        """
        pattern = r"```json\n(.*?)\n```"
        matches = re.findall(pattern, text, re.DOTALL)
        if len(matches) == 0:
            pattern = r"```json\n(.*?)(?:\n```|$)"
            matches = re.findall(pattern, text, re.DOTALL)
            if len(matches) == 0:
                return [text]
        return matches


    def _replace_code_in_source(self, src_code, replacement_block):
        """
        Replace the best matching block in the source_code with the replacement_block, considering variable block lengths.
        """
        replacement_block = self._extract_python_code_blocks(replacement_block)[0]
        start_index, end_index = self._find_best_match_location(src_code, replacement_block)
        if start_index != -1 and end_index != -1:
            # Replace the best matching part with the replacement block
            new_source = (
                src_code[:start_index] + replacement_block + src_code[end_index:]
            )
            return new_source
        else:
            return src_code

    
    def _extract_python_code_blocks(self, text):
        """
        Extracts Python code blocks from the given text that are enclosed in triple backticks with a python language identifier.
        Parameters:
        - text: A string that may contain one or more Python code blocks.
        Returns:
        - A list of strings, where each string is a block of Python code extracted from the text.
        """
        pattern = r"```python\n(.*?)\n```"
        matches = re.findall(pattern, text, re.DOTALL)
        if len(matches) == 0:
            pattern = r"```python\n(.*?)(?:\n```|$)"
            matches = re.findall(pattern, text, re.DOTALL)
            if len(matches) == 0:
                return [text]
            else:
                matches = [self._remove_last_line(matches[0])]

        return matches


    def _find_best_match_location(self, src_code, trg_block):
        """
        Find the best match for the target_block within the source_code by searching line by line,
        considering blocks of varying lengths.
        """
        source_lines = src_code.split("\n")
        target_lines = trg_block.split("\n")

        best_similarity = 0
        best_start_index = 0
        best_end_index = -1

        # Iterate over the source lines to find the best matching range for all lines in target_block
        for start_index in range(len(source_lines) - len(target_lines) + 1):
            for end_index in range(start_index + len(target_lines), len(source_lines) + 1):
                current_window = "\n".join(source_lines[start_index:end_index])
                current_similarity = self._calculate_similarity(current_window, trg_block)
                if current_similarity > best_similarity:
                    best_similarity = current_similarity
                    best_start_index = start_index
                    best_end_index = end_index

        # Convert line indices back to character indices for replacement
        char_start_index = len("\n".join(source_lines[:best_start_index])) + (
            1 if best_start_index > 0 else 0
        )
        char_end_index = len("\n".join(source_lines[:best_end_index]))

        return char_start_index, char_end_index


    def _calculate_similarity(self, source, target):
        """
        Calculate a similarity score between the source and target strings.
        This uses the edit distance relative to the length of the strings.
        """
        edit_distance = pylcs.edit_distance(source, target)
        max_length = max(len(source), len(target))
        # Normalize the score by the maximum possible edit distance (the length of the longer string)
        similarity = 1 - (edit_distance / max_length)
        return similarity


    def _remove_last_line(self, python_code):
        """
        Removes the last line from a given string of Python code.
        Parameters:
        - python_code: A string representing Python source code.
        Returns:
        - A string with the last line removed.
        """
        lines = python_code.split("\n")  # Split the string into lines
        if lines:  # Check if there are any lines to remove
            lines.pop()  # Remove the last line
        return "\n".join(lines)  # Join the remaining lines back into a string

if __name__ == "__main__":
    op = Operator()

    # Path to the current file
    current_file_path = __file__

    # Directory of the current file
    current_directory = os.path.dirname(current_file_path)

    path = current_directory + "/planning_op.py"
    with open(path, "r", encoding="utf8") as f:
        raw = f.read()

    op.on_event({
        "type": "INPUT",
        "id": "code_modifier",
        "value": pa.array([{
            "path": path,
            "user_message": "change planning to make gimbal follow bounding box ",
        }]),
        "metadata": []
    }, print)