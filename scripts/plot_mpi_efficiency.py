import csv
import os
import matplotlib.pyplot as plt

INPUT_FILE = "results/mpi_summary.csv"
OUTPUT_FILE = "graphs/mpi_efficiency.png"

os.makedirs("graphs", exist_ok=True)

data = {}

with open(INPUT_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        dataset = int(row["dataset_size"])
        processes = int(row["processes"])
        efficiency = float(row["efficiency_percent"])

        if processes not in data:
            data[processes] = []

        data[processes].append((dataset, efficiency))


plt.figure(figsize=(10, 6))

for processes in sorted(data):
    values = sorted(data[processes])

    datasets = [x[0] for x in values]
    efficiencies = [x[1] for x in values]

    plt.plot(
        datasets,
        efficiencies,
        marker="o",
        label=f"{processes} processes"
    )

plt.xlabel("Dataset Size")
plt.ylabel("Parallel Efficiency (%)")
plt.title("MPI Parallel Efficiency vs Dataset Size")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

print(f"Graph saved to: {OUTPUT_FILE}")