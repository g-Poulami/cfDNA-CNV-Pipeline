#!/bin/bash

set -e

echo "Step 1: Simulating CNV data"
python scripts/simulate_cnv.py

echo "Step 2: Running ichorCNA"
Rscript scripts/runIchorCNA.R \
  --WIG data/synthetic.wig \
  --gcWig scripts/gc_final.wig \
  --mapWig scripts/map_hg38_1000kb.wig \
  --outDir results/sim \
  --id synthetic

echo "Complete!"
