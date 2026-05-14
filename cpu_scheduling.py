import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUSchedulingFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
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
        
        # Control frame (no algorithm selector anymore)
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(fill='x')
        
        ttk.Label(control_frame, text="Number of Processes:").grid(row=0, column=0, padx=5, pady=5)
        self.spin_n = ttk.Spinbox(control_frame, from_=1, to=20, width=5)
        self.spin_n.set(3)
        self.spin_n.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Quantum (RR only):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_q = ttk.Entry(control_frame, width=5)
        self.entry_q.insert(0, "2")
        self.entry_q.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(control_frame, text="Set Processes", command=self.generate_fields).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(control_frame, text="Run All Algorithms", command=self.simulate).grid(row=1, column=2, columnspan=2, pady=10)

        # Main PanedWindow for split inputs/results
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill='both', expand=True, padx=10, pady=5)

        # Left: Process input fields
        input_frame_container = ttk.Frame(self.paned)
        self.paned.add(input_frame_container, weight=1)

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

        # Right: Scrollable results area (Notebook with tabs for each algorithm)
        results_container = ttk.Frame(self.paned)
        self.paned.add(results_container, weight=3)

        self.notebook = ttk.Notebook(results_container)
        self.notebook.pack(fill='both', expand=True)

        # We'll create tabs dynamically in simulate(), store references here
        self.algo_tabs = {}
        self.algo_trees = {}
        self.algo_stats = {}
        self.algo_figs = {}
        self.algo_axes = {}
        self.algo_canvas_widgets = {}

        self.generate_fields()  # Default call
        
    def reapply_theme(self, dark_mode):
        self.canvas_scroll.configure(bg='#2d2d2d' if dark_mode else '#f0f0f0')
        # Reapply to all algo charts
        for algo_name in self.algo_figs:
            fig = self.algo_figs[algo_name]
            ax = self.algo_axes[algo_name]
            if dark_mode:
                fig.patch.set_facecolor('#2d2d2d')
                ax.set_facecolor('#333333')
                ax.tick_params(colors='white')
                ax.xaxis.label.set_color('white')
                for spine in ax.spines.values():
                    spine.set_edgecolor('white')
            else:
                fig.patch.set_facecolor('#f0f0f0')
                ax.set_facecolor('white')
                ax.tick_params(colors='black')
                ax.xaxis.label.set_color('black')
                for spine in ax.spines.values():
                    spine.set_edgecolor('black')
            if algo_name in self.algo_canvas_widgets and self.algo_canvas_widgets[algo_name]:
                self.algo_canvas_widgets[algo_name].draw()

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
        ttk.Label(self.scrollable_frame, text="Arrival (ms)", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Burst (ms)", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        
        for i in range(n):
            ttk.Label(self.scrollable_frame, text=f"P{i+1}").grid(row=i+1, column=0, padx=5, pady=2)
            arr_entry = ttk.Entry(self.scrollable_frame, width=8)
            arr_entry.grid(row=i+1, column=1, padx=5, pady=2)
            burst_entry = ttk.Entry(self.scrollable_frame, width=8)
            burst_entry.grid(row=i+1, column=2, padx=5, pady=2)
            self.entries.append((arr_entry, burst_entry))

    def _create_algo_tab(self, algo_name):
        """Create a tab for a single algorithm with table, stats, and chart."""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=algo_name)

        # Scrollable content inside the tab
        tab_canvas = tk.Canvas(tab_frame, highlightthickness=0)
        tab_scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=tab_canvas.yview)
        tab_inner = ttk.Frame(tab_canvas)

        tab_inner.bind(
            "<Configure>",
            lambda e, c=tab_canvas: c.configure(scrollregion=c.bbox("all"))
        )
        tab_canvas.create_window((0, 0), window=tab_inner, anchor="nw")
        tab_canvas.configure(yscrollcommand=tab_scrollbar.set)
        tab_canvas.pack(side="left", fill="both", expand=True)
        tab_scrollbar.pack(side="right", fill="y")

        # Enable mousewheel scrolling
        def _on_mousewheel(event, canvas=tab_canvas):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        tab_canvas.bind("<Enter>", lambda e, c=tab_canvas: c.bind_all("<MouseWheel>", lambda ev: _on_mousewheel(ev, c)))
        tab_canvas.bind("<Leave>", lambda e, c=tab_canvas: c.unbind_all("<MouseWheel>"))

        # Result Table
        columns = ("pid", "arr", "burst", "comp", "tat", "wt")
        tree = ttk.Treeview(tab_inner, columns=columns, show="headings", height=8)
        tree.heading("pid", text="Process")
        tree.heading("arr", text="Arrival (ms)")
        tree.heading("burst", text="Burst (ms)")
        tree.heading("comp", text="Completion (ms)")
        tree.heading("tat", text="Turnaround (ms)")
        tree.heading("wt", text="Waiting (ms)")
        
        tree.column("pid", width=60, anchor='center')
        tree.column("arr", width=80, anchor='center')
        tree.column("burst", width=70, anchor='center')
        tree.column("comp", width=100, anchor='center')
        tree.column("tat", width=100, anchor='center')
        tree.column("wt", width=80, anchor='center')
        
        tree.pack(fill='x', padx=5, pady=5)
        self.algo_trees[algo_name] = tree

        # Stats label
        stats_lbl = ttk.Label(tab_inner, text="", font=("Segoe UI", 11, "bold"))
        stats_lbl.pack(pady=5)
        self.algo_stats[algo_name] = stats_lbl

        # Gantt chart
        fig, ax = plt.subplots(figsize=(8, 2))
        self.algo_figs[algo_name] = fig
        self.algo_axes[algo_name] = ax

        chart_frame = ttk.Frame(tab_inner)
        chart_frame.pack(fill='x', padx=5, pady=5)

        canvas_widget = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas_widget.get_tk_widget().pack(fill='x')
        self.algo_canvas_widgets[algo_name] = canvas_widget

        # Download button
        btn_download = ttk.Button(tab_inner, text="Download Chart",
                                  command=lambda name=algo_name: self.download_chart(name))
        btn_download.pack(pady=5)

        self.algo_tabs[algo_name] = tab_frame
        return tree, stats_lbl, fig, ax, canvas_widget

    def draw_gantt(self, gantt_data, algo_name):
        ax = self.algo_axes[algo_name]
        fig = self.algo_figs[algo_name]
        ax.clear()
        colors = plt.cm.tab20.colors
        
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
        ax.set_xlabel('Time (ms)')
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks)
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        ax.set_title(f'{algo_name} - Gantt Chart', color='white' if self.controller.dark_mode else 'black')
        fig.tight_layout()
        
        self.reapply_theme(self.controller.dark_mode)
        self.algo_canvas_widgets[algo_name].draw()
        
    def download_chart(self, algo_name):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")])
        if file_path:
            fig = self.algo_figs[algo_name]
            fig.savefig(file_path, facecolor=fig.get_facecolor(), edgecolor='none')
            messagebox.showinfo("Success", f"Chart saved to {file_path}")

    def _run_fcfs(self, processes):
        procs = sorted(processes, key=lambda x: x['arrival'])
        current_time = 0
        results = []
        gantt_data = []
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
        return results, gantt_data

    def _run_sjf_np(self, processes):
        procs = sorted([dict(p) for p in processes], key=lambda x: x['arrival'])
        completed = []
        gantt_data = []
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
        return completed, gantt_data

    def _run_sjf_p(self, processes):
        procs = [dict(p) for p in processes]
        for p in procs: p['rem'] = p['burst']
        current_time = 0
        completed = 0
        n = len(procs)
        last_pid = None
        start_chunk = 0
        gantt_data = []
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
            
        results = [res_dict[p['pid']] for p in processes]
        return results, gantt_data

    def _run_rr(self, processes, quantum):
        procs = [dict(p) for p in processes]
        for p in procs: p['rem'] = p['burst']
            
        procs.sort(key=lambda x: x['arrival'])
        queue = []
        current_time = 0
        completed_count = 0
        n = len(procs)
        res_dict = {}
        gantt_data = []
        
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
            exec_time = min(quantum, p['rem'])
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
                
        results = [res_dict[p['pid']] for p in processes]
        return results, gantt_data

    def simulate(self):
        # Parse process inputs
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
        
        # Parse quantum for RR
        try:
            q = int(self.entry_q.get())
            if q <= 0: raise ValueError
        except:
            messagebox.showerror("Error", "Invalid Quantum size for Round Robin")
            return

        # Clear old tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self.algo_tabs.clear()
        self.algo_trees.clear()
        self.algo_stats.clear()
        # Close old figures to free memory
        for fig in self.algo_figs.values():
            plt.close(fig)
        self.algo_figs.clear()
        self.algo_axes.clear()
        self.algo_canvas_widgets.clear()

        # Run all algorithms
        algos = {
            "FCFS": lambda: self._run_fcfs(processes),
            "SJF (Non-preemptive)": lambda: self._run_sjf_np(processes),
            "SJF (Preemptive)": lambda: self._run_sjf_p(processes),
            "Round Robin": lambda: self._run_rr(processes, q),
        }

        for algo_name, algo_func in algos.items():
            results, gantt_data = algo_func()
            tree, stats_lbl, fig, ax, canvas_widget = self._create_algo_tab(algo_name)

            # Populate table
            for r in results:
                tree.insert("", "end", values=(r['pid'], r['arr'], r['burst'], r['comp'], r['tat'], r['wt']))

            # Stats
            total_tat = sum(r['tat'] for r in results)
            total_wt = sum(r['wt'] for r in results)
            stats_lbl.config(text=f"Avg Turnaround: {total_tat/len(results):.2f} ms | Avg Waiting: {total_wt/len(results):.2f} ms")

            # Merge consecutive same-process gantt blocks
            merged_gantt = []
            for block in gantt_data:
                if not merged_gantt:
                    merged_gantt.append(list(block))
                elif merged_gantt[-1][0] == block[0]:
                    merged_gantt[-1][2] += block[2]
                else:
                    merged_gantt.append(list(block))

            self.draw_gantt(merged_gantt, algo_name)
