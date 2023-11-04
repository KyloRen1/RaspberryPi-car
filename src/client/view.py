import tkinter as tk 
from tkmacosx import Button
from PIL import Image, ImageTk
import cv2
import requests
import ujson as json
from easydict import EasyDict


class ControllerView:
    def __init__(self, cfg, url, stream_port, comm_port):
        self.cfg = cfg

        self.car_url = url 
        self.stream_port = stream_port
        self.comm_port = comm_port
        self.header = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

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

        r = requests.post(
            f'{self.car_url}:{self.comm_port}', 
            data=json.dumps({'key': key, 'status' : 'pressed'}), 
            headers=self.header)
        #r = requests.get(
        #    f'{self.car_url}:{self.comm_port}/{key}/pressed'
        #)
        assert r.status_code == 200

    def button_release(self, event):
        key = event.keysym
        self.buttons[key].config(bg="white")
        r = requests.post(
            f'{self.car_url}:{self.comm_port}', 
            data=json.dumps({'key': key, 'status' : 'released'}), 
            headers=self.header)
        #r = requests.get(
        #    f'{self.car_url}:{self.comm_port}/{key}/released'
        #)
        assert r.status_code == 200


    def stream(self, url=None):
        if url is None:
            url = f'{self.car_url}:{self.stream_port}' 
        video = cv2.VideoCapture(url)
        while video.isOpened():
            ret, frame = video.read()
            if ret:
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
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


    view = ControllerView(
        cfg, 
        url='http://192.168.1.150', 
        stream_port='8091/?action=stream', 
        comm_port='5000'
    )
    view.stream()

if __name__ == '__main__':
    main()