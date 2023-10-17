import random

import toga
from toga.colors import BLUE, RED
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ControllerView(toga.App):
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        #   Also make the window non-resizable and non-minimizable.
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500), resizeable=False, minimizable=False
        )


        button_left = toga.Button(
            "Left",
            on_press=self.turn_left,
            style=Pack(flex=1),
        )

        button_right = toga.Button(
            "Right",
            on_press=self.turn_right,
            style=Pack(flex=1),
        )

        button_forward = toga.Button(
            "Forward",
            on_press=self.move_forward,
            style=Pack(flex=1),
        )

        button_backward = toga.Button(
            "Forward",
            on_press=self.move_backward,
            style=Pack(flex=1),
        )

        view = toga.ImageView(id='images', image = '/Users/bogdanivanyuk/Desktop/picar/assets/car_img.png')


        # Box class
        # Container of components
        #   Add components for the first row of the outer box
        inner_box1 = toga.Box(
            style=Pack(direction=ROW), # common style
            children=[
                button_left,
                button_right,
                button_forward,
                button_backward
            ],
        )

        inner_box2 = toga.Box(
            style=Pack(direction=ROW), # common style
            children=[
                view
            ]
        )

    

        #  Create the outer box with 2 rows
        outer_box = toga.Box(
            style=Pack(direction=COLUMN, height=10), children=[inner_box1, inner_box2]
        )

        self.main_window.content = outer_box  # Add the content on the main window
        self.main_window.show()


    def turn_left(self, button):
        print("Left")
    
    def turn_right(self, button):
        print("Right")

    def move_backward(self, button):
        print("Backward")

    def move_forward(self, button):
        print("Forward")

