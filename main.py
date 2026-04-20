import tkinter as tk
from tkinter import ttk
import sys

# Import the modules for each section
# Currently they will be missing until we create them, so we wrap in try-except or import safely
try:
    from cpu_scheduling import open_cpu_scheduling
    from memory_allocation import open_memory_allocation
    from page_replacement import open_page_replacement
except ImportError:
    # Dummy functions for now until modules are created
    def open_cpu_scheduling(): print("CPU Scheduling module not loaded.")
    def open_memory_allocation(): print("Memory Allocation module not loaded.")
    def open_page_replacement(): print("Page Replacement module not loaded.")


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Operating System Simulator")
        self.geometry("400x350")
       # self.resizable(False, False)

        # Style configuration
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 12), padding=10)
        style.configure('TLabel', font=('Segoe UI', 16, 'bold'))

        self._setup_ui()

    def _setup_ui(self):
        # Header Label
        lbl_header = ttk.Label(self, text="OS Simulator Menu")
        lbl_header.pack(pady=30)

        # Buttons Frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='both', expand=True, padx=40)

        # CPU Scheduling Button
        btn_cpu = ttk.Button(btn_frame, text="CPU scheduling algorithms", command=self._on_cpu_scheduling)
        btn_cpu.pack(fill='x', pady=5)

        # Contiguous Memory Allocation Button
        btn_memory = ttk.Button(btn_frame, text="Contiguous Memory Allocation", command=self._on_memory_allocation)
        btn_memory.pack(fill='x', pady=5)

        # Page Replacement Button
        btn_page = ttk.Button(btn_frame, text="Page replacement algorithms", command=self._on_page_replacement)
        btn_page.pack(fill='x', pady=5)

        # Exit Button
        btn_exit = ttk.Button(btn_frame, text="Exit", command=self.destroy)
        btn_exit.pack(fill='x', pady=5)

    def _on_cpu_scheduling(self):
        open_cpu_scheduling()

    def _on_memory_allocation(self):
        open_memory_allocation()

    def _on_page_replacement(self):
        open_page_replacement()


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
