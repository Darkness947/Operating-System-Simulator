import tkinter as tk
from tkinter import ttk
import sys

# Import the modules
from cpu_scheduling import CPUSchedulingFrame
from memory_allocation import MemoryAllocationFrame
from page_replacement import PageReplacementFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Operating System Simulator")
        self.geometry("1000x750")
        
        self.dark_mode = False
        
        # Container for stacking frames
        self.container = ttk.Frame(self)
        self.container.pack(fill='both', expand=True)
        
        # Grid layout for container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        self._init_theme()
        self._build_main_menu()
        
    def _init_theme(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            bg_color = '#2d2d2d'
            fg_color = '#ffffff'
            btn_bg = '#444444'
            tree_bg = '#333333'
            entry_bg = '#555555'
        else:
            bg_color = '#f0f0f0'
            fg_color = '#000000'
            btn_bg = '#e0e0e0'
            tree_bg = '#ffffff'
            entry_bg = '#ffffff'

        self.configure(bg=bg_color)
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, foreground=fg_color)
        self.style.configure('Header.TLabel', font=('Segoe UI', 20, 'bold'))
        self.style.configure('TButton', background=btn_bg, foreground=fg_color, font=('Segoe UI', 10), padding=5)
        self.style.map('TButton', background=[('active', '#555555' if self.dark_mode else '#d0d0d0')])
        
        self.style.configure('TCheckbutton', background=bg_color, foreground=fg_color)
        self.style.configure('TSpinbox', fieldbackground=entry_bg, foreground=fg_color, background=bg_color)
        self.style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color)
        self.style.configure('TCombobox', fieldbackground=entry_bg, foreground=fg_color, background=bg_color)
        
        self.style.configure('Treeview', background=tree_bg, foreground=fg_color, fieldbackground=tree_bg)
        self.style.configure('Treeview.Heading', background=btn_bg, foreground=fg_color)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        # Redraw matplotlib charts if any
        if 'cpu' in self.frames and hasattr(self.frames['cpu'], 'reapply_theme'):
            self.frames['cpu'].reapply_theme(self.dark_mode)

    def _build_main_menu(self):
        menu_frame = ttk.Frame(self.container)
        menu_frame.grid(row=0, column=0, sticky="nsew")
        self.frames['menu'] = menu_frame
        
        lbl_header = ttk.Label(menu_frame, text="OS Simulator Menu", style='Header.TLabel')
        lbl_header.pack(pady=40)
        
        # Dark mode toggle
        btn_toggle = ttk.Button(menu_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        btn_toggle.pack(pady=10)

        btn_frame = ttk.Frame(menu_frame)
        btn_frame.pack(fill='both', expand=True, padx=150)

        btn_cpu = ttk.Button(btn_frame, text="CPU scheduling algorithms", command=lambda: self.show_frame('cpu'))
        btn_cpu.pack(fill='x', pady=10)

        btn_memory = ttk.Button(btn_frame, text="Contiguous Memory Allocation", command=lambda: self.show_frame('memory'))
        btn_memory.pack(fill='x', pady=10)

        btn_page = ttk.Button(btn_frame, text="Page replacement algorithms", command=lambda: self.show_frame('page'))
        btn_page.pack(fill='x', pady=10)

        btn_exit = ttk.Button(btn_frame, text="Exit", command=self.destroy)
        btn_exit.pack(fill='x', pady=10)

    def show_frame(self, frame_name):
        if frame_name not in self.frames:
            if frame_name == 'cpu':
                self.frames['cpu'] = CPUSchedulingFrame(self.container, self)
                self.frames['cpu'].grid(row=0, column=0, sticky="nsew")
            elif frame_name == 'memory':
                self.frames['memory'] = MemoryAllocationFrame(self.container, self)
                self.frames['memory'].grid(row=0, column=0, sticky="nsew")
            elif frame_name == 'page':
                self.frames['page'] = PageReplacementFrame(self.container, self)
                self.frames['page'].grid(row=0, column=0, sticky="nsew")
                
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
