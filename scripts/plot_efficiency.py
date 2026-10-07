import csv
import os
import matplotlib.pyplot as plt

INPUT_FILE = "results/openmp_summary.csv"
OUTPUT_FILE = "graphs/openmp_efficiency.png"

os.makedirs("graphs", exist_ok=True)

data = {}

with open(INPUT_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        dataset = int(row["dataset_size"])
        threads = int(row["threads"])
        efficiency = float(row["efficiency_percent"])

        if threads not in data:
            data[threads] = []

        data[threads].append((dataset, efficiency))


plt.figure(figsize=(10, 6))

for threads in sorted(data):
    values = sorted(data[threads])

    datasets = [x[0] for x in values]
    efficiencies = [x[1] for x in values]

    plt.plot(
        datasets,
        efficiencies,
        marker="o",
        label=f"{threads} threads"
    )

plt.xlabel("Dataset Size")
plt.ylabel("Parallel Efficiency (%)")
plt.title("OpenMP Parallel Efficiency vs Dataset Size")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

print(f"Graph saved to: {OUTPUT_FILE}")