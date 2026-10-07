#!/bin/bash

OUTPUT="results/sequential_raw.csv"

mkdir -p results

echo "dataset_size,run,execution_time" > "$OUTPUT"

DATASETS=(1000000 10000000 50000000 100000000)

RUNS=5

echo "Starting Sequential experiments..."
echo

for N in "${DATASETS[@]}"
do
    echo "Dataset: $N"

    for ((R=1; R<=RUNS; R++))
    do
        RESULT=$(./sequential.exe "$N" csv)

        TIME=$(echo "$RESULT" | cut -d',' -f2)

        echo "$N,$R,$TIME" >> "$OUTPUT"

        echo "  Run $R: $TIME seconds"
    done
done

echo
echo "=========================================="
echo "Sequential experiment completed!"
echo "Results saved to:"
echo "$OUTPUT"
echo "=========================================="