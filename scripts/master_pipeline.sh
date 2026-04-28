#!/bin/bash

# Configuration
SAMPLE_ID="Patient_Sample_01"
ICHOR_PARAMS="results/ichor/${SAMPLE_ID}.params.txt"
CNVKIT_SEGMENTS="results/cnvkit/${SAMPLE_ID}.cns"
CNVKIT_RATIOS="results/cnvkit/${SAMPLE_ID}.cnr"
OUTPUT_DIR="results/final"

echo "----------------------------------------------------"
echo "Processing Liquid Biopsy Sample: $SAMPLE_ID"
echo "----------------------------------------------------"

# 1. Extraction Phase
echo "[1/3] Extracting Tumor Fraction from ichorCNA..."
PURITY=$(python3 scripts/extract_purity.py "$ICHOR_PARAMS")
echo "Found Purity: $PURITY"

# 2. Refinement Phase
echo "[2/3] Running CNVkit Call with Purity Correction..."
cnvkit.py call "$CNVKIT_SEGMENTS" \
    --purity "$PURITY" \
    --method clonal \
    --ploidy 2 \
    -o "${OUTPUT_DIR}/${SAMPLE_ID}.refined.cns"

# 3. Reporting Phase
echo "[3/3] Generating Gene-Level Metrics..."
cnvkit.py genemetrics "${OUTPUT_DIR}/${SAMPLE_ID}.refined.cns" \
    -s "$CNVKIT_RATIOS" \
    -o "${OUTPUT_DIR}/${SAMPLE_ID}_gene_report.txt"

echo "DONE. Check ${OUTPUT_DIR} for refined results."
