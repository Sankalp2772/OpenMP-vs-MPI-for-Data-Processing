# OpenMP vs MPI for Data Processing

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## 📌 Project Overview
This repository contains the experimental implementation for a Parallel Computing laboratory project focused on comparing the performance of shared-memory (OpenMP) and message-passing (MPI) paradigms. The project implements a data-processing operation across Sequential, OpenMP, and MPI approaches, experimentally analyzing execution time, speedup, and parallel efficiency.

## 🎯 Problem Statement
To design, implement, and analyze parallel algorithms for a large-scale data processing operation using OpenMP and MPI. The goal is to evaluate their relative performance on a shared-memory architecture and understand the trade-offs between shared-memory multi-threading and message-passing communication overhead.

## 🚀 Objectives
- Implement a baseline sequential version of the data processing algorithm.
- Implement parallel versions using OpenMP (shared memory) and MPI (distributed memory model simulated on shared memory).
- Experimentally evaluate and compare execution time, speedup, and efficiency across different dataset sizes and thread/process counts.
- Analyze the impact of communication and synchronization overheads in MPI versus OpenMP for a compute-light workload.

## 🧮 Mathematical Formulation
For a generated dataset of size `N`, the operation calculates the average of the squares of the elements.

**Dataset Generation:**
$$x[i] = (i \pmod{100}) + 1$$

**Computation:**
$$S = \sum_{i=0}^{N-1} x[i]^2$$
$$\text{AverageSquare} = \frac{S}{N}$$

**Expected Output:** For the above generation logic, the expected `AverageSquare` is always **3383.5**.

## ⚙️ Algorithm
1. Initialize an array of size $N$.
2. Populate the array with values $1, 2, \dots, 100, 1, 2, \dots$
3. Compute the sum of squares of all elements.
4. Divide the sum by $N$ to find the average.

## 🛠️ Methodologies

### OpenMP Methodology
The OpenMP implementation leverages multi-threading within a single process. It uses a parallel `for` loop with a `reduction(+:sum)` clause to parallelize the sum-of-squares calculation. This allows multiple threads to compute partial sums concurrently and safely accumulate them without explicit locks, maximizing shared-memory performance.

### MPI Methodology
The MPI implementation uses the message-passing model.
1. The root process generates the dataset.
2. `MPI_Scatterv` distributes chunks of the array to different processes.
3. Each process performs local computation (sum of squares) on its chunk.
4. `MPI_Reduce` aggregates the local sums back to the root process using the `MPI_SUM` operation.
5. The root process computes the final average.

*Note: The MPI timing intentionally encompasses `MPI_Scatterv`, the local computation, and `MPI_Reduce` to accurately reflect the overall processing time including data distribution and aggregation overhead.*

## 🧪 Experimental Setup

### Experiment Matrix
- **Dataset Sizes ($N$):** 1,000,000 | 10,000,000 | 50,000,000 | 100,000,000
- **Sequential:** 5 runs per dataset.
- **OpenMP Threads:** 1, 2, 4, 8, 12 (5 runs per combination).
- **MPI Processes:** 1, 2, 4, 8 (5 runs per combination).
- **Averaging:** Results represent the average of 5 repetitions to mitigate timing variability, particularly noticeable in extremely short executions of small datasets.

### Hardware/Software Environment
- **Architecture:** Shared-memory machine
- **Languages/Libraries:** C++, OpenMP API, MPI (Message Passing Interface) implementation

## 📊 Results and Analysis

*Note: Detailed raw logs and summaries can be found in the [`results/`](results/) directory.*

### Performance Metrics Definitions
- **Speedup ($S$)** = $T_{\text{sequential}} / T_{\text{parallel}}$
- **Efficiency ($E$)** = $(S / \text{number\_of\_workers}) \times 100\%$

### Key Measurements (100M Dataset)

**Baseline Sequential Execution Time:** 0.107600 s

| Paradigm | Workers | Execution Time (s) | Speedup | Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **OpenMP** | 1 thread | 0.091271 | 1.1789x | >100%* |
| | 2 threads | 0.054297 | 1.9817x | 99.08% |
| | 4 threads | 0.032904 | 3.2702x | 81.75% |
| | 8 threads | 0.031884 | 3.3747x | 42.18% |
| | 12 threads | 0.028256 | 3.8080x | 31.73% |
| **MPI** | 1 process | 1.214828 | 0.0886x | 8.86% |
| | 2 processes | 0.652338 | 0.1649x | 8.25% |
| | 4 processes | 0.438255 | 0.2455x | 6.14% |
| | 8 processes | 0.317580 | 0.3388x | 4.24% |

*\*OpenMP 1-thread efficiency above 100% occurs due to differing baseline compiler optimizations, memory layouts, and runtime effects between a separately compiled sequential executable and the OpenMP executable.*

### 📈 Graphs

*(Ensure to check the [`graphs/`](graphs/) directory for full visual analysis)*

- **OpenMP Performance:** Execution Time | Speedup | Efficiency
- **MPI Performance:** Execution Time | Speedup | Efficiency
- **Comparative (100M):** `openmp_vs_mpi_100m.png` | `openmp_vs_mpi_speedup_100m.png`

## 🔍 Comparative Analysis and Observations

1. **OpenMP Outperforms on Shared Memory:** For this specific, compute-light workload running on a single shared-memory machine, OpenMP significantly outperformed MPI. OpenMP leverages lightweight threads sharing the same address space, resulting in minimal overhead.
2. **MPI Overhead:** The MPI speedup being consistently below 1 is a valid and expected experimental result in this context, not an implementation flaw. The overhead of packing, sending (`MPI_Scatterv`), receiving, and reducing (`MPI_Reduce`) data across separate process memory spaces vastly outweighed the actual computation time (a simple arithmetic operation).
3. **Diminishing Returns:** In OpenMP, speedup increases up to 4-8 threads but efficiency drops rapidly (from ~99% at 2 threads to ~31% at 12 threads). Memory bandwidth saturation and thread management overhead begin to dominate the relatively small computational workload per thread.

## 🏁 Conclusion

This experiment effectively highlights the critical importance of matching the parallel programming paradigm to both the workload characteristics and the underlying hardware architecture.

**It is incorrect to conclude that MPI is inherently slower or inferior to OpenMP.** The accurate conclusion is:
> *For this specific workload on a single shared-memory machine, OpenMP significantly outperformed MPI because MPI introduced substantial inter-process communication and synchronization/runtime overhead. MPI becomes much more attractive—and often necessary—for distributed-memory clusters or highly compute-intensive workloads where the communication costs can be effectively amortized.*

## ⚠️ Limitations
- The operation is heavily memory-bound and computationally simple, meaning memory bandwidth bottlenecks appear early.
- All MPI processes were executed on a single machine, enforcing communication over shared memory/loopback instead of actual network links, which changes the typical MPI latency profile.
- Extremely small datasets suffer from timer resolution limits and background OS noise.

## 📂 Project Structure
```text
openmp-vs-mpi-data-processing/
├── src/
│   ├── sequential.cpp
│   ├── openmp.cpp
│   └── mpi.cpp
├── scripts/
│   ├── run_sequential.sh
│   ├── run_openmp.sh
│   ├── run_mpi.sh
│   └── analyze_*.py / plot_*.py
├── results/
│   └── *.csv (Raw and summary data)
├── graphs/
│   └── *.png (Visualizations)
└── README.md
```

## 💻 Reproducibility Instructions
1. Clone the repository: `git clone https://github.com/Sankalp2772/OpenMP-vs-MPI-for-Data-Processing.git`
2. Compile the sources in `src/` using `g++` (for sequential), `g++ -fopenmp` (for OpenMP), and `mpic++` (for MPI).
3. Run the shell scripts in the `scripts/` directory to generate data.
4. Execute the Python analysis scripts to process the CSVs and generate graphs.

## 🔮 Future Improvements
- Test the MPI implementation on a genuine distributed computing cluster (multiple nodes).
- Implement a more compute-intensive kernel (e.g., matrix multiplication or N-body simulation) to observe how an increased computation-to-communication ratio affects MPI's relative performance.
- Profile cache misses and memory bandwidth utilization to better explain OpenMP's diminishing returns at higher thread counts.
