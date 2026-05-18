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

        ttk.Label(input_frame, text="Free Memory Blocks (KB, comma-separated):").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_blocks = ttk.Entry(input_frame, width=50)
        self.entry_blocks.insert(0, "100, 500, 200, 300, 600")
        self.entry_blocks.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(input_frame, text="Process Memory Requests (KB, comma-separated):").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_requests = ttk.Entry(input_frame, width=50)
        self.entry_requests.insert(0, "212, 417, 112, 426")
        self.entry_requests.grid(row=1, column=1, pady=5, padx=5)

        ttk.Button(self, text="Run All Algorithms", command=self.simulate).pack(pady=10)

        # Notebook for tabs (one per algorithm)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

    def parse_memory_input(self, text):
        items = text.split(",")
        result = []
        for item in items:
            item = item.strip().upper()
            if not item:
                continue
            if item.endswith("KB"):
                val = float(item[:-2].strip())
            elif item.endswith("B"):
                val = float(item[:-1].strip()) / 1024.0
            else:
                val = float(item)
            result.append(val)
        return result

    def _create_algo_tab(self, algo_name, blocks, processes):
        """Create a tab for one allocation algorithm and run its simulation."""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=algo_name)

        # Result Table
        res_frame = ttk.Frame(tab_frame, padding=10)
        res_frame.pack(fill='both', expand=True)

        columns = ("p_no", "p_size", "b_no", "b_size", "int_frag")
        tree = ttk.Treeview(res_frame, columns=columns, show="headings")
        tree.heading("p_no", text="Process No.")
        tree.heading("p_size", text="Process Size (KB)")
        tree.heading("b_no", text="Block No.")
        tree.heading("b_size", text="Original Block Size (KB)")
        tree.heading("int_frag", text="Internal Fragmentation (KB)")
        
        tree.column("p_no", width=80, anchor='center')
        tree.column("p_size", width=120, anchor='center')
        tree.column("b_no", width=80, anchor='center')
        tree.column("b_size", width=150, anchor='center')
        tree.column("int_frag", width=170, anchor='center')

        scrollbar = ttk.Scrollbar(res_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        tree.tag_configure('unallocated', background='#ffcccc')

        # Run the algorithm
        mem_blocks = [{'id': i+1, 'size': s, 'original': s} for i, s in enumerate(blocks)]

        total_allocated = 0
        total_fragmentation = 0

        for i, p_size in enumerate(processes):
            allocated_block = None
            
            if algo_name == "First Fit":
                for blk in mem_blocks:
                    if blk['size'] >= p_size:
                        allocated_block = blk
                        break
                        
            elif algo_name == "Best Fit":
                best_idx = -1
                min_diff = float('inf')
                for j, blk in enumerate(mem_blocks):
                    if blk['size'] >= p_size:
                        if blk['size'] - p_size < min_diff:
                            min_diff = blk['size'] - p_size
                            best_idx = j
                if best_idx != -1:
                    allocated_block = mem_blocks[best_idx]
                    
            elif algo_name == "Worst Fit":
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
                tree.insert("", "end", values=(f"P{i+1}", f"{p_size}", allocated_block['id'], f"{allocated_block['original']}", f"{int_frag}"))
                allocated_block['size'] = 0
                total_allocated += 1
                total_fragmentation += int_frag
            else:
                tree.insert("", "end", values=(f"P{i+1}", f"{p_size}", "Not Allocated", "-", "-"), tags=('unallocated',))

        # Summary label
        summary = f"Allocated: {total_allocated}/{len(processes)} processes | Total Internal Fragmentation: {total_fragmentation:.1f} KB"
        summary_lbl = ttk.Label(tab_frame, text=summary, font=("Segoe UI", 11, "bold"))
        summary_lbl.pack(pady=5)

    def simulate(self):
        try:
            blocks = self.parse_memory_input(self.entry_blocks.get())
            processes = self.parse_memory_input(self.entry_requests.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers (e.g., 100, 2048B, 50KB) separated by commas.")
            return

        if any(v < 0 for v in blocks):
            messagebox.showerror("Error", "Memory block sizes cannot be negative.")
            return
        if any(v < 0 for v in processes):
            messagebox.showerror("Error", "Process memory requests cannot be negative.")
            return
        if not blocks or not processes:
            messagebox.showerror("Error", "Please provide at least one memory block and one process request.")
            return

        # Clear old tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        # Run all three algorithms
        for algo_name in ["First Fit", "Best Fit", "Worst Fit"]:
            self._create_algo_tab(algo_name, blocks, processes)
