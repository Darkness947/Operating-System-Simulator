import tkinter as tk
from tkinter import ttk, messagebox

class MemoryAllocationFrame(ttk.Frame):
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
        
        lbl_title = ttk.Label(top_bar, text="Contiguous Memory Allocation", font=("Segoe UI", 16, "bold"))
        lbl_title.pack(side='left', padx=20)

        # Inputs Frame
        input_frame = ttk.Frame(self, padding=10)
        input_frame.pack(fill='x')

        ttk.Label(input_frame, text="Free Memory Blocks (comma-separated):").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_blocks = ttk.Entry(input_frame, width=50)
        self.entry_blocks.insert(0, "100, 500, 200, 300, 600")
        self.entry_blocks.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(input_frame, text="Process Memory Requests (comma-separated):").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_requests = ttk.Entry(input_frame, width=50)
        self.entry_requests.insert(0, "212, 417, 112, 426")
        self.entry_requests.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(input_frame, text="Allocation Technique:").grid(row=2, column=0, sticky='w', pady=5)
        algos = ["First Fit", "Best Fit", "Worst Fit"]
        self.algo_var = tk.StringVar(value=algos[0])
        algo_dropdown = ttk.Combobox(input_frame, textvariable=self.algo_var, values=algos, state="readonly", width=15)
        algo_dropdown.grid(row=2, column=1, sticky='w', pady=5, padx=5)

        ttk.Button(self, text="Simulate", command=self.simulate).pack(pady=10)

        # Result Table
        res_frame = ttk.Frame(self, padding=10)
        res_frame.pack(fill='both', expand=True)

        columns = ("p_no", "p_size", "b_no", "b_size", "int_frag")
        self.tree = ttk.Treeview(res_frame, columns=columns, show="headings")
        self.tree.heading("p_no", text="Process No.")
        self.tree.heading("p_size", text="Process Size")
        self.tree.heading("b_no", text="Block No.")
        self.tree.heading("b_size", text="Original Block Size")
        self.tree.heading("int_frag", text="Internal Fragmentation")
        
        self.tree.column("p_no", width=80, anchor='center')
        self.tree.column("p_size", width=100, anchor='center')
        self.tree.column("b_no", width=80, anchor='center')
        self.tree.column("b_size", width=120, anchor='center')
        self.tree.column("int_frag", width=140, anchor='center')
        
        self.tree.pack(fill='both', expand=True)
        self.tree.tag_configure('unallocated', background='#ffcccc')

    def simulate(self):
        try:
            blocks = [int(x.strip()) for x in self.entry_blocks.get().split(",") if x.strip()]
            processes = [int(x.strip()) for x in self.entry_requests.get().split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers separated by commas.")
            return

        algo = self.algo_var.get()
        mem_blocks = [{'id': i+1, 'size': s, 'original': s} for i, s in enumerate(blocks)]
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, p_size in enumerate(processes):
            allocated_block = None
            
            if algo == "First Fit":
                for blk in mem_blocks:
                    if blk['size'] >= p_size:
                        allocated_block = blk
                        break
                        
            elif algo == "Best Fit":
                best_idx = -1
                min_diff = float('inf')
                for j, blk in enumerate(mem_blocks):
                    if blk['size'] >= p_size:
                        if blk['size'] - p_size < min_diff:
                            min_diff = blk['size'] - p_size
                            best_idx = j
                if best_idx != -1:
                    allocated_block = mem_blocks[best_idx]
                    
            elif algo == "Worst Fit":
                worst_idx = -1
                max_diff = -1
                for j, blk in enumerate(mem_blocks):
                    if blk['size'] >= p_size:
                        if blk['size'] - p_size > max_diff:
                            max_diff = blk['size'] - p_size
                            worst_idx = j
                if worst_idx != -1:
                    allocated_block = mem_blocks[worst_idx]

            if allocated_block:
                int_frag = allocated_block['size'] - p_size
                self.tree.insert("", "end", values=(f"P{i+1}", p_size, allocated_block['id'], allocated_block['original'], int_frag))
                allocated_block['size'] -= p_size
            else:
                self.tree.insert("", "end", values=(f"P{i+1}", p_size, "Not Allocated", "-", "-"), tags=('unallocated',))
