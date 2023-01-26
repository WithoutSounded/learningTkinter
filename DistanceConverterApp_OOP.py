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

    # wont be available anywhere else, so using self.frame
    frame = MetresToFeet(self, padding=(60, 30))
    frame.grid()

    self.bind("<Return>", frame.calculate_feet)
    self.bind("<KP_Enter>", frame.calculate_feet)


class MetresToFeet(ttk.Frame):
  def __init__(self, container, **kwargs):
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
    calc_btn = ttk.Button(self, text="Calculate!", command=self.calculate_feet)

    # widget layout
    metres_lbl.grid(column=0, row=0, sticky='w')
    metres_input.grid(column=1, row=0, sticky='ew')
    metres_input.focus()
    
    feet_lbl.grid(column=0, row=1, sticky='w')
    feet_display.grid(column=1, row=1, sticky='ew')
    
    calc_btn.grid(column=0, row=2, columnspan=2, sticky='ew')

    # due to ALL element has config in padx and pady
    for child in self.winfo_children():
      child.grid_configure(padx=15, pady=15)
  
  def calculate_feet(self, *args):
    try:
      metres = float(self.metres_value.get())
      feet = metres * 3.28084
      self.feet_value.set(f"{feet:.3f}")
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
