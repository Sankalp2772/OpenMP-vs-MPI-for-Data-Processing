import csv
import statistics
import os

SEQUENTIAL_FILE = "results/sequential_raw.csv"
OPENMP_FILE = "results/openmp_raw.csv"
SUMMARY_FILE = "results/openmp_summary.csv"


def read_sequential_data():
    data = {}

    with open(SEQUENTIAL_FILE, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            dataset = int(row["dataset_size"])
            time = float(row["execution_time"])

            if dataset not in data:
                data[dataset] = []

            data[dataset].append(time)

    return data


def read_openmp_data():
    data = {}

    with open(OPENMP_FILE, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            dataset = int(row["dataset_size"])
            threads = int(row["threads"])
            time = float(row["execution_time"])

            key = (dataset, threads)

            if key not in data:
                data[key] = []

            data[key].append(time)

    return data


def main():

    sequential = read_sequential_data()
    openmp = read_openmp_data()

    os.makedirs("results", exist_ok=True)

    with open(SUMMARY_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "dataset_size",
            "threads",
            "sequential_avg",
            "openmp_avg",
            "speedup",
            "efficiency_percent"
        ])

        for (dataset, threads), times in sorted(openmp.items()):

            sequential_avg = statistics.mean(sequential[dataset])
            openmp_avg = statistics.mean(times)

            speedup = sequential_avg / openmp_avg

            efficiency = (speedup / threads) * 100

            writer.writerow([
                dataset,
                threads,
                f"{sequential_avg:.6f}",
                f"{openmp_avg:.6f}",
                f"{speedup:.4f}",
                f"{efficiency:.2f}"
            ])

    print("==========================================")
    print("OpenMP Analysis Completed")
    print("==========================================")
    print(f"Summary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()