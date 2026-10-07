import csv
import os
import matplotlib.pyplot as plt

OPENMP_FILE = "results/openmp_summary.csv"
MPI_FILE = "results/mpi_summary.csv"

OUTPUT_FILE = "graphs/openmp_vs_mpi_speedup_100m.png"

TARGET_DATASET = 100000000

labels = []
speedups = []

# Sequential baseline
labels.append("Sequential")
speedups.append(1.0)

# OpenMP
with open(OPENMP_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if int(row["dataset_size"]) == TARGET_DATASET:
            threads = int(row["threads"])

            if threads in [2, 4, 8, 12]:
                labels.append(f"OpenMP {threads}")
                speedups.append(float(row["speedup"]))

# MPI
with open(MPI_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if int(row["dataset_size"]) == TARGET_DATASET:
            processes = int(row["processes"])

            if processes in [2, 4, 8]:
                labels.append(f"MPI {processes}")
                speedups.append(float(row["speedup"]))

os.makedirs("graphs", exist_ok=True)

plt.figure(figsize=(11, 6))

plt.bar(labels, speedups)

plt.axhline(
    y=1.0,
    linestyle="--",
    label="Sequential baseline"
)

plt.xlabel("Implementation")
plt.ylabel("Speedup")
plt.title("OpenMP vs MPI Speedup — 100M Dataset")

plt.xticks(rotation=30)

plt.legend()
plt.grid(axis="y")

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

print(f"Graph saved to: {OUTPUT_FILE}")