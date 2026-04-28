#!/bin/bash
SAMPLE=$1
ICHOR_RESULTS="results/ichor/${SAMPLE}.params.txt"
CNV_CNS="results/cnvkit/${SAMPLE}.cns"

# 1. Extract Purity using Python bridge
TF=$(python3 scripts/extract_purity.py $ICHOR_RESULTS)
echo "Identified Tumor Fraction for $SAMPLE: $TF"

# 2. Refine CNVkit calls
# High Purity = high confidence. Low Purity = scaled thresholds.
cnvkit.py call $CNV_CNS --purity $TF --method clonal -o results/final/${SAMPLE}.refined.cns

# 3. Export Data for Portfolio
cnvkit.py genemetrics results/final/${SAMPLE}.refined.cns -o results/final/${SAMPLE}_genes.txt