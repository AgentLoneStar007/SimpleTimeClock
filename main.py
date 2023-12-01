## Simple Time Clock
## By AgentLoneStar007
## https://github.com/AgentLoneStar007


# Imports
import tkinter as tk
import tkinter.font as tkFont
import os
import sys
import platform
import threading

# Var(s)
current_time: int = 0


# Function(s)
## Format input of minutes to DD:HH:MM
def formatMinutesString(minutes: int) -> str:
    # Return an error if the input is somehow negative
    if minutes < 0:
        raise ValueError("Input must be a non-negative integer.")

    days, remainder = divmod(minutes, 1440)  # 1,440 minutes in a day
    hours, minutes = divmod(remainder, 60)  # 60 minutes in an hour

    # Return a formatted string
    return "{:02d}:{:02d}:{:02d}".format(days, hours, minutes)


# Timer background function
class Timer(threading.Thread):
    # Vars
    label: tk.Label
    app_class: 'App'  # Reference to the App class because I have to pass through the current_time var from app class
    # to the timer

    # Init function
    def __init__(self, label: tk.Label = None, app_class: 'App' = None) -> None:
        # Initialize the parent class
        super().__init__()
        # Set is_running to false
        self._is_running: bool = False
        # Set in-class variables to their proper values of the label needing updating to the label from App,
        self.label = label
        # and the app_class var to the App class itself
        self.app_class = app_class

    # Run function, which changes is_running to true, and starts a Tkinter background task
    def run(self) -> None:
        self._is_running = True
        self.root.after(60000, self.updateTime)  # Schedule the update_time function every 60 seconds

    # Stop function, which simply stops the background timer task
    def stop(self):
        self._is_running = False

    # Update time function, which does most the work
    def updateTime(self):
        # If the timer is running,
        if self._is_running:
            # Add 1 to the current time var
            self.app_class.current_time += 1
            # Update the current time readout label
            self.label.config(text=formatMinutesString(self.app_class.current_time))
            self.root.after(60000, self.updateTime)  # Schedule the next update after 60 seconds


class App:
    # Vars
    toggle_button: tk.Button
    total_time_label: tk.Label
    clocked_in: bool = False
    current_time: int

    def __init__(self, root) -> None:
        root.title('Simple Time Clock')
        width: int = 500
        height: int = 220
        screenwidth: int = root.winfo_screenwidth()
        screenheight: int = root.winfo_screenheight()
        align_string: str = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(align_string)
        root.resizable(width=False, height=False)

        total_time_label: tk.Label = tk.Label(root)
        total_time_label["font"] = tkFont.Font(family='Times', size=68)
        total_time_label["fg"] = "#333333"
        total_time_label["justify"] = "center"
        total_time_label["text"] = "00:00:00"
        total_time_label.place(x=75, y=30, width=320, height=150)

        total_time_header_label: tk.Label = tk.Label(root)
        total_time_header_label["font"] = tkFont.Font(family='Times', size=18)
        total_time_header_label["fg"] = "#333333"
        total_time_header_label["justify"] = "center"
        total_time_header_label["text"] = "Total Time, in Minutes:"
        total_time_header_label.place(x=20, y=10, width=240, height=40)

        toggle_button: tk.Button = tk.Button(root)
        toggle_button["bg"] = "#efefef"
        toggle_button["font"] = tkFont.Font(family='Times', size=18)
        toggle_button["fg"] = "#000000"
        toggle_button["justify"] = "center"
        toggle_button["text"] = "Clock In"
        toggle_button.place(x=160, y=160, width=157, height=42)
        toggle_button["command"] = lambda: self.toggleClockState()

        # Set class vars to items needing updates
        self.toggle_button = toggle_button
        self.total_time_label = total_time_label

    def toggleClockState(self) -> int:
        # If already clocked in,
        if self.clocked_in:
            # Update clocked in var
            self.clocked_in = False
            # Update button text
            self.toggle_button.config(text='Clock In')
            # Stop the timer thread
            self.timer.stop()
        else:
            # Update clocked in var
            self.clocked_in = True
            # Update button text
            self.toggle_button.config(text='Clock Out')
            # Create object of Timer class
            self.timer = Timer(self.total_time_label, self)
            self.timer.root = root  # Pass the root window to the Timer class
            self.timer.start()  # Start the timer thread

        return 0


# Function to select the needed icon, depending on whether the user is on Windows or a Unix-based OS
def chooseIcon(providedWindow) -> None:
    bundle_dir: str = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    error_message: str = 'Failed to set window icon.'
    if platform.system() == 'Windows':
        # Putting this in a try/except because it still might not work
        try:
            providedWindow.iconbitmap(os.path.abspath(os.path.join(bundle_dir, 'assets\icon.ico')))
            return
        except:
            return print(error_message)
    else:
        try:
            unixIcon = os.path.abspath(os.path.join(bundle_dir, 'assets/icon.xbm'))
            providedWindow.iconbitmap(f'@{unixIcon}')
            return
        except:
            return print(error_message)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.current_time = current_time
    chooseIcon(root)
    root.mainloop()
