import csv
import os
import matplotlib.pyplot as plt

INPUT_FILE = "results/mpi_summary.csv"
OUTPUT_FILE = "graphs/mpi_execution_time.png"

os.makedirs("graphs", exist_ok=True)

data = {}

with open(INPUT_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        dataset = int(row["dataset_size"])
        processes = int(row["processes"])
        time = float(row["mpi_avg"])

        if processes not in data:
            data[processes] = []

        data[processes].append((dataset, time))


plt.figure(figsize=(10, 6))

for processes in sorted(data):
    values = sorted(data[processes])

    datasets = [x[0] for x in values]
    times = [x[1] for x in values]

    plt.plot(
        datasets,
        times,
        marker="o",
        label=f"{processes} processes"
    )

plt.xlabel("Dataset Size")
plt.ylabel("Average Execution Time (seconds)")
plt.title("MPI Execution Time vs Dataset Size")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

print(f"Graph saved to: {OUTPUT_FILE}")