import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUSchedulingFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.fig, self.ax = plt.subplots(figsize=(8, 2))
        self.canvas_widget = None
        
        self._build_ui()
        self.reapply_theme(self.controller.dark_mode)

    def _build_ui(self):
        # Top Bar
        top_bar = ttk.Frame(self)
        top_bar.pack(fill='x', padx=10, pady=5)
        
        btn_back = ttk.Button(top_bar, text="← Back to Menu", command=lambda: self.controller.show_frame('menu'))
        btn_back.pack(side='left')
        
        lbl_title = ttk.Label(top_bar, text="CPU Scheduling Algorithms", font=("Segoe UI", 16, "bold"))
        lbl_title.pack(side='left', padx=20)
        
        # Algorithm selector
        algos = ["FCFS", "SJF (Non-preemptive)", "SJF (Preemptive)", "Round Robin"]
        self.algo_var = tk.StringVar(value=algos[0])
        
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(fill='x')
        
        ttk.Label(control_frame, text="Select Algorithm:").grid(row=0, column=0, padx=5, pady=5)
        algo_dropdown = ttk.Combobox(control_frame, textvariable=self.algo_var, values=algos, state="readonly")
        algo_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Number of Processes:").grid(row=0, column=2, padx=5, pady=5)
        self.spin_n = ttk.Spinbox(control_frame, from_=1, to=20, width=5)
        self.spin_n.set(3)
        self.spin_n.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Quantum (RR only):").grid(row=0, column=4, padx=5, pady=5)
        self.entry_q = ttk.Entry(control_frame, width=5)
        self.entry_q.insert(0, "2")
        self.entry_q.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(control_frame, text="Set Processes", command=self.generate_fields).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(control_frame, text="Simulate", command=self.simulate).grid(row=1, column=2, columnspan=2, pady=10)
        
        self.btn_download = ttk.Button(control_frame, text="Download Chart", command=self.download_chart, state="disabled")
        self.btn_download.grid(row=1, column=4, columnspan=2, pady=10)

        # Main PanedWindow for split inputs/results and chart
        self.paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.paned.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Upper part: Inputs and Table
        upper_frame = ttk.Frame(self.paned)
        self.paned.add(upper_frame, weight=1)

        # Canvas for scrolling if many processes
        input_frame_container = ttk.Frame(upper_frame)
        input_frame_container.pack(side='left', fill='both', expand=True)

        self.canvas_scroll = tk.Canvas(input_frame_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(input_frame_container, orient="vertical", command=self.canvas_scroll.yview)
        self.scrollable_frame = ttk.Frame(self.canvas_scroll)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))
        )

        self.canvas_scroll.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_scroll.configure(yscrollcommand=scrollbar.set)
        self.canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.entries = []

        # Result Table
        res_frame = ttk.Frame(upper_frame, padding=10)
        res_frame.pack(side='right', fill='both', expand=True)

        columns = ("pid", "arr", "burst", "comp", "tat", "wt")
        self.tree = ttk.Treeview(res_frame, columns=columns, show="headings", height=8)
        self.tree.heading("pid", text="Process")
        self.tree.heading("arr", text="Arrival")
        self.tree.heading("burst", text="Burst")
        self.tree.heading("comp", text="Completion")
        self.tree.heading("tat", text="Turnaround")
        self.tree.heading("wt", text="Waiting")
        
        self.tree.column("pid", width=60, anchor='center')
        self.tree.column("arr", width=60, anchor='center')
        self.tree.column("burst", width=60, anchor='center')
        self.tree.column("comp", width=80, anchor='center')
        self.tree.column("tat", width=80, anchor='center')
        self.tree.column("wt", width=60, anchor='center')
        
        self.tree.pack(fill='both', expand=True)
        
        self.stats_lbl = ttk.Label(self, text="Avg Turnaround: 0.00 | Avg Waiting: 0.00", font=("Segoe UI", 12, "bold"))
        self.stats_lbl.pack(pady=5)

        # Lower part: Chart
        self.chart_frame = ttk.Frame(self.paned)
        self.paned.add(self.chart_frame, weight=1)

        self.generate_fields() # Default call
        
    def reapply_theme(self, dark_mode):
        if dark_mode:
            self.canvas_scroll.configure(bg='#2d2d2d')
            self.fig.patch.set_facecolor('#2d2d2d')
            self.ax.set_facecolor('#333333')
            self.ax.tick_params(colors='white')
            self.ax.xaxis.label.set_color('white')
            for spine in self.ax.spines.values():
                spine.set_edgecolor('white')
        else:
            self.canvas_scroll.configure(bg='#f0f0f0')
            self.fig.patch.set_facecolor('#f0f0f0')
            self.ax.set_facecolor('white')
            self.ax.tick_params(colors='black')
            self.ax.xaxis.label.set_color('black')
            for spine in self.ax.spines.values():
                spine.set_edgecolor('black')
                
        if self.canvas_widget:
            self.canvas_widget.draw()

    def generate_fields(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.entries.clear()
        
        try:
            n = int(self.spin_n.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of processes")
            return
            
        ttk.Label(self.scrollable_frame, text="Process", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Arrival", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Burst", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        
        for i in range(n):
            ttk.Label(self.scrollable_frame, text=f"P{i+1}").grid(row=i+1, column=0, padx=5, pady=2)
            arr_entry = ttk.Entry(self.scrollable_frame, width=8)
            arr_entry.grid(row=i+1, column=1, padx=5, pady=2)
            burst_entry = ttk.Entry(self.scrollable_frame, width=8)
            burst_entry.grid(row=i+1, column=2, padx=5, pady=2)
            self.entries.append((arr_entry, burst_entry))

    def draw_gantt(self, gantt_data):
        self.ax.clear()
        colors = plt.cm.tab20.colors
        
        y_ticks = [10]
        y_labels = ["CPU"]
        
        xticks = set()
        for i, block in enumerate(gantt_data):
            pid, start, duration = block
            xticks.add(start)
            xticks.add(start + duration)
            
            if pid == "Idle":
                self.ax.broken_barh([(start, duration)], (5, 10), facecolors='gray', edgecolor='black', hatch='/')
                self.ax.text(start + duration/2, 10, "Idle", ha='center', va='center', color='white')
            else:
                p_num = int(pid.replace("P", ""))
                color = colors[p_num % len(colors)]
                self.ax.broken_barh([(start, duration)], (5, 10), facecolors=color, edgecolor='black')
                self.ax.text(start + duration/2, 10, pid, ha='center', va='center', color='black')

        xticks = sorted(list(xticks))
        
        self.ax.set_ylim(0, 20)
        self.ax.set_xlim(0, gantt_data[-1][1] + gantt_data[-1][2] + 2 if gantt_data else 10)
        self.ax.set_xlabel('Time')
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(xticks)
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels(y_labels)
        self.ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        self.ax.set_title('Gantt Chart', color='white' if self.controller.dark_mode else 'black')
        self.fig.tight_layout()
        
        self.reapply_theme(self.controller.dark_mode)

        if not self.canvas_widget:
            self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
            self.canvas_widget.get_tk_widget().pack(fill='both', expand=True)
            
        self.canvas_widget.draw()
        self.btn_download.config(state="normal")
        
    def download_chart(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")])
        if file_path:
            self.fig.savefig(file_path, facecolor=self.fig.get_facecolor(), edgecolor='none')
            messagebox.showinfo("Success", f"Chart saved to {file_path}")

    def simulate(self):
        processes = []
        for i, (arr_e, burst_e) in enumerate(self.entries):
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
        
        algo = self.algo_var.get()
        results = []
        gantt_data = []

        for item in self.tree.get_children():
            self.tree.delete(item)

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

        elif algo == "SJF (Preemptive)":
            procs = [dict(p) for p in processes]
            for p in procs: p['rem'] = p['burst']
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
                
            for p in processes: results.append(res_dict[p['pid']])

        elif algo == "Round Robin":
            try:
                q = int(self.entry_q.get())
                if q <= 0: raise ValueError
            except:
                messagebox.showerror("Error", "Invalid Quantum size")
                return
                
            procs = [dict(p) for p in processes]
            for p in procs: p['rem'] = p['burst']
                
            procs.sort(key=lambda x: x['arrival'])
            queue = []
            current_time = 0
            completed_count = 0
            n = len(procs)
            res_dict = {}
            
            if procs[0]['arrival'] > 0:
                current_time = procs[0]['arrival']
                gantt_data.append(("Idle", 0, current_time))
                
            i = 0
            while i < n and procs[i]['arrival'] <= current_time:
                queue.append(procs[i])
                i += 1
                
            while completed_count < n:
                if not queue:
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
                    
            for p in processes: results.append(res_dict[p['pid']])

        total_tat = sum(r['tat'] for r in results)
        total_wt = sum(r['wt'] for r in results)
        
        for r in results:
            self.tree.insert("", "end", values=(r['pid'], r['arr'], r['burst'], r['comp'], r['tat'], r['wt']))
            
        self.stats_lbl.config(text=f"Avg Turnaround: {total_tat/len(results):.2f} | Avg Waiting: {total_wt/len(results):.2f}")
        
        merged_gantt = []
        for block in gantt_data:
            if not merged_gantt:
                merged_gantt.append(list(block))
            elif merged_gantt[-1][0] == block[0]:
                merged_gantt[-1][2] += block[2]
            else:
                merged_gantt.append(list(block))
                
        self.draw_gantt(merged_gantt)
