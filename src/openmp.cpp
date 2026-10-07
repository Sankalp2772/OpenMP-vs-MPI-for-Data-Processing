#include <iostream>
#include <vector>
#include <chrono>
#include <cstdlib>
#include <omp.h>
#include <string>

using namespace std;
using namespace chrono;

int main(int argc, char* argv[]) {

    // Default dataset size
    long long N = 10000000;

    // Read dataset size from command line
    if (argc > 1) {
        N = atoll(argv[1]);
    }

    // Create dataset
    vector<double> data(N);

    // Generate dataset
    for (long long i = 0; i < N; i++) {
        data[i] = (i % 100) + 1;
    }

    // Start timer
    auto start = high_resolution_clock::now();

    // OpenMP parallel computation
    double sum = 0.0;
    int actual_threads = 1;

    #pragma omp parallel
    {
        #pragma omp single
        {
            actual_threads = omp_get_num_threads();
        }

        #pragma omp for reduction(+:sum)
        for (long long i = 0; i < N; i++) {
            sum += data[i] * data[i];
        }
    }

    // Calculate average
    double average = sum / N;

    // Stop timer
    auto end = high_resolution_clock::now();

    duration<double> elapsed = end - start;

    // Display results
    // Check whether CSV output is requested
bool csv_mode = (argc > 2 && string(argv[2]) == "csv");

if (csv_mode) {

    // CSV format:
    // dataset_size,threads,execution_time
    cout << N << ","
         << actual_threads << ","
         << elapsed.count() << "\n";

} else {

    cout << "=====================================\n";
    cout << " OpenMP Data Processing\n";
    cout << "=====================================\n";

    cout << "Dataset size    : " << N << "\n";
    cout << "Threads         : " << actual_threads << "\n";
    cout << "Sum of squares  : " << sum << "\n";
    cout << "Average square  : " << average << "\n";
    cout << "Execution time  : " << elapsed.count()
         << " seconds\n";
}
    return 0;
}