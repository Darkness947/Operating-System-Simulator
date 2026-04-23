import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

def open_cpu_scheduling():
    window = tk.Toplevel()
    window.title("CPU Scheduling Algorithms")
    window.geometry("800x600")

    # Algorithm selector
    algos = ["FCFS", "SJF (Non-preemptive)", "SJF (Preemptive)", "Round Robin"]
    algo_var = tk.StringVar(value=algos[0])
    
    control_frame = ttk.Frame(window, padding=10)
    control_frame.pack(fill='x')
    
    ttk.Label(control_frame, text="Select Algorithm:").grid(row=0, column=0, padx=5, pady=5)
    algo_dropdown = ttk.Combobox(control_frame, textvariable=algo_var, values=algos, state="readonly")
    algo_dropdown.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(control_frame, text="Number of Processes:").grid(row=0, column=2, padx=5, pady=5)
    spin_n = ttk.Spinbox(control_frame, from_=1, to=20, width=5)
    spin_n.set(3)
    spin_n.grid(row=0, column=3, padx=5, pady=5)
    
    ttk.Label(control_frame, text="Quantum (RR only):").grid(row=0, column=4, padx=5, pady=5)
    entry_q = ttk.Entry(control_frame, width=5)
    entry_q.insert(0, "2")
    entry_q.grid(row=0, column=5, padx=5, pady=5)

    input_frame_container = ttk.Frame(window)
    input_frame_container.pack(fill='both', expand=True, padx=10, pady=5)
    
    # Canvas for scrolling if many processes
    canvas = tk.Canvas(input_frame_container)
    scrollbar = ttk.Scrollbar(input_frame_container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    entries = []

    def generate_fields():
        # Clear existing
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        entries.clear()
        
        try:
            n = int(spin_n.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of processes")
            return
            
        ttk.Label(scrollable_frame, text="Process", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(scrollable_frame, text="Arrival Time", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(scrollable_frame, text="Burst Time", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=10, pady=5)
        
        for i in range(n):
            ttk.Label(scrollable_frame, text=f"P{i+1}").grid(row=i+1, column=0, padx=10, pady=2)
            arr_entry = ttk.Entry(scrollable_frame, width=10)
            arr_entry.grid(row=i+1, column=1, padx=10, pady=2)
            # Default empty arrival -> 0 handled in logic, but visually we can leave it empty
            burst_entry = ttk.Entry(scrollable_frame, width=10)
            burst_entry.grid(row=i+1, column=2, padx=10, pady=2)
            entries.append((arr_entry, burst_entry))

    ttk.Button(control_frame, text="Set Processes", command=generate_fields).grid(row=1, column=0, columnspan=2, pady=10)
    generate_fields() # Default call

    # Result Table
    res_frame = ttk.Frame(window, padding=10)
    res_frame.pack(fill='both', expand=True)

    columns = ("pid", "arr", "burst", "comp", "tat", "wt")
    tree = ttk.Treeview(res_frame, columns=columns, show="headings", height=8)
    tree.heading("pid", text="Process")
    tree.heading("arr", text="Arrival Time")
    tree.heading("burst", text="Burst Time")
    tree.heading("comp", text="Completion Time")
    tree.heading("tat", text="Turnaround Time")
    tree.heading("wt", text="Waiting Time")
    
    tree.column("pid", width=80, anchor='center')
    tree.column("arr", width=100, anchor='center')
    tree.column("burst", width=100, anchor='center')
    tree.column("comp", width=120, anchor='center')
    tree.column("tat", width=120, anchor='center')
    tree.column("wt", width=100, anchor='center')
    
    tree.pack(fill='both', expand=True, side='left')
    
    stats_lbl = ttk.Label(window, text="Avg Turnaround: 0.00 | Avg Waiting: 0.00", font=("Segoe UI", 12, "bold"))
    stats_lbl.pack(pady=5)

    def draw_gantt(gantt_data):
        colors = plt.cm.tab20.colors
        fig, ax = plt.subplots(figsize=(10, 2))
        
        y_ticks = [10]
        y_labels = ["CPU"]
        
        xticks = set()
        for i, block in enumerate(gantt_data):
            pid, start, duration = block
            xticks.add(start)
            xticks.add(start + duration)
            
            if pid == "Idle":
                ax.broken_barh([(start, duration)], (5, 10), facecolors='gray', edgecolor='black', hatch='/')
                ax.text(start + duration/2, 10, "Idle", ha='center', va='center', color='white')
            else:
                p_num = int(pid.replace("P", ""))
                color = colors[p_num % len(colors)]
                ax.broken_barh([(start, duration)], (5, 10), facecolors=color, edgecolor='black')
                ax.text(start + duration/2, 10, pid, ha='center', va='center', color='black')

        xticks = sorted(list(xticks))
        
        ax.set_ylim(0, 20)
        ax.set_xlim(0, gantt_data[-1][1] + gantt_data[-1][2] + 2 if gantt_data else 10)
        ax.set_xlabel('Time')
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks)
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        plt.title('Gantt Chart')
        plt.tight_layout()
        plt.show(block=False)

    def simulate():
        processes = []
        for i, (arr_e, burst_e) in enumerate(entries):
            arr_val = arr_e.get().strip()
            burst_val = burst_e.get().strip()
            
            arr = int(arr_val) if arr_val else 0
            if not burst_val:
                messagebox.showerror("Error", f"Burst time missing for P{i+1}")
                return
            burst = int(burst_val)
            if burst <= 0:
                messagebox.showerror("Error", f"Burst time must be positive for P{i+1}")
                return
            processes.append({"pid": f"P{i+1}", "arrival": arr, "burst": burst})
        
        algo = algo_var.get()
        results = []
        gantt_data = []

        # Remove existing items in tree
        for item in tree.get_children():
            tree.delete(item)

        if algo == "FCFS":
            procs = sorted(processes, key=lambda x: x['arrival'])
            current_time = 0
            for p in procs:
                if current_time < p['arrival']:
                    gantt_data.append(("Idle", current_time, p['arrival'] - current_time))
                    current_time = p['arrival']
                start_time = current_time
                current_time += p['burst']
                gantt_data.append((p['pid'], start_time, p['burst']))
                comp = current_time
                tat = comp - p['arrival']
                wt = tat - p['burst']
                results.append({"pid": p['pid'], "arr": p['arrival'], "burst": p['burst'], "comp": comp, "tat": tat, "wt": wt})

        elif algo == "SJF (Non-preemptive)":
            procs = sorted([dict(p) for p in processes], key=lambda x: x['arrival'])
            completed = []
            current_time = 0
            while procs:
                ready_queue = [p for p in procs if p['arrival'] <= current_time]
                if not ready_queue:
                    next_arrival = min([p['arrival'] for p in procs])
                    gantt_data.append(("Idle", current_time, next_arrival - current_time))
                    current_time = next_arrival
                    continue
                
                # Pick shortest burst
                ready_queue.sort(key=lambda x: x['burst'])
                p = ready_queue[0]
                procs.remove(p)
                
                start_time = current_time
                current_time += p['burst']
                gantt_data.append((p['pid'], start_time, p['burst']))
                comp = current_time
                tat = comp - p['arrival']
                wt = tat - p['burst']
                completed.append({"pid": p['pid'], "arr": p['arrival'], "burst": p['burst'], "comp": comp, "tat": tat, "wt": wt})
            results = completed

        elif algo == "SJF (Preemptive)": # SRTF
            procs = [dict(p) for p in processes]
            for p in procs:
                p['rem'] = p['burst']
            current_time = 0
            completed = 0
            n = len(procs)
            last_pid = None
            start_chunk = 0
            
            res_dict = {}
            while completed != n:
                ready_queue = [p for p in procs if p['arrival'] <= current_time and p['rem'] > 0]
                if not ready_queue:
                    if last_pid is not None:
                        gantt_data.append((last_pid, start_chunk, current_time - start_chunk))
                        last_pid = None
                    
                    # Jump to next arrival
                    future_procs = [p for p in procs if p['arrival'] > current_time and p['rem'] > 0]
                    if future_procs:
                        next_arr = min(p['arrival'] for p in future_procs)
                        gantt_data.append(("Idle", current_time, next_arr - current_time))
                        current_time = next_arr
                    continue
                
                ready_queue.sort(key=lambda x: x['rem'])
                p = ready_queue[0]
                
                if last_pid != p['pid']:
                    if last_pid is not None:
                        gantt_data.append((last_pid, start_chunk, current_time - start_chunk))
                    start_chunk = current_time
                    last_pid = p['pid']
                
                p['rem'] -= 1
                current_time += 1
                
                if p['rem'] == 0:
                    completed += 1
                    comp = current_time
                    tat = comp - p['arrival']
                    wt = tat - p['burst']
                    res_dict[p['pid']] = {"pid": p['pid'], "arr": p['arrival'], "burst": p['burst'], "comp": comp, "tat": tat, "wt": wt}
            
            if last_pid is not None:
                gantt_data.append((last_pid, start_chunk, current_time - start_chunk))
                
            for p in processes:
                results.append(res_dict[p['pid']])

        elif algo == "Round Robin":
            try:
                q = int(entry_q.get())
                if q <= 0: raise ValueError
            except:
                messagebox.showerror("Error", "Invalid Quantum size")
                return
                
            procs = [dict(p) for p in processes]
            for p in procs:
                p['rem'] = p['burst']
                
            procs.sort(key=lambda x: x['arrival'])
            queue = []
            current_time = 0
            completed_count = 0
            n = len(procs)
            res_dict = {}
            
            # Find first arrived
            if procs[0]['arrival'] > 0:
                current_time = procs[0]['arrival']
                gantt_data.append(("Idle", 0, current_time))
                
            i = 0
            while i < n and procs[i]['arrival'] <= current_time:
                queue.append(procs[i])
                i += 1
                
            while completed_count < n:
                if not queue:
                    # CPU Idle
                    next_arr = procs[i]['arrival']
                    gantt_data.append(("Idle", current_time, next_arr - current_time))
                    current_time = next_arr
                    while i < n and procs[i]['arrival'] <= current_time:
                        queue.append(procs[i])
                        i += 1
                    continue
                    
                p = queue.pop(0)
                exec_time = min(q, p['rem'])
                gantt_data.append((p['pid'], current_time, exec_time))
                current_time += exec_time
                p['rem'] -= exec_time
                
                # Check for new arrivals during exec_time
                while i < n and procs[i]['arrival'] <= current_time:
                    queue.append(procs[i])
                    i += 1
                    
                if p['rem'] == 0:
                    completed_count += 1
                    comp = current_time
                    tat = comp - p['arrival']
                    wt = tat - p['burst']
                    res_dict[p['pid']] = {"pid": p['pid'], "arr": p['arrival'], "burst": p['burst'], "comp": comp, "tat": tat, "wt": wt}
                else:
                    queue.append(p)
                    
            for p in processes:
                results.append(res_dict[p['pid']])

        # Sort results by PID to look clean (optional, or chronological)
        # Results naturally ordered by completion or arrival depending on algo. Let's just output them directly.
        total_tat = sum(r['tat'] for r in results)
        total_wt = sum(r['wt'] for r in results)
        
        for r in results:
            tree.insert("", "end", values=(r['pid'], r['arr'], r['burst'], r['comp'], r['tat'], r['wt']))
            
        stats_lbl.config(text=f"Avg Turnaround: {total_tat/len(results):.2f} | Avg Waiting: {total_wt/len(results):.2f}")
        
        # Merge adjacent identical blocks in Gantt for SRTF / RR if needed
        merged_gantt = []
        for block in gantt_data:
            if not merged_gantt:
                merged_gantt.append(list(block))
            elif merged_gantt[-1][0] == block[0]:
                merged_gantt[-1][2] += block[2]
            else:
                merged_gantt.append(list(block))
                
        draw_gantt(merged_gantt)

    ttk.Button(window, text="Simulate", command=simulate).pack(pady=10)
    
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_cpu_scheduling()
    root.mainloop()
