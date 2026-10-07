#!/bin/bash

# ==========================================
# OpenMP Experiment Runner
# ==========================================

OUTPUT="results/openmp_raw.csv"

# Create results directory if it doesn't exist
mkdir -p results

# CSV header
echo "dataset_size,threads,run,execution_time" > "$OUTPUT"

# Dataset sizes
DATASETS=(1000000 10000000 50000000 100000000)

# Thread counts
THREADS=(1 2 4 8 12)

# Number of repetitions
RUNS=5

echo "Starting OpenMP experiments..."
echo

for N in "${DATASETS[@]}"
do

    for T in "${THREADS[@]}"
    do

        echo "Dataset: $N | Threads: $T"

        export OMP_NUM_THREADS=$T

        for ((R=1; R<=RUNS; R++))
        do

            RESULT=$(./openmp.exe "$N" csv)

            TIME=$(echo "$RESULT" | cut -d',' -f3)

            echo "$N,$T,$R,$TIME" >> "$OUTPUT"

            echo "  Run $R: $TIME seconds"

        done

    done

done

echo
echo "=========================================="
echo "Experiment completed!"
echo "Results saved to:"
echo "$OUTPUT"
echo "=========================================="