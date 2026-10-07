#!/bin/bash

OUTPUT="results/mpi_raw.csv"

echo "dataset_size,processes,run,execution_time" > "$OUTPUT"

DATASETS=(1000000 10000000 50000000 100000000)
PROCESSES=(1 2 4 8)
RUNS=5

for N in "${DATASETS[@]}"
do
    for P in "${PROCESSES[@]}"
    do
        for R in $(seq 1 $RUNS)
        do
            RESULT=$(mpiexec -n "$P" ./mpi.exe "$N" csv)

            echo "$N,$P,$R,$(echo "$RESULT" | cut -d',' -f3)" >> "$OUTPUT"
        done
    done
done

echo "MPI experiments completed."
echo "Results saved to: $OUTPUT"