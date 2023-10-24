import tkinter as tk 
import cv2
from PIL import Image, ImageTk
import time 
import imageio

def button_event(event):
    print('Turn right', event.keysym)


# download video at: http://www.html5videoplayer.net/videos/toystory.mp4
video_name = '/Users/bogdanivanyuk/Desktop/PySauron/data/UCF-Crime/Anomaly-Videos-Part-2/Burglary/Burglary001_x264.mp4'
video = imageio.get_reader(video_name)


def video_frame_generator():
    def current_time():
        return time.time()

    start_time = current_time()
    _time = 0
    for frame, image in enumerate(video.iter_data()):

        # turn video array into an image and reduce the size
        image = Image.fromarray(image)
        image.thumbnail((750, 750))

        # make image in a tk Image and put in the label
        image = ImageTk.PhotoImage(image)

        # introduce a wait loop so movie is real time -- asuming frame rate is 24 fps
        # if there is no wait check if time needs to be reset in the event the video was paused
        _time += 1 / 24
        run_time = current_time() - start_time
        while run_time < _time:
            run_time = current_time() - start_time
        else:
            if run_time - _time > 0.1:
                start_time = current_time()
                _time = 0

        yield frame, image

def main():

    root = tk.Tk()
    root.title('PiCar')
    # Create a label in the frame
    lmain = tk.Label(root)
    lmain.pack()

    movie_frame = video_frame_generator()


    video = cv2.VideoCapture(
        '/Users/bogdanivanyuk/Desktop/PySauron/data/UCF-Crime/Anomaly-Videos-Part-2/Burglary/Burglary001_x264.mp4')
    # function for video streaming

    counter = 0
    while counter < 100:
        frame_number, frame = next(movie_frame)
        lmain.config(image=frame)
        root.bind("<KeyRelease>", button_event)
        root.update()

    root.mainloop()


if __name__ == '__main__':
    main()