import tkinter as tk
from tkinter import ttk
from collections import deque
from frames import Timer, Settings, set_dpi_awareness

set_dpi_awareness()


COLOUR_PRIMARY = "#2e3f4f"
COLOUR_SECONDARY = "#293846"
COLOUR_LIGHT_BACKGROUND = "#fff"
COLOUR_LIGHT_TEXT = "#eee"
COLOUR_DARK_TEXT = "#8095a8"


class PomodoroTimer(tk.Tk):
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      style = ttk.Style(self)
      style.theme_use("clam")

      # create new style named Timer.TFrame, inherit TFrame but change bg color
      style.configure("Timer.TFrame", background=COLOUR_LIGHT_BACKGROUND)
      style.configure("Background.TFrame", background=COLOUR_PRIMARY)
      style.configure(
          "TimerText.TLabel",
          background=COLOUR_LIGHT_BACKGROUND,
          foreground=COLOUR_DARK_TEXT,
          font="Courier 38"
      )

      style.configure(
          "LightText.TLabel",
          background=COLOUR_PRIMARY,
          foreground=COLOUR_LIGHT_TEXT,
      )

      style.configure(
          "PomodoroButton.TButton",
          background=COLOUR_SECONDARY,
          foreground=COLOUR_LIGHT_TEXT,
      )

      style.map(
          "PomodoroButton.TButton",
          background=[("active", COLOUR_PRIMARY), ("disabled", COLOUR_LIGHT_TEXT)]
      )
      
      # Main app window is a tk widget, so background is set directly
      self["background"] = COLOUR_PRIMARY
    
      self.title("Pomodoro Timer")
      self.columnconfigure(0, weight=1) # take all the space
      self.rowconfigure(1, weight=1) # not nesassary, just to push row 0

      # Timer Setting which wanted to shared across others classes
      self.timer_order = ["Pomodoro", "Short Break", "Pomodoro", "Short Break", "Pomodoro", "Long Break"]
      self.timer_schedule = deque(self.timer_order)
      self.pomodoro = tk.StringVar(value=25)
      self.short_break = tk.StringVar(value=5)
      self.long_break = tk.StringVar(value=15)
    
      container = ttk.Frame(self)
      container.grid()
      container.columnconfigure(0, weight=1)

      # switch frame
      settings_frame = Settings(container, self, lambda: self.show_frame(Timer))
      timer_frame = Timer(container, self, lambda: self.show_frame(Settings))
    
      self.frames = {}
      self.frames[Timer] = timer_frame
      self.frames[Settings] = settings_frame
    
      settings_frame.grid(row=0, column=0, sticky="nesw")
      timer_frame.grid(row=0, column=0, sticky="nesw")
  

  def show_frame(self, container):
    frame = self.frames[container]
    frame.tkraise()


app = PomodoroTimer()
app.mainloop()