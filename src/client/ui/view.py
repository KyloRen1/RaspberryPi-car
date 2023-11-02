import tkinter as tk 
from tkmacosx import Button
from PIL import Image, ImageTk
import numpy as np 
import cv2
from urllib import request
from easydict import EasyDict


class ControllerView:
    def __init__(self, cfg):
        self.cfg = cfg 

        self.root = tk.Tk()
        self._construct_view()
        self._add_buttons()
    
    def _construct_view(self):
        self.root.title(self.cfg.view.title)
        self.root.geometry(f'{self.cfg.view.width}x{self.cfg.view.height}')

        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0)

        self.video_window = tk.Label(self.frame)
        self.video_window.grid(
            row=self.cfg.view.video.pos[0], column=self.cfg.view.video.pos[1],
            padx=self.cfg.view.video.pad[0], pady=self.cfg.view.video.pad[1],
            rowspan=self.cfg.view.video.rowspan)

    def _add_buttons(self):
        self.buttons = {}
        for button in self.cfg.view.buttons:
            self.buttons[button['key']] = Button(self.frame, text=button['name'], 
                width=button['width'], height=button['height'])
            self.buttons[button['key']].grid(
                row=button['pos'][0], column=button['pos'][1])


    def button_press(self, event):
        key = event.keysym
        if key in ['l', 's']:
             self.buttons[key].config(bg="green")
        else:
            self.buttons[key].config(bg="red")

    def button_release(self, event):
        for key in self.buttons.keys():
            self.buttons[key].config(bg="white")


    def stream(self, url):
        video = request.urlopen(url)

        bytes = b''

        while True:
            bytes += video.read(1024)
            a = bytes.find(b'\xff\xd8') #frame starting 
            b = bytes.find(b'\xff\xd9') #frame ending
            if a != -1 and b != -1:
                bytes = bytes[b+2:]
                img = cv2.imdecode(
                    np.fromstring(bytes[a:b+2], dtype=np.uint8), 
                    cv2.IMREAD_COLOR)
                self.video_window.config(image=img)
                self.root.bind("<KeyPress>", self.button_press)
                self.root.bind("<KeyRelease>", self.button_release)
                self.root.update()

        self.root.mainloop()


def main():
    cfg = EasyDict({
        'view': {
            'title': 'picar',
            'width': 600,
            'height': 400,
            'buttons': [
                {'key': 'Up',    'name': 'Up',    'pos': [0, 2], 'width': 60, 'height': 30},
                {'key': 'Down',  'name': 'Down',  'pos': [2, 2], 'width': 60, 'height': 30},
                {'key': 'Left',  'name': 'Left',  'pos': [1, 1], 'width': 60, 'height': 30},
                {'key': 'Right', 'name': 'Right', 'pos': [1, 3], 'width': 60, 'height': 30},
                {'key': 'l',     'name': 'Light', 'pos': [3, 1], 'width': 60, 'height': 30},
                {'key': 's',     'name': 'Sound', 'pos': [3, 2], 'width': 60, 'height': 30}
            ],
            'video': {
                'pos': [0, 0],
                'pad': [10, 10],
                'rowspan': 3
            }
        }
    })


    view = ControllerView(cfg)
    view.stream('/Users/bogdanivanyuk/Desktop/PySauron/data/UCF-Crime/Anomaly-Videos-Part-2/Burglary/Burglary001_x264.mp4')


if __name__ == '__main__':
    main()