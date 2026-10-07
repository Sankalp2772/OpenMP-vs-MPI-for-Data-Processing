import csv
import statistics
import os

SEQUENTIAL_FILE = "results/sequential_raw.csv"
MPI_FILE = "results/mpi_raw.csv"
SUMMARY_FILE = "results/mpi_summary.csv"


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


def read_mpi_data():

    data = {}

    with open(MPI_FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            dataset = int(row["dataset_size"])
            processes = int(row["processes"])
            time = float(row["execution_time"])

            key = (dataset, processes)

            if key not in data:
                data[key] = []

            data[key].append(time)

    return data


def main():

    sequential = read_sequential_data()
    mpi = read_mpi_data()

    os.makedirs("results", exist_ok=True)

    with open(SUMMARY_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "dataset_size",
            "processes",
            "sequential_avg",
            "mpi_avg",
            "speedup",
            "efficiency_percent"
        ])

        for (dataset, processes), times in sorted(mpi.items()):

            sequential_avg = statistics.mean(
                sequential[dataset]
            )

            mpi_avg = statistics.mean(times)

            speedup = sequential_avg / mpi_avg

            efficiency = (
                speedup / processes
            ) * 100

            writer.writerow([
                dataset,
                processes,
                f"{sequential_avg:.6f}",
                f"{mpi_avg:.6f}",
                f"{speedup:.4f}",
                f"{efficiency:.2f}"
            ])

    print("==========================================")
    print("MPI Analysis Completed")
    print("==========================================")
    print(f"Summary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()