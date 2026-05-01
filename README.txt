OS Simulator
======================

This is an Operating System Simulator developed in Python using Tkinter for the GUI, ttk.Treeview for tabulated outputs, and Matplotlib for visualizing Gantt charts.

Features Simulated:
-------------------
1. CPU Scheduling Algorithms (FCFS, SJF Preemptive & Non-preemptive, Round Robin)
2. Contiguous Memory Allocation (First Fit, Best Fit, Worst Fit)
3. Page Replacement Algorithms (FIFO, Optimal, LRU)

Prerequisites:
--------------
- Python 3.8+
- Tkinter (Usually included in the standard Python library)
- Matplotlib

To compile/run the program:
---------------------------

You can run this application either from the source Python files or directly via the bundled executable.

### Option 1: Run via Executable (No installation required)
1. Navigate to the `dist/` folder in the project directory.
2. Double-click `main.exe` to launch the OS Simulator immediately.

### Option 2: Run via Python Source
1. **Clone or Download** the project files to your local machine.
2. **Install Dependencies**:
   Ensure you have `matplotlib` installed. If not, run:
   ```bash
   pip install matplotlib
   ```
3. **Run the Application**:
   Execute the `main.py` script from the terminal:
   ```bash
   python main.py
   ```


Expected Outputs Based on Mock Datasets:
----------------------------------------
1. CPU Scheduling (FCFS):
   Processes: 3
   Arrival Times: 0, 1, 2
   Burst Times: 5, 3, 8
   Output expected: Gantt Chart from 0-16. Process 1 (0-5), Process 2 (5-8), Process 3 (8-16), and Average Waiting Time: 3.33.

2. Memory Allocation (First Fit):
   Free Blocks: 100, 500, 200, 300, 600
   Process Requests: 212, 417, 112, 426
   Output expected: 
   Process 1 (212) -> Block 2 (500)
   Process 2 (417) -> Block 5 (600)
   Process 3 (112) -> Block 2 (remaining 288)
   Process 4 (426) -> Unallocated (no block large enough)

3. Page Replacement (FIFO):
   Frame Size: 3
   Reference String: 7,0,1,2,0,3,0,4,2,3,0,3,2,1,2
   Output expected: Number of Page Faults: 12

Note: Ensure all inputs are separated by commas where lists/sequences are needed as instructed in the respective simulation windows.
