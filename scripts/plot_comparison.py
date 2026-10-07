import csv
import os
import matplotlib.pyplot as plt

OPENMP_FILE = "results/openmp_summary.csv"
MPI_FILE = "results/mpi_summary.csv"

OUTPUT_FILE = "graphs/openmp_vs_mpi_100m.png"

TARGET_DATASET = 100000000

os.makedirs("graphs", exist_ok=True)

labels = []
times = []

# -----------------------------
# Read OpenMP results
# -----------------------------

with open(OPENMP_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        dataset = int(row["dataset_size"])
        threads = int(row["threads"])

        if dataset == TARGET_DATASET:

            if threads == 1:
                labels.append("OpenMP 1")
                times.append(float(row["openmp_avg"]))

            elif threads == 2:
                labels.append("OpenMP 2")
                times.append(float(row["openmp_avg"]))

            elif threads == 4:
                labels.append("OpenMP 4")
                times.append(float(row["openmp_avg"]))

            elif threads == 8:
                labels.append("OpenMP 8")
                times.append(float(row["openmp_avg"]))

            elif threads == 12:
                labels.append("OpenMP 12")
                times.append(float(row["openmp_avg"]))


# -----------------------------
# Read MPI results
# -----------------------------

with open(MPI_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        dataset = int(row["dataset_size"])
        processes = int(row["processes"])

        if dataset == TARGET_DATASET:

            if processes == 1:
                labels.append("MPI 1")
                times.append(float(row["mpi_avg"]))

            elif processes == 2:
                labels.append("MPI 2")
                times.append(float(row["mpi_avg"]))

            elif processes == 4:
                labels.append("MPI 4")
                times.append(float(row["mpi_avg"]))

            elif processes == 8:
                labels.append("MPI 8")
                times.append(float(row["mpi_avg"]))


# -----------------------------
# Add sequential baseline
# -----------------------------

with open(OPENMP_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        dataset = int(row["dataset_size"])

        if dataset == TARGET_DATASET:

            labels.insert(0, "Sequential")
            times.insert(0, float(row["sequential_avg"]))

            break


# -----------------------------
# Plot
# -----------------------------

plt.figure(figsize=(12, 6))

plt.bar(labels, times)

plt.xlabel("Implementation")
plt.ylabel("Average Execution Time (seconds)")
plt.title("Sequential vs OpenMP vs MPI — 100M Dataset")

plt.xticks(rotation=30)

plt.grid(axis="y")

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

print(f"Graph saved to: {OUTPUT_FILE}")