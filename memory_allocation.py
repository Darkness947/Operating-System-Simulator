import tkinter as tk
from tkinter import ttk, messagebox

def open_memory_allocation():
    window = tk.Toplevel()
    window.title("Contiguous Memory Allocation")
    window.geometry("700x500")

    # Inputs Frame
    input_frame = ttk.Frame(window, padding=10)
    input_frame.pack(fill='x')

    ttk.Label(input_frame, text="Free Memory Blocks (comma-separated):").grid(row=0, column=0, sticky='w', pady=5)
    entry_blocks = ttk.Entry(input_frame, width=50)
    entry_blocks.insert(0, "100, 500, 200, 300, 600")
    entry_blocks.grid(row=0, column=1, pady=5, padx=5)

    ttk.Label(input_frame, text="Process Memory Requests (comma-separated):").grid(row=1, column=0, sticky='w', pady=5)
    entry_requests = ttk.Entry(input_frame, width=50)
    entry_requests.insert(0, "212, 417, 112, 426")
    entry_requests.grid(row=1, column=1, pady=5, padx=5)

    ttk.Label(input_frame, text="Allocation Technique:").grid(row=2, column=0, sticky='w', pady=5)
    algos = ["First Fit", "Best Fit", "Worst Fit"]
    algo_var = tk.StringVar(value=algos[0])
    algo_dropdown = ttk.Combobox(input_frame, textvariable=algo_var, values=algos, state="readonly", width=15)
    algo_dropdown.grid(row=2, column=1, sticky='w', pady=5, padx=5)

    # Result Table
    res_frame = ttk.Frame(window, padding=10)
    res_frame.pack(fill='both', expand=True)

    columns = ("p_no", "p_size", "b_no", "b_size", "int_frag")
    tree = ttk.Treeview(res_frame, columns=columns, show="headings")
    tree.heading("p_no", text="Process No.")
    tree.heading("p_size", text="Process Size")
    tree.heading("b_no", text="Block No.")
    tree.heading("b_size", text="Original Block Size")
    tree.heading("int_frag", text="Internal Fragmentation")
    
    tree.column("p_no", width=80, anchor='center')
    tree.column("p_size", width=100, anchor='center')
    tree.column("b_no", width=80, anchor='center')
    tree.column("b_size", width=120, anchor='center')
    tree.column("int_frag", width=140, anchor='center')
    
    tree.pack(fill='both', expand=True)

    def simulate():
        try:
            blocks = [int(x.strip()) for x in entry_blocks.get().split(",") if x.strip()]
            processes = [int(x.strip()) for x in entry_requests.get().split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers separated by commas.")
            return

        algo = algo_var.get()
        
        # We need to keep track of blocks.
        # Format block: {'id': i+1, 'size': s, 'original': s}
        mem_blocks = [{'id': i+1, 'size': s, 'original': s} for i, s in enumerate(blocks)]
        
        for item in tree.get_children():
            tree.delete(item)

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
                # Calculate internal fragmentation strictly for THIS process vs current available block size
                int_frag = allocated_block['size'] - p_size
                tree.insert("", "end", values=(
                    f"P{i+1}", 
                    p_size, 
                    allocated_block['id'], 
                    allocated_block['original'], 
                    int_frag
                ))
                # Update block available size
                allocated_block['size'] -= p_size
            else:
                tree.insert("", "end", values=(
                    f"P{i+1}", 
                    p_size, 
                    "Not Allocated", 
                    "-", 
                    "-"
                ), tags=('unallocated',))
                
        tree.tag_configure('unallocated', background='#ffcccc')

    ttk.Button(window, text="Simulate", command=simulate).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_memory_allocation()
    root.mainloop()
