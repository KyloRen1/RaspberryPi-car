import tkinter as tk 
from tkmacosx import Button
from PIL import Image, ImageTk
import time 
import imageio
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

        self.video_window = tk.Label(self.root)
        self.video_window.grid(
            row=self.cfg.view.video.pos[0], column=self.cfg.view.video.pos[1])

    def _add_buttons(self):
        button_width = self.cfg.view.button.vehicle.width
        button_height = self.cfg.view.button.vehicle.height

        self.buttons = {}

        for button in self.cfg.view.button.vehicle.buttons:
            self.buttons[button['name']] = Button(self.root, text=button['name'], 
                width=button_width, height=button_height)
            self.buttons[button['name']].grid(
                row=button['pos'][0], column=button['pos'][1])


    def button_press(self, event):
        key = event.keysym
        print('Turn: ', key)
        self.buttons[key].config(bg="red")

    def button_release(self, event):
        for name in self.buttons.keys():
            self.buttons[name].config(bg="white")

    def connect_stream(self, url):
        video = imageio.get_reader(url)
        start_time = time.time()
        _time = 0
        for frame, image in enumerate(video.iter_data()):

            # turn video array into an image and reduce the size
            image = Image.fromarray(image)

            # make image in a tk Image and put in the label
            image = ImageTk.PhotoImage(image)

            # introduce a wait loop so movie is real time -- asuming frame rate is 24 fps
            # if there is no wait check if time needs to be reset in the event the video was paused
            _time += 1 / 24
            run_time = time.time() - start_time
            while run_time < _time:
                run_time = time.time() - start_time
            else:
                if run_time - _time > 0.1:
                    start_time = time.time()
                    _time = 0

            yield frame, image


    def stream(self, url):
        video = self.connect_stream(url)

        while True:
            frame_number, frame = next(video)
            self.video_window.config(image=frame)
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
            'button': {
                'vehicle': {
                    'width': 60,
                    'height': 30,
                    'buttons': [
                        {'name': 'Up',    'pos': [1, 1]},
                        {'name': 'Down',  'pos': [2, 2]},
                        {'name': 'Left',  'pos': [3, 3]},
                        {'name': 'Right', 'pos': [4, 4]},
                    ]
                }
            },
            'video': {
                'pos': [0, 0]
            }
        }
    })


    view = ControllerView(cfg)
    view.stream('/Users/bogdanivanyuk/Desktop/PySauron/data/UCF-Crime/Anomaly-Videos-Part-2/Burglary/Burglary001_x264.mp4')


if __name__ == '__main__':
    main()