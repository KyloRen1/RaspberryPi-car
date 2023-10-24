import tkinter as tk 


def button_event(event):
    print('Turn right', event.keysym)

def left(val):
    print('Turn left', val)

def up(val):
    print('Turn up', val)

def down(val):
    print('Turn down', val)

def main():
    main_window = tk.Tk()
    main_window.title("PiCar")

    main_window.geometry("600x600")

    main_window.bind("<KeyRelease>", button_event)
   # main_window.bind("<Left>", button_event)
   # main_window.bind("<Up>", button_event)
   # main_window.bind("<Down>", button_event)

    main_window.mainloop()


if __name__ == '__main__':
    main()