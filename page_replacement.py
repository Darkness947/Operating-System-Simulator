import tkinter as tk
from tkinter import ttk, messagebox

class PageReplacementFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self._build_ui()

    def _build_ui(self):
        # Top Bar
        top_bar = ttk.Frame(self)
        top_bar.pack(fill='x', padx=10, pady=5)
        
        btn_back = ttk.Button(top_bar, text="← Back to Menu", command=lambda: self.controller.show_frame('menu'))
        btn_back.pack(side='left')
        
        lbl_title = ttk.Label(top_bar, text="Page Replacement Algorithms", font=("Segoe UI", 16, "bold"))
        lbl_title.pack(side='left', padx=20)

        input_frame = ttk.Frame(self, padding=10)
        input_frame.pack(fill='x')

        ttk.Label(input_frame, text="Frame Size:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_frames = ttk.Entry(input_frame, width=10)
        self.entry_frames.insert(0, "3")
        self.entry_frames.grid(row=0, column=1, pady=5, padx=5, sticky='w')

        ttk.Label(input_frame, text="Reference String (comma-separated):").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_refs = ttk.Entry(input_frame, width=60)
        self.entry_refs.insert(0, "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2")
        self.entry_refs.grid(row=1, column=1, pady=5, padx=5, sticky='w')

        ttk.Button(input_frame, text="Simulate All", command=self.simulate).grid(row=2, column=0, columnspan=2, pady=10)

        # Notebook for the 3 tables
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        self.fifo_frame = ttk.Frame(self.notebook)
        self.opt_frame = ttk.Frame(self.notebook)
        self.lru_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.fifo_frame, text="FIFO")
        self.notebook.add(self.opt_frame, text="Optimal")
        self.notebook.add(self.lru_frame, text="LRU")

        self.fifo_tree = None
        self.opt_tree = None
        self.lru_tree = None
        
        self.fifo_lbl = ttk.Label(self.fifo_frame, font=("Segoe UI", 12, "bold"))
        self.fifo_lbl.pack(pady=5)
        self.opt_lbl = ttk.Label(self.opt_frame, font=("Segoe UI", 12, "bold"))
        self.opt_lbl.pack(pady=5)
        self.lru_lbl = ttk.Label(self.lru_frame, font=("Segoe UI", 12, "bold"))
        self.lru_lbl.pack(pady=5)

    def _create_tree(self, parent_frame, frames_count):
        columns = ["ref"] + [f"f{i+1}" for i in range(frames_count)] + ["status"]
        tree = ttk.Treeview(parent_frame, columns=columns, show="headings", height=10)
        
        tree.heading("ref", text="Reference")
        tree.column("ref", width=80, anchor='center')
        
        for i in range(frames_count):
            tree.heading(f"f{i+1}", text=f"Frame {i+1}")
            tree.column(f"f{i+1}", width=80, anchor='center')
            
        tree.heading("status", text="Status")
        tree.column("status", width=100, anchor='center')
        
        tree.pack(fill='both', expand=True, side='left')
        
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        tree.tag_configure('hit', background='#ccffcc')
        tree.tag_configure('miss', background='#ffcccc')
        
        return tree

    def simulate(self):
        try:
            frames_count = int(self.entry_frames.get().strip())
            if frames_count <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer for frame size.")
            return

        try:
            refs = [int(x.strip()) for x in self.entry_refs.get().split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers separated by commas for reference string.")
            return

        if not refs:
            messagebox.showerror("Error", "Reference string cannot be empty.")
            return

        # Destroy old trees
        for widget in self.fifo_frame.winfo_children():
            if isinstance(widget, ttk.Treeview) or isinstance(widget, ttk.Scrollbar): widget.destroy()
        for widget in self.opt_frame.winfo_children():
            if isinstance(widget, ttk.Treeview) or isinstance(widget, ttk.Scrollbar): widget.destroy()
        for widget in self.lru_frame.winfo_children():
            if isinstance(widget, ttk.Treeview) or isinstance(widget, ttk.Scrollbar): widget.destroy()

        self.fifo_tree = self._create_tree(self.fifo_frame, frames_count)
        self.opt_tree = self._create_tree(self.opt_frame, frames_count)
        self.lru_tree = self._create_tree(self.lru_frame, frames_count)

        n = len(refs)

        def get_row_values(ref, current_frames, status):
            # Pad with hyphens if frames are empty
            padded_frames = list(current_frames) + ["-"] * (frames_count - len(current_frames))
            return [ref] + padded_frames + [status]

        # 1. FIFO
        fifo_frames = []
        fifo_faults = 0
        fifo_hits = 0
        
        for r in refs:
            status = ""
            if r in fifo_frames:
                fifo_hits += 1
                status = "Hit"
            else:
                fifo_faults += 1
                status = "Miss"
                if len(fifo_frames) < frames_count:
                    fifo_frames.append(r)
                else:
                    fifo_frames.pop(0)
                    fifo_frames.append(r)
            
            tag = 'hit' if status == "Hit" else 'miss'
            self.fifo_tree.insert("", "end", values=get_row_values(r, fifo_frames, status), tags=(tag,))
            
        self.fifo_lbl.config(text=f"FIFO - Faults: {fifo_faults} | Hits: {fifo_hits} | Hit Ratio: {(fifo_hits/n)*100:.2f}%")

        # 2. Optimal
        opt_frames = []
        opt_faults = 0
        opt_hits = 0
        
        for i, r in enumerate(refs):
            status = ""
            if r in opt_frames:
                opt_hits += 1
                status = "Hit"
            else:
                opt_faults += 1
                status = "Miss"
                if len(opt_frames) < frames_count:
                    opt_frames.append(r)
                else:
                    farthest_idx = -1
                    farthest_page_idx = -1
                    for j, f in enumerate(opt_frames):
                        try:
                            next_use = refs[i+1:].index(f)
                        except ValueError:
                            next_use = float('inf')
                            
                        if next_use > farthest_idx:
                            farthest_idx = next_use
                            farthest_page_idx = j
                            
                    opt_frames.pop(farthest_page_idx)
                    opt_frames.append(r)
                    
            tag = 'hit' if status == "Hit" else 'miss'
            self.opt_tree.insert("", "end", values=get_row_values(r, opt_frames, status), tags=(tag,))

        self.opt_lbl.config(text=f"Optimal - Faults: {opt_faults} | Hits: {opt_hits} | Hit Ratio: {(opt_hits/n)*100:.2f}%")

        # 3. LRU
        lru_frames = []
        lru_faults = 0
        lru_hits = 0
        
        for r in refs:
            status = ""
            if r in lru_frames:
                lru_hits += 1
                status = "Hit"
                lru_frames.remove(r)
                lru_frames.append(r)
            else:
                lru_faults += 1
                status = "Miss"
                if len(lru_frames) < frames_count:
                    lru_frames.append(r)
                else:
                    lru_frames.pop(0)
                    lru_frames.append(r)
                    
            tag = 'hit' if status == "Hit" else 'miss'
            self.lru_tree.insert("", "end", values=get_row_values(r, lru_frames, status), tags=(tag,))

        self.lru_lbl.config(text=f"LRU - Faults: {lru_faults} | Hits: {lru_hits} | Hit Ratio: {(lru_hits/n)*100:.2f}%")
