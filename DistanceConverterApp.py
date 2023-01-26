import tkinter as tk
from tkinter import ttk

import tkinter.font as font
from windows import set_dpi_awareness

set_dpi_awareness()


def calculate_feet(*args):
  try:
    metres = float(metres_value.get())
    feet = metres* 3.28084
    feet_value.set(f"{feet:.3f}")
  except ValueError:
    pass

root = tk.Tk()
root.title("Distance Converter")
# config
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# it has to be in root
font.nametofont("TkDefaultFont").configure(size=15) # not for input
# so using this method then developer has to change manully

# value store and change
metres_value = tk.StringVar()
feet_value = tk.StringVar(value="Feet Shown Here")

# main frame
main = ttk.Frame(root, padding=(30,15))
main.grid()

# element
metres_lbl = ttk.Label(main, text="Metres:")
metres_input = ttk.Entry(main, textvariable=metres_value, font=("Segoe UI", 15))
feet_lbl = ttk.Label(main, text="Feet:")
feet_display = ttk.Label(main, textvariable=feet_value)
calc_btn = ttk.Button(main, text="Calculate!", command=calculate_feet)


metres_lbl.grid(column=0, row=0, sticky='w')
metres_input.grid(column=1, row=0, sticky='ew')
metres_input.focus()

feet_lbl.grid(column=0, row=1, sticky='w')
feet_display.grid(column=1, row=1, sticky='ew')

calc_btn.grid(column=0, row=2, columnspan=2, sticky='ew')


# due to ALL element has config in padx and pady
for child in main.winfo_children():
  child.grid_configure(padx=15, pady=15)
  

metres_input.bind("<Return>", calculate_feet)
metres_input.bind("<KP_Enter>", calculate_feet)

root.mainloop()
