import tkinter as tk
from tkinter import ttk, messagebox

def open_page_replacement():
    window = tk.Toplevel()
    window.title("Page Replacement Algorithms")
    window.geometry("800x400")

    input_frame = ttk.Frame(window, padding=10)
    input_frame.pack(fill='x')

    ttk.Label(input_frame, text="Frame Size:").grid(row=0, column=0, sticky='w', pady=5)
    entry_frames = ttk.Entry(input_frame, width=10)
    entry_frames.insert(0, "3")
    entry_frames.grid(row=0, column=1, pady=5, padx=5, sticky='w')

    ttk.Label(input_frame, text="Reference String (comma-separated):").grid(row=1, column=0, sticky='w', pady=5)
    entry_refs = ttk.Entry(input_frame, width=60)
    entry_refs.insert(0, "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2")
    entry_refs.grid(row=1, column=1, pady=5, padx=5, sticky='w')

    # Result Table
    res_frame = ttk.Frame(window, padding=10)
    res_frame.pack(fill='both', expand=True)

    columns = ("algo", "faults", "hits", "hit_ratio", "miss_ratio")
    tree = ttk.Treeview(res_frame, columns=columns, show="headings", height=4)
    tree.heading("algo", text="Algorithm")
    tree.heading("faults", text="Page Faults")
    tree.heading("hits", text="Page Hits")
    tree.heading("hit_ratio", text="Hit Ratio (%)")
    tree.heading("miss_ratio", text="Miss Ratio (%)")
    
    tree.column("algo", width=120, anchor='center')
    tree.column("faults", width=100, anchor='center')
    tree.column("hits", width=100, anchor='center')
    tree.column("hit_ratio", width=120, anchor='center')
    tree.column("miss_ratio", width=120, anchor='center')
    
    tree.pack(fill='x')

    def simulate():
        try:
            frames_count = int(entry_frames.get().strip())
            if frames_count <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer for frame size.")
            return

        try:
            refs = [int(x.strip()) for x in entry_refs.get().split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers separated by commas for reference string.")
            return

        if not refs:
            messagebox.showerror("Error", "Reference string cannot be empty.")
            return

        # Clear tree
        for item in tree.get_children():
            tree.delete(item)

        n = len(refs)

        # 1. FIFO
        fifo_frames = []
        fifo_faults = 0
        fifo_hits = 0
        
        for r in refs:
            if r in fifo_frames:
                fifo_hits += 1
            else:
                fifo_faults += 1
                if len(fifo_frames) < frames_count:
                    fifo_frames.append(r)
                else:
                    fifo_frames.pop(0)
                    fifo_frames.append(r)

        # 2. Optimal
        opt_frames = []
        opt_faults = 0
        opt_hits = 0
        
        for i, r in enumerate(refs):
            if r in opt_frames:
                opt_hits += 1
            else:
                opt_faults += 1
                if len(opt_frames) < frames_count:
                    opt_frames.append(r)
                else:
                    # Find furthest used
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

        # 3. LRU
        lru_frames = []
        lru_faults = 0
        lru_hits = 0
        
        for r in refs:
            if r in lru_frames:
                lru_hits += 1
                # Move to end to mark as recently used
                lru_frames.remove(r)
                lru_frames.append(r)
            else:
                lru_faults += 1
                if len(lru_frames) < frames_count:
                    lru_frames.append(r)
                else:
                    # Least recently used is at index 0
                    lru_frames.pop(0)
                    lru_frames.append(r)

        def insert_results(algo, hits, faults):
            hr = (hits / n) * 100
            mr = (faults / n) * 100
            tree.insert("", "end", values=(algo, faults, hits, f"{hr:.2f}%", f"{mr:.2f}%"))

        insert_results("FIFO", fifo_hits, fifo_faults)
        insert_results("Optimal", opt_hits, opt_faults)
        insert_results("LRU", lru_hits, lru_faults)

    ttk.Button(window, text="Simulate All", command=simulate).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_page_replacement()
    root.mainloop()
