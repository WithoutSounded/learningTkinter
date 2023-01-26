import tkinter as tk
from tkinter import ttk

import tkinter.font as font
from windows import set_dpi_awareness

set_dpi_awareness()


# application interface
class DistanceConverter(tk.Tk):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.title("Distance Converter")
    self.frames = dict()

    container = ttk.Frame(self)
    container.grid(padx=60, pady=30, sticky='EW')

    # MetresToFeet_frame = MetresToFeet(container, self)
    # FeetToMetres_frame = FeetToMetres(container, self)
    # MetresToFeet_frame.grid(column=0, row=0, sticky='NSEW')
    # FeetToMetres_frame.grid(column=0, row=0, sticky='NSEW')
    # self.frames[MetresToFeet] = MetresToFeet_frame
    # self.frames[FeetToMetres] = FeetToMetres_frame

    for FrameClass in (MetresToFeet, FeetToMetres):
      frame = FrameClass(container, self)
      self.frames[FrameClass] = frame
      frame.grid(column=0, row=0, sticky='NSEW')
      # wont work
      # b/c frame itself are NOT SELECTED
      # frame.bind("<Return>", frame.calculate)
      # frame.bind("<KP_Enter>", frame.calculate)

    # handling initial binding problem
    # just select/raise the frame we want
    self.show_frame(MetresToFeet)
      
    # this will only bind to the LAST frame
    # self.bind("<Return>", frame.calculate)
    # self.bind("<KP_Enter>", frame.calculate)

  def show_frame(self, container):
    frame = self.frames[container]
    self.bind("<Return>", frame.calculate)
    self.bind("<KP_Enter>", frame.calculate)
    frame.tkraise()


class MetresToFeet(ttk.Frame):
  def __init__(self, container, controller, **kwargs):
    super().__init__(container, **kwargs)

    # value store and change
    self.metres_value = tk.StringVar()
    self.feet_value = tk.StringVar(value="Feet Shown Here")

    # element(widget)
    metres_lbl = ttk.Label(self, text="Metres:")
    metres_input = ttk.Entry(self,
                             textvariable=self.metres_value,
                             font=("Segoe UI", 15))

    feet_lbl = ttk.Label(self, text="Feet:")
    feet_display = ttk.Label(self, textvariable=self.feet_value)
    calc_btn = ttk.Button(self, text="Calculate!", command=self.calculate)

    switch_btn = ttk.Button(self,
                            text="Switch to Feet Converter",
                            command=lambda: controller.show_frame(FeetToMetres))

    # widget layout
    metres_lbl.grid(column=0, row=0, sticky='w')
    metres_input.grid(column=1, row=0, sticky='ew')
    metres_input.focus()

    feet_lbl.grid(column=0, row=1, sticky='w')
    feet_display.grid(column=1, row=1, sticky='ew')

    calc_btn.grid(column=0, row=2, columnspan=2, sticky='ew')
    switch_btn.grid(column=0, row=3, columnspan=2, sticky='ew')

    # due to ALL element has config in padx and pady
    for child in self.winfo_children():
      child.grid_configure(padx=15, pady=15)

  def calculate(self, *args):
    try:
      metres = float(self.metres_value.get())
      feet = metres * 3.28084
      self.feet_value.set(f"{feet:.3f}")
    except ValueError:
      pass


class FeetToMetres(ttk.Frame):
  def __init__(self, container, controller, **kwargs):
    super().__init__(container, **kwargs)

    # value store and change
    self.feet_value = tk.StringVar()
    self.metres_value = tk.StringVar(value="Metres Shown Here")

    # element(widget)
    feet_lbl = ttk.Label(self, text="Feet:")
    feet_input = ttk.Entry(self,
                           textvariable=self.feet_value,
                           font=("Segoe UI", 15))

    metres_lbl = ttk.Label(self, text="Metres:")
    metres_display = ttk.Label(self, textvariable=self.metres_value)
    calc_btn = ttk.Button(self,
                          text="Calculate!",
                          command=self.calculate)

    switch_btn = ttk.Button(self,
                            text="Switch to Metres Converter",
                            command=lambda: controller.show_frame(MetresToFeet))
    
    # widget layout
    feet_lbl.grid(column=0, row=0, sticky='w')
    feet_input.grid(column=1, row=0, sticky='ew')
    feet_input.focus()

    metres_lbl.grid(column=0, row=1, sticky='w')
    metres_display.grid(column=1, row=1, sticky='ew')

    calc_btn.grid(column=0, row=2, columnspan=2, sticky='ew')
    switch_btn.grid(column=0, row=3, columnspan=2, sticky='ew')

    # due to ALL element has config in padx and pady
    for child in self.winfo_children():
      child.grid_configure(padx=15, pady=15)

  def calculate(self, *args):
    try:
      feet = float(self.feet_value.get())
      metres = feet / 3.28084
      self.metres_value.set(f"{metres:.3f}")
    except ValueError:
      pass


root = DistanceConverter()

# config
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# it has to be in root
font.nametofont("TkDefaultFont").configure(size=15)  # not for input
# so using this method then developer has to change manully

root.mainloop()
