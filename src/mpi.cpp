#include <mpi.h>
#include <iostream>
#include <vector>
#include <chrono>
#include <cstdlib>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {

    MPI_Init(&argc, &argv);

    int rank, size;

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    long long N = 10000000;

    if (argc > 1) {
        N = atoll(argv[1]);
    }

    // ----------------------------------------
    // Calculate how much data each process gets
    // ----------------------------------------

    vector<int> counts(size);
    vector<int> displacements(size);

    long long base = N / size;
    long long remainder = N % size;

    for (int i = 0; i < size; i++) {
        counts[i] = base + (i < remainder ? 1 : 0);
    }

    displacements[0] = 0;

    for (int i = 1; i < size; i++) {
        displacements[i] =
            displacements[i - 1] + counts[i - 1];
    }

    // ----------------------------------------
    // Root process creates the complete dataset
    // ----------------------------------------

    vector<double> data;

    if (rank == 0) {

        data.resize(N);

        for (long long i = 0; i < N; i++) {
            data[i] = (i % 100) + 1;
        }
    }

    // ----------------------------------------
    // Each process receives its portion
    // ----------------------------------------

    vector<double> local_data(counts[rank]);

    // Synchronize before timing
    MPI_Barrier(MPI_COMM_WORLD);

    double start = MPI_Wtime();

    MPI_Scatterv(
        rank == 0 ? data.data() : nullptr,
        counts.data(),
        displacements.data(),
        MPI_DOUBLE,
        local_data.data(),
        counts[rank],
        MPI_DOUBLE,
        0,
        MPI_COMM_WORLD
    );

    // ----------------------------------------
    // Local computation
    // ----------------------------------------

    double local_sum = 0.0;

    for (int i = 0; i < counts[rank]; i++) {
        local_sum += local_data[i] * local_data[i];
    }

    // ----------------------------------------
    // Combine partial sums
    // ----------------------------------------

    double global_sum = 0.0;

    MPI_Reduce(
        &local_sum,
        &global_sum,
        1,
        MPI_DOUBLE,
        MPI_SUM,
        0,
        MPI_COMM_WORLD
    );

    // ----------------------------------------
    // Measure maximum process execution time
    // ----------------------------------------

    double local_time = MPI_Wtime() - start;
    double max_time = 0.0;

    MPI_Reduce(
        &local_time,
        &max_time,
        1,
        MPI_DOUBLE,
        MPI_MAX,
        0,
        MPI_COMM_WORLD
    );

    // ----------------------------------------
    // Output
    // ----------------------------------------

    double average = global_sum / N;

    bool csv_mode =
        (argc > 2 && string(argv[2]) == "csv");

    if (rank == 0) {

        if (csv_mode) {

            cout << N << ","
                 << size << ","
                 << max_time << "\n";

        } else {

            cout << "=====================================\n";
            cout << " MPI Data Processing\n";
            cout << "=====================================\n";

            cout << "Dataset size    : " << N << "\n";
            cout << "Processes       : " << size << "\n";
            cout << "Sum of squares  : " << global_sum << "\n";
            cout << "Average square  : " << average << "\n";
            cout << "Execution time  : "
                 << max_time
                 << " seconds\n";
        }
    }

    MPI_Finalize();

    return 0;
}