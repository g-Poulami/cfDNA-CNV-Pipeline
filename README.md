# cfDNA Copy Number Analysis Project
## Multi-Tool Integration: ichorCNA + CNVkit

### Overview
This project addresses the "signal dilution" problem in cell-free DNA (cfDNA). In liquid biopsies, tumor DNA is often mixed with high amounts of healthy DNA. 

By using **ichorCNA** to estimate the Tumor Fraction (Purity) and **CNVkit** to call the segments, we can "correct" the log2 ratios to find absolute copy number changes.

### Components
- `scripts/extract_purity.py`: Parses ichorCNA parameters.
- `scripts/master_pipeline.sh`: Automates the handover between tools.
- `data/`: Place your .bam or .wig files here.

### Mathematical Logic
The script adjusts the observed log2 ratio ($R$) using the purity ($P$) from ichorCNA:
$$R_{corrected} = \log_2\left(\frac{2^R - (1-P)}{P}\right)$$

### Quick Start
1. Place your ichorCNA `.params.txt` in `results/ichor/`.
2. Place your CNVkit `.cns` files in `results/cnvkit/`.
3. Run: `bash scripts/master_pipeline.sh`
