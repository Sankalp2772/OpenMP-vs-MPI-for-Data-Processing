import csv
import os
import matplotlib.pyplot as plt

INPUT_FILE = "results/openmp_summary.csv"
OUTPUT_FILE = "graphs/openmp_speedup.png"

os.makedirs("graphs", exist_ok=True)

data = {}

with open(INPUT_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        dataset = int(row["dataset_size"])
        threads = int(row["threads"])
        speedup = float(row["speedup"])

        if threads not in data:
            data[threads] = []

        data[threads].append((dataset, speedup))


plt.figure(figsize=(10, 6))

for threads in sorted(data):
    values = sorted(data[threads])

    datasets = [x[0] for x in values]
    speedups = [x[1] for x in values]

    plt.plot(
        datasets,
        speedups,
        marker="o",
        label=f"{threads} threads"
    )

plt.xlabel("Dataset Size")
plt.ylabel("Speedup")
plt.title("OpenMP Speedup vs Dataset Size")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

print(f"Graph saved to: {OUTPUT_FILE}")