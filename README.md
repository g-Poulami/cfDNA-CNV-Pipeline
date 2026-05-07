# cfDNA-CNV-Pipeline

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

A specialised bioinformatics workflow for detecting **Copy Number Variations (CNVs)** from **cell-free DNA (cfDNA)** sequencing data, designed to support non-invasive liquid biopsy research in oncology.

---

## Overview

Cell-free DNA circulating in blood plasma carries fragmented tumour-derived material that can be captured via low-coverage whole-genome sequencing (lcWGS). Unlike tissue biopsy, liquid biopsy is minimally invasive and can reflect real-time tumour dynamics, making cfDNA CNV analysis a critical tool for cancer detection, monitoring, and treatment response.

This pipeline addresses the key challenges of cfDNA data — low tumour fraction, high fragmentation, and shallow coverage — by applying normalisation and binning strategies adapted for plasma-derived input.

---

## Pipeline Overview

```
Raw cfDNA FASTQ
      |
      v
FastQC (raw QC)           -- assess read quality, fragment length distribution
      |
      v
Trimmomatic               -- adapter removal, quality trimming
      |
      v
FastQC (post-trim QC)     -- confirm trimming
      |
      v
BWA MEM alignment         -- map to reference genome (hg38)
      |
      v
SAMtools sort & index      -- coordinate-sorted BAM
      |
      v
Picard MarkDuplicates      -- PCR duplicate removal
      |
      v
Read depth binning         -- genome partitioned into fixed-size windows
      |
      v
GC correction              -- normalise coverage for GC-content bias
      |
      v
CNV segmentation           -- circular binary segmentation (CBS)
      |
      v
CNV visualisation          -- genome-wide copy number profile plots
      |
      v
MultiQC report             -- aggregated QC summary
```

---

## Key Features

- **cfDNA-optimised alignment**: tuned for short, highly fragmented reads characteristic of plasma-derived DNA
- **GC bias correction**: normalises binned read depth to account for GC-content-driven coverage artefacts, a critical step for shallow-coverage cfDNA data
- **Circular binary segmentation**: statistically principled breakpoint detection for reliable CNV calling
- **Fragment length analysis**: reports fragment size distributions as an orthogonal quality indicator of cfDNA input integrity
- **Reproducible outputs**: all intermediate files and final CNV profiles versioned and traceable

---

## Requirements

```bash
# Core dependencies
bwa >= 0.7.17
samtools >= 1.15
trimmomatic >= 0.39
picard >= 2.27
fastqc >= 0.11
multiqc >= 1.14

# Python packages
pip install numpy pandas matplotlib scipy
```

---

## Installation

```bash
git clone https://github.com/g-Poulami/cfDNA-CNV-Pipeline.git
cd cfDNA-CNV-Pipeline
pip install -r requirements.txt
```

---

## Usage

### 1. Configure input paths

Edit `config.yaml`:

```yaml
sample_id: SAMPLE_001
reads_dir: data/raw/
r1: SAMPLE_001_R1.fastq.gz
r2: SAMPLE_001_R2.fastq.gz
genome: ref/hg38.fa
bin_size: 500000     # 500 kb bins for lcWGS
gc_correction: true
outdir: results/
```

### 2. Run the pipeline

```bash
python run_pipeline.py --config config.yaml
```

### 3. Review outputs

```
results/
├── qc/             # FastQC and MultiQC reports
├── bam/            # Sorted, deduplicated BAM files
├── bins/           # Per-bin read depth tables
├── cnv/            # Segmented CNV calls (.seg files)
└── plots/          # Genome-wide CNV profile visualisations
```

---

## Outputs

| File | Description |
|------|-------------|
| `*.cnv.seg` | Segmented copy number calls with chromosome, start, end, and log2 ratio |
| `cnv_profile.png` | Genome-wide copy number scatter plot with segment lines |
| `fragment_length.png` | cfDNA fragment length distribution (expected peak ~167 bp) |
| `gc_correction.png` | Before/after GC normalisation diagnostic plot |
| `multiqc_report.html` | Aggregated QC metrics across all pipeline steps |

---

## Biological Context

cfDNA CNV analysis is particularly relevant for:

- **Early cancer detection**: tumour-derived CNVs in plasma may be detectable before clinical symptoms
- **Treatment monitoring**: tracking copy number changes over treatment cycles
- **Minimal residual disease**: detecting residual tumour signal post-treatment
- **Paediatric oncology**: enabling non-invasive monitoring where repeat tissue biopsy is impractical

---

## Project Structure

```
cfDNA-CNV-Pipeline/
├── run_pipeline.py          # Main entry point
├── config.yaml              # Input configuration
├── src/
│   ├── align.py             # BWA alignment wrapper
│   ├── bin_reads.py         # Read depth binning
│   ├── gc_correct.py        # GC bias correction
│   ├── segment.py           # CBS segmentation
│   └── visualise.py         # CNV profile plotting
├── data/
│   └── raw/                 # Input FASTQ files (not tracked)
├── ref/                     # Reference genome (not tracked)
├── results/                 # Pipeline outputs
└── requirements.txt
```

---

## License

MIT License

---

## Author

Poulami Ghosh — [LinkedIn](https://linkedin.com/in/poulami-ghosh-879439304) | [Google Scholar](https://scholar.google.com)
