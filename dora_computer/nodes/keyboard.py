import pyarrow as pa 
from pynput import keyboard
from pynput.keyboard import Key, Events
from dora import Node


node = Node()
buffer_text = ""

with Events() as events:
    while True:
        dora_event = node.next(0.01)
        event = events.get(1.0)

        if isinstance(event, Events.Press):
            if event.key == Key.enter:
                # start recording audio command
                if buffer_text == 'record':
                    node.send_output(buffer_text, pa.array([buffer_text]))
                # send buffer text
                else:
                    node.send_output("buffer", pa.array([buffer_text]))
            
            elif event.key == Key.esc:
                break

        elif isinstance(event, Events.Release):
            if event.key == Key.enter:
                buffer_text = ""
                continue
            # add empty char
            if event.key == Key.space:
                buffer_text += " "
            # remove last char
            elif event.key == Key.backspace:
                buffer_text = buffer_text[:-1]
            # camera control move up
            elif event.key == Key.up:
                node.send_output("camera", pa.array(['camera/up']))
            # camera control move down
            elif event.key == Key.down:
                node.send_output("camera", pa.array(['camera/down']))
            # camera control move left
            elif event.key == Key.left:
                node.send_output("camera", pa.array(['camera/left']))
            # camera control move right
            elif event.key == Key.right:
                node.send_output("camera", pa.array(['camera/right']))
            # add character to text
            else:
                buffer_text += event.key.char
