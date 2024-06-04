import os
import sys
import datetime
import winsound
import tkcalendar
from tktimepicker import SpinTimePickerOld, constants

# tkinter
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from tkinter import filedialog, messagebox


class ClockityClock:
    def __init__(self) -> None:
        # Create GUI
        self.root = tk.Tk()

        # set the style
        self._set_azure_style()

        # screen settings
        self.width = 400
        self.height = 500
        self._set_screen_settings()

        # populate the GUI
        self._create_main_frame()

        self.root.mainloop()
    
    def _set_azure_style(self):
        """ Set the Azure Style """
        self.style = ttk.Style(self.root)
        style_path = 'res/style/azure.tcl' # if locally called, use local path.
        if not os.path.isfile(style_path):
            # if not locally called, use the absolute path.
            style_path = os.path.join(os.path.dirname(sys.argv[0]), style_path)
        self.root.tk.call('source', style_path)
        self.style.theme_use('azure')

    def _set_screen_settings(self):
        """ Set the screen settings and the window placement. """
        # setting title
        self.root.title("Clockity-Clock")

        # set the icon
        # self.png_icon_path = 'res/wallet.png'
        # self.ico_icon_path = 'res/wallet.ico'
        # if not os.path.isfile(self.png_icon_path): # if not locally called, use the absolute path.
        #     self.png_icon_path = os.path.join(os.path.dirname(sys.argv[0]), self.png_icon_path)
        #     self.ico_icon_path = os.path.join(os.path.dirname(sys.argv[0]), self.ico_icon_path)
        # self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=self.png_icon_path))

        # setting window size
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height,
                                    (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

    def _create_main_frame(self):
        """ Create the main frame """
        self.margin = 20 # margin to be used across the gui

        # Title label
        highlightFont = font.Font(family='Helvetica', name='appHighlightFont', size=12, weight='bold')
        title_label = ttk.Label(self.root, text="Clockity Clock", font=highlightFont)
        title_height = 32
        title_label.pack(side=tk.TOP, anchor='n', pady=self.margin)

        # Version label
        version_label = ttk.Label(self.root, text="0.1")
        version_label.pack(side=tk.BOTTOM, anchor='se', padx=5, pady=5)

        ## Select date section
        self.date_frame = ttk.Frame(self.root)
        self.date_frame.pack(padx=5, pady=5)
        ttk.Label(self.date_frame, text="Alarm date:").pack(padx=5, pady=5)

        self.cal = tkcalendar.Calendar(self.date_frame, selectmode='day', date_pattern='dd-mm-yyyy')
        self.cal.pack()


        ## Select time section
        self.time_frame = ttk.Frame(self.root)
        self.time_frame.pack(padx=5, pady=5)
        # Label
        #ttk.Label(self.time_frame, text="Time:").pack(padx=5, pady=5)


        # Selection button
        #ttk.Button(self.time_frame, text="Select Time", command=self.open_time_picker_callback).pack(padx=5, pady=5)
        self.selected_hour = tk.StringVar()
        hour_label = ttk.Label(self.time_frame, text="HH:")
        hour_label.grid(row=1, column=1, padx=5, pady=5)
        spin_hour = tk.Spinbox(self.time_frame, from_=0, to=23, width=2, textvariable=self.selected_hour)
        spin_hour.grid(row=1, column=2, padx=5, pady=5)

        self.selected_minutes = tk.StringVar()
        minute_label = ttk.Label(self.time_frame, text="MM:")
        minute_label.grid(row=1, column=3, padx=5, pady=5)
        spin_minute = tk.Spinbox(self.time_frame, from_=0, to=59, width=2, textvariable=self.selected_minutes)
        spin_minute.grid(row=1, column=4, padx=5, pady=5)

        self.selected_seconds = tk.StringVar()
        seconds_label = ttk.Label(self.time_frame, text="SS:")
        seconds_label.grid(row=1, column=5, padx=5, pady=5)
        spin_second = tk.Spinbox(self.time_frame, from_=0, to=59, width=2, textvariable=self.selected_seconds)
        spin_second.grid(row=1, column=6, padx=5, pady=5)

        # Select date button
        self.selection_frame = ttk.Frame(self.root)
        self.selection_frame.pack()

        button_select_date = ttk.Button(self.selection_frame, text="Select Date & Time", command=self.select_date_and_time_callback)
        button_select_date.pack(side=tk.RIGHT)

        # Entry
        self.selected_date_and_time = tk.StringVar()
        ttk.Entry(self.selection_frame, textvariable=self.selected_date_and_time).pack(padx=5, pady=5, side=tk.LEFT)

        ## Start alarm section
        ttk.Button(self.root, text="Set Alarm", command=self.set_alarm_callback).pack(padx=5, pady=5)

    # Callback functions
    def select_date_and_time_callback(self):
        self.date_and_time = "{} {}:{}:{}".format(self.cal.get_date(), self.selected_hour.get().zfill(2), self.selected_minutes.get().zfill(2), self.selected_seconds.get().zfill(2))
        self.selected_date_and_time.set(self.date_and_time)

    def updateTime(self, time):
        self.label_time.configure(text="{}:{}:{}".format(*time)) # if you are using 24 hours, remove the 3rd flower bracket its for period

    def set_alarm_callback(self):
        alarm_datetime = datetime.datetime.strptime(self.date_and_time, "%d-%m-%Y %H:%M:%S")
        #alarm_datetime = alarm_datetime.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        now = datetime.datetime.now()
        delta_t = alarm_datetime - now
        if delta_t.total_seconds() < 0:
            alarm_datetime += datetime.timedelta(days=1)
            delta_t = alarm_datetime - now
        print(f"Alarm set for {alarm_datetime}")
        self.root.after(int(delta_t.total_seconds() * 1000), self.play_alarm_callback)

    def play_alarm_callback(self):
        winsound.Beep(1000, 1000)  # Beep for 1 second
        messagebox.showinfo("Alarm", "ALARM!")



if __name__ == "__main__":
    app = ClockityClock()