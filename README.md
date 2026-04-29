# 🖥️ Operating System Simulator

Welcome to the **Operating System Simulator**! This is a comprehensive educational tool built in Python to help students and developers visualize core Operating System concepts through interactive simulations.

---

## 🚀 Overview

This simulator provides a graphical interface to explore and understand three fundamental pillars of Operating Systems:
1. **CPU Scheduling**: How processes share the processor.
2. **Contiguous Memory Allocation**: How memory blocks are assigned to processes.
3. **Page Replacement**: How memory management handles page faults in virtual memory.

Built with **Tkinter** for the UI and **Matplotlib** for visualization, it offers a seamless and informative experience.

---

## ✨ Features

### 1. 🕒 CPU Scheduling Algorithms
Simulate how different strategies impact process execution:
- **FCFS** (First-Come, First-Served)
- **SJF (Non-preemptive)** (Shortest Job First)
- **SJF (Preemptive / SRTF)** (Shortest Remaining Time First)
- **Round Robin** (Time-shared execution with a custom quantum)
- **Visualization**: Generates a dynamic **Gantt Chart** with clear start and completion/interruption time labels.
- **Metrics**: Computes Completion Time, Turnaround Time, and Waiting Time for every process.

### 2. 💾 Contiguous Memory Allocation
Explore how memory is managed in a contiguous space:
- **First Fit**: Allocates the first block that is big enough.
- **Best Fit**: Allocates the smallest block that is big enough.
- **Worst Fit**: Allocates the largest available block.
- **Metrics**: Tracks Process size, Block allocation, and **Internal Fragmentation**.

### 3. 📄 Page Replacement Algorithms
Analyze memory paging efficiency:
- **FIFO** (First-In, First-Out)
- **Optimal**: Replaces the page that will not be used for the longest time.
- **LRU** (Least Recently Used)
- **Metrics**: Displays Page Faults, Page Hits, Hit Ratio, and Miss Ratio for all algorithms simultaneously for easy comparison.

---

## 🛠️ Technologies Used

- **Python 3.x**: Core logic and scripting.
- **Tkinter**: Native GUI framework for the user interface.
- **Matplotlib**: Used for drawing professional-grade Gantt charts.
- **ttk.Treeview**: For clean, tabulated data representation.

---

## 📁 Project Structure

```text
OS Simulator/
├── main.py                # Entry point & Main Menu
├── cpu_scheduling.py      # CPU Scheduling logic & UI
├── memory_allocation.py   # Memory Allocation logic & UI
├── page_replacement.py    # Page Replacement logic & UI
├── README.md              # Project Documentation (You are here)
├── README.txt             # Legacy documentation
└── .gitignore             # Python ignore rules
```

---

## ⚙️ Installation & Setup

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

---

## 📖 Usage Guide

### CPU Scheduling
1. Enter the **Number of Processes**.
2. Click **Set Processes** to generate input fields.
3. Input **Arrival Times** (defaults to 0 if empty) and **Burst Times**.
4. Choose an algorithm and set the **Quantum** if using Round Robin.
5. Click **Simulate** to see the table results and the pop-up Gantt Chart.

### Memory Allocation
1. Provide **Free Memory Blocks** as comma-separated integers (e.g., `100, 500, 200`).
2. Provide **Process Memory Requests** as comma-separated integers (e.g., `212, 417`).
3. Select an allocation strategy and click **Simulate**.

### Page Replacement
1. Set the **Frame Size** (number of memory frames).
2. Input the **Reference String** (comma-separated page requests).
3. Click **Simulate All** to compare FIFO, Optimal, and LRU results instantly.

---

## 📊 Sample Output Visualization

- **Gantt Chart**: A clear timeline showing when each process starts and ends.
- **Tabulated Data**: High-level statistics including Average Waiting and Turnaround times.
- **Fragmentation Tracking**: Clear indication of wasted memory space in allocation simulations.

---

## 📝 License

This project was developed for educational purposes as part of an Operating Systems course. 

---

### 🌟 Happy Simulating! 🌟
