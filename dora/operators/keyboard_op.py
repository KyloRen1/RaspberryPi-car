import pyarrow as pa 
from pynput import keyboard
from pynput.keyboard import Key, Events
from dora import Node


node = Node()
buffer_text = ""
ctrl = False
text = list()
cursor = 0

NODE_TOPIC = ['record', 'send', 'ask', 'change']

with keyboard.Events() as events:
    while True:
        dora_event = node.next(0.01)