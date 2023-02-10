import tkinter as tk
from tkinter import ttk
from collections import deque


class Timer(ttk.Frame):
  def __init__(self, parent, controller, show_settings):
    super().__init__(parent)

    self["style"] = "Background.TFrame"
    
    self.controller = controller
    self.columnconfigure(0, weight=1) # take all the space
    self.rowconfigure(1, weight=1) # not nesassary, just to push row 0
    
    pomodoro_time = int(controller.pomodoro.get())
    
    # Timer layout
    self.current_timer_label = tk.StringVar(value = controller.timer_schedule[0])
    self.current_time = tk.StringVar(value=f"{pomodoro_time:02d}:00")
    self.timer_running=False
    self._timer_decrement_job = None # underscore means that it's private variable, used only in this class
    # this variable are used for tracking after() chain

    # row 0 Timer Descroption and Settings button
    timer_description = ttk.Label(
      self,
      textvariable=self.current_timer_label,
      style="LightText.TLabel",
    )
    
    settings_button = ttk.Button(
        self,
        text="Settings",
        command=show_settings,
        style = "PomodoroButton.TButton",
        cursor="hand2"
    )
    
    timer_description.grid(row=0, column=0, sticky="W", padx=(10,0), pady=(10,0))
    settings_button.grid(row=0, column=1, sticky="E", padx=10, pady=(10, 0))

    # row 1 TIMER
    timer_frame = ttk.Frame(self, height="100", style="Timer.TFrame")
    timer_frame.grid(columnspan=2, pady=(10,0), sticky="NSEW")

    timer_counter = ttk.Label(
      timer_frame,
      textvariable=self.current_time,
      style="TimerText.TLabel"
    )
    # timer_counter.grid()
    timer_counter.place(relx=.5, rely=.5, anchor="center")
    # if there is no setting for anchor, the center point will be the top left of the label

    # row 2 start btn, stop btn and reset btn
    button_container = ttk.Frame(self, padding=10, style="Background.TFrame")
    button_container.grid(row=2, column=0, columnspan=2, sticky="EW")
    button_container.columnconfigure((0,1,2), weight=1) # let column 0, 1, 2 has same weight

    self.start_button = ttk.Button(
      button_container,
      text="Start",
      command=self.start_timer,
      style = "PomodoroButton.TButton",
      cursor="hand2",
    )
    
    self.stop_button = ttk.Button(
      button_container,
      text="Stop",
      state="disabled",
      command=self.stop_timer,
      style="PomodoroButton.TButton",
      cursor="hand2",
    )

    self.reset_button = ttk.Button(
      button_container,
      text="Reset",
      command=self.reset_timer,
      style="PomodoroButton.TButton",
      cursor="hand2",
    )

    
    self.start_button.grid(row=0, column=0, sticky="EW")
    self.stop_button.grid(row=0, column=1, sticky="EW", padx=5)
    self.reset_button.grid(row=0, column=2, sticky="EW")
    

  def start_timer(self):
    self.timer_running=True
    self.stop_button['state'] = "enabled"
    self.start_button['state'] = "disabled"
    self.decrement_time()


  def stop_timer(self):
    self.timer_running=False
    self.stop_button['state'] = "disabled"
    self.start_button['state'] = "enabled"

    if self._timer_decrement_job:
      self.after_cancel(self._timer_decrement_job)
      self._timer_decrement_job = None

  def reset_timer(self):
    self.stop_timer()
    pomodoro_time = int(self.controller.pomodoro.get())
    self.current_time.set(f"{pomodoro_time:02d}:00")
    self.timer_schedule = deque(self.controller.timer_order)
    self.current_timer_label.set(self.controller.timer_schedule[0])

  
  def decrement_time(self):
    current_time = self.current_time.get()

    if self.timer_running and current_time != "00:00":
      minutes, seconds = current_time.split(":")

      if int(seconds) > 0:
        seconds = int(seconds)-1
        minutes = int(minutes) # just for same datatype
      else:
        seconds = 59
        minutes = int(minutes)-1

      self.current_time.set(f"{minutes:02d}:{seconds:02d}")
      self._timer_decrement_job = self.after(1000, self.decrement_time) # 1000ms
      
    elif self.timer_running and current_time == "00:00":
      self.controller.timer_schedule.rotate(-1) # take first element to last
      next_up = self.controller.timer_schedule[0]
      self.current_timer_label.set(next_up)
      
      if next_up == "Pomodoro":
          pomodoro_time = int(self.controller.pomodoro.get())
          self.current_time.set(f"{pomodoro_time:02d}:00")
      elif next_up == "Short Break":
          short_break_time = int(self.controller.short_break.get())
          self.current_time.set(f"{short_break_time:02d}:00")
      elif next_up == "Long Break":
          long_break_time = int(self.controller.long_break.get())
          self.current_time.set(f"{long_break_time:02d}:00")

      self._timer_decrement_job = self.after(1000, self.decrement_time) # 1000ms
