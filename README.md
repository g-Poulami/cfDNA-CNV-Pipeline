# cfDNA-CNV-Pipeline

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![BWA-MEM](https://img.shields.io/badge/Aligner-BWA--MEM-purple?style=flat-square)](http://bio-bwa.sourceforge.net/)
[![Picard](https://img.shields.io/badge/Tools-Picard-orange?style=flat-square)](https://broadinstitute.github.io/picard/)
[![CBS](https://img.shields.io/badge/Segmentation-CBS-teal?style=flat-square)](https://bioconductor.org/packages/DNAcopy/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

---

## Biological Question

Can copy number alterations shed from a tumour into the bloodstream be reliably detected from low-coverage whole-genome sequencing of plasma DNA — and what analytical challenges must be solved to make this clinically useful?

Tumours continuously shed DNA into the circulation through cell death and active secretion. This circulating tumour DNA (ctDNA), mixed with cell-free DNA (cfDNA) released by healthy cells, is recoverable from a standard blood draw and can be sequenced without any surgical intervention. The promise of this technology — liquid biopsy — is profound: a blood test capable of detecting cancer, monitoring treatment response, and identifying resistance mechanisms in real time, without the morbidity and sampling bias of repeat tissue biopsy.

Copy number variations (CNVs) — large-scale gains and losses of chromosomal segments — are among the most frequent and diagnostically informative alterations in cancer genomes. Amplification of oncogenes such as *ERBB2* (HER2), *MYC*, and *CCND1*, and deletion of tumour suppressors such as *TP53*, *RB1*, and *CDKN2A*, are defining features of many cancer subtypes and are directly linked to treatment eligibility, prognosis, and mechanisms of acquired resistance. Detecting these alterations from cfDNA rather than tissue is now a regulatory-approved approach in several clinical contexts, including *ERBB2* copy number assessment in breast cancer and *MET* amplification in NSCLC.

However, cfDNA presents a fundamentally different analytical problem from tissue-derived DNA. Tumour-derived fragments typically constitute only a small fraction of total cfDNA — often 1–10% in early-stage cancers, sometimes less — mixed with a large background of normal cell-derived DNA. The fragments themselves are short (median ~167 bp, reflecting nucleosomal organisation) and the sequencing is shallow (0.1–1× genome coverage) to keep clinical costs tractable. Together, these properties — low tumour fraction, high fragmentation, and sparse coverage — mean that the statistical and normalisation methods developed for high-coverage tumour tissue sequencing do not transfer directly to cfDNA data.

This pipeline addresses those challenges head-on: adapter trimming tuned for cfDNA fragment lengths, GC-bias correction adapted for shallow coverage, and circular binary segmentation (CBS) for statistically principled CNV breakpoint detection from binned read depth.

---

## Key Findings

> **cfDNA CNV analysis requires a dedicated analytical stack. Standard WGS CNV pipelines applied naively to plasma data produce artefact-dominated profiles; each stage of this pipeline addresses a specific source of technical noise.**

1. **Fragment length distribution is a primary quality indicator for cfDNA input.** Genuine cfDNA produces a characteristic fragment length peak at ~167 bp (mononucleosomal) with a secondary peak at ~340 bp (dinucleosomal). Deviation from this pattern — a broad distribution without a clear peak, or a peak shifted toward larger fragments — indicates degradation of the cfDNA input, contamination with high-molecular-weight genomic DNA from cell lysis, or a DNA extraction problem. The `fragment_length.png` output serves as the first quality gate before interpreting copy number results.

2. **GC bias correction is essential for shallow-coverage cfDNA data.** At low coverage, stochastic sampling variance and systematic GC-content-driven amplification efficiency differences produce artifactual coverage waves across the genome that can mimic chromosomal copy number changes. Without correction, high-GC regions (e.g., gene-dense chromosome arms) appear falsely amplified, and low-GC regions appear falsely deleted. The `gc_correction.png` diagnostic plot makes this correction visible and auditable.

3. **Fixed-size binning at 500 kb balances resolution against statistical power.** At 0.1–1× coverage, individual base positions and even kilobase-scale windows contain too few reads for reliable depth estimation. Aggregating reads into 500 kb bins provides a stable depth estimate (expected ~50–500 reads per bin at 0.1–1×) while preserving resolution sufficient to detect focal amplifications of individual oncogenes and broad arm-level gains and losses. Bin size is configurable for users working with higher-coverage data.

4. **Circular binary segmentation identifies CNV boundaries without requiring prior knowledge of breakpoint locations.** CBS treats the genome-wide log2 copy number ratio profile as a piecewise-constant signal and identifies changepoints using a permutation-based statistical test. This is a model-free approach: it makes no assumptions about the number or location of CNV segments, making it robust to the variable and patient-specific copy number landscapes seen across tumour types.

5. **The cfDNA-specific alignment strategy reduces systematic mapping artefacts.** BWA-MEM alignment parameters are tuned for the short, blunt-ended cfDNA fragments. Standard WGS alignment pipelines often apply minimum read length filters or insert-size-based quality filters that would disproportionately discard the shortest (and often most tumour-enriched) cfDNA fragments. Picard MarkDuplicates removes PCR amplification duplicates that are over-represented in cfDNA libraries due to the low input DNA quantities used in library preparation.

---

## Clinical Relevance

This pipeline connects directly to several active clinical and research priorities in liquid biopsy oncology:

**Early cancer detection.** Large-scale prospective studies (CCGA, GRAIL/Galleri, TRACERx) have demonstrated that plasma CNV profiles can detect tumour-derived signal before clinical symptoms in a range of cancer types. Establishing analytical pipelines that reliably extract this signal from low-coverage data is foundational infrastructure for early detection research.

**Treatment response monitoring and minimal residual disease.** Serial liquid biopsies during and after treatment can track tumour burden non-invasively. CNV changes — for example, amplification of the androgen receptor gene *AR* in castration-resistant prostate cancer, or *ERBB2* amplification emerging under HER2-targeted therapy — are clinically actionable indicators of treatment resistance that can appear in cfDNA before radiological progression.

**Paediatric oncology.** Repeat tissue biopsy is particularly difficult in paediatric patients, both technically and ethically. cfDNA CNV analysis is especially valuable in paediatric tumours with characteristic copy number landscapes: *MYCN* amplification in neuroblastoma, whole-chromosome gains in medulloblastoma, and segmental chromosomal aberrations in childhood leukaemia. Non-invasive monitoring via cfDNA reduces procedural burden in this population.

**CNV-driven treatment eligibility.** Several targeted therapies have companion diagnostic requirements based on copy number: *ERBB2* amplification for trastuzumab and pertuzumab in breast and gastric cancer, *MET* amplification for capmatinib and tepotinib in NSCLC, and *CDK4/6* amplification for emerging CDK inhibitor indications. A validated cfDNA CNV pipeline enables blood-based companion diagnostic testing as an alternative to tissue rebiopsy, particularly in patients with inaccessible tumours.

---

## Dataset

**User-provided cfDNA low-coverage whole-genome sequencing data**

| Property | Details |
|---|---|
| **Input format** | Paired-end FASTQ (Illumina) |
| **Reference genome** | GRCh38 / hg38 |
| **Recommended coverage** | 0.1–5× (pipeline optimised for lcWGS) |
| **Bin size (default)** | 500 kb (configurable) |
| **Expected fragment peak** | ~167 bp (mononucleosomal cfDNA) |
| **Duplication rate** | Typically 10–40% for cfDNA libraries; flagged by Picard |

> This pipeline does not ship with example data due to the patient-derived and clinically sensitive nature of cfDNA sequencing. Publicly available cfDNA WGS datasets include those deposited by the TRACERx consortium ([EGA: EGAS00001006254](https://ega-archive.org/studies/EGAS00001006254)) and CCGA study participants. Synthetic cfDNA datasets can be generated with tools such as [Sherman](https://www.bioinformatics.babraham.ac.uk/projects/sherman/) or [BAMSurgeon](https://github.com/adamewing/bamsurgeon) for pipeline testing.

### Data Files

| File | Description |
|---|---|
| `data/raw/{sample}_R1.fastq.gz` | Raw forward reads |
| `data/raw/{sample}_R2.fastq.gz` | Raw reverse reads |
| `ref/hg38.fa` | GRCh38 reference genome |
| `ref/hg38.fa.bwt` | BWA index (generated during setup) |
| `config.yaml` | Per-run sample configuration |

---

## Project Structure

```
cfDNA-CNV-Pipeline/
├── run_pipeline.py              # Main orchestration entry point
├── config.yaml                  # Per-sample input configuration
├── src/
│   ├── align.py                 # BWA-MEM alignment + Samtools sort/index wrapper
│   ├── bin_reads.py             # Fixed-window read depth binning
│   ├── gc_correct.py            # GC bias estimation and normalisation
│   ├── segment.py               # Circular binary segmentation (CBS)
│   └── visualise.py             # Genome-wide CNV profile and QC plots
├── data/
│   └── raw/                     # Input FASTQ files (not tracked in git)
├── ref/                         # Reference genome and BWA index (not tracked in git)
├── results/
│   ├── qc/                      # FastQC HTML reports + MultiQC aggregated report
│   ├── bam/                     # Sorted, deduplicated BAM + BAI index
│   ├── bins/                    # Per-bin read depth tables (TSV)
│   ├── cnv/                     # CBS segmented copy number calls (.seg)
│   └── plots/                   # CNV profile, fragment length, GC correction PNGs
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/g-Poulami/cfDNA-CNV-Pipeline.git
cd cfDNA-CNV-Pipeline
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install external tools

```bash
# Via conda (recommended for reproducibility)
conda install -c bioconda bwa samtools trimmomatic picard fastqc multiqc

# Or via apt (Ubuntu/Debian)
sudo apt-get install bwa samtools trimmomatic fastqc
pip install multiqc
# Picard: download from https://github.com/broadinstitute/picard/releases
```

### 4. Download and index the reference genome

```bash
mkdir -p ref
cd ref
wget https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
gunzip hg38.fa.gz

# Build BWA index (required before alignment)
bwa index hg38.fa

# Build FAI index (required for depth binning)
samtools faidx hg38.fa
```

### 5. Verify tool versions

```bash
bwa 2>&1 | head -3               # Expect >= 0.7.17
samtools --version | head -1     # Expect >= 1.15
trimmomatic -version             # Expect >= 0.39
picard MarkDuplicates --version  # Expect >= 2.27
fastqc --version                 # Expect >= 0.11
multiqc --version                # Expect >= 1.14
```

---

## Pipeline

### Step 1 — Raw Quality Control (`FastQC`)

Runs FastQC on each input FASTQ file to assess base quality scores, per-base GC content, sequence duplication levels, adapter content, and — critically for cfDNA — the fragment length distribution. The fragment length histogram at this stage reflects the insert size distribution of the cfDNA library and should show a mononucleosomal peak at ~167 bp. A clean peak confirms that the input is genuine cfDNA; a flat or bimodal distribution may indicate genomic DNA contamination or degradation.

**Output:** `results/qc/{sample}_R{1,2}_fastqc.html`

### Step 2 — Adapter Trimming (`Trimmomatic`)

Removes Illumina adapter sequences and trims low-quality bases from read ends. For cfDNA, adapter trimming is especially important: because cfDNA fragments are short, a substantial fraction of reads extend through the insert into the adapter on the opposite end. Untrimmed adapter sequence at read ends causes misalignment or soft-clipping, reducing the effective mapping rate and biasing fragment length estimates. Trimmomatic is run in paired-end mode with sliding-window quality trimming (window size 4, minimum average quality 20) and a minimum post-trimming read length of 36 bp.

**Output:** `data/trimmed/{sample}_R{1,2}_trimmed.fastq.gz`

### Step 3 — Post-trimming QC (`FastQC`)

Re-runs FastQC after trimming to confirm that adapter content has been removed and quality score distributions have improved. The updated fragment length histogram reflects the trimmed insert sizes and should retain the mononucleosomal peak.

**Output:** `results/qc/{sample}_R{1,2}_trimmed_fastqc.html`

### Step 4 — Alignment (`BWA-MEM`)

Maps trimmed reads to GRCh38 using BWA-MEM, the standard short-read aligner for Illumina data. Read group tags (`@RG`) are added at this stage to record sample identity, library, and platform — required by downstream tools including Picard. BWA-MEM handles the short, blunt-ended fragments characteristic of cfDNA more accurately than gapped aligners designed for longer reads, maintaining a high mapping rate across the fragment length distribution.

**Output:** `results/bam/{sample}.bam`

### Step 5 — Sorting and Indexing (`Samtools`)

Coordinate-sorts the output BAM file and builds a BAI index. Coordinate-sorted BAMs are required for Picard MarkDuplicates and for the read depth binning step, as positional access patterns are far more efficient on sorted data.

**Output:** `results/bam/{sample}.sorted.bam`, `results/bam/{sample}.sorted.bam.bai`

### Step 6 — Duplicate Removal (`Picard MarkDuplicates`)

Identifies and flags PCR duplicates — reads with identical start and end positions arising from amplification of the same original molecule during library preparation. In cfDNA library preparation, low input DNA quantity (typically 1–10 ng from plasma) requires extensive PCR amplification, resulting in higher duplication rates (10–40%) than typical tissue-derived WGS. Failing to remove duplicates inflates apparent read depth at specific positions, biasing bin depth estimates and producing false CNV signals. Marked duplicates are excluded from downstream depth calculations.

**Output:** `results/bam/{sample}.dedup.bam`, `results/qc/{sample}.duplicate_metrics.txt`

### Step 7 — Read Depth Binning (`src/bin_reads.py`)

Partitions the genome into fixed-size non-overlapping windows (default: 500 kb) and counts the number of deduplicated reads mapping to each bin. Bins overlapping centromeres, telomeres, segmental duplications, and other problematic regions (ENCODE blacklist) are excluded. The resulting per-bin read depth table is the input to GC correction and segmentation. The choice of bin size represents a resolution-versus-power trade-off: smaller bins provide finer spatial resolution but require higher coverage for stable depth estimates.

**Output:** `results/bins/{sample}_binned_depth.tsv`

### Step 8 — GC Bias Correction (`src/gc_correct.py`)

Normalises per-bin read depth for GC content bias using a locally weighted regression (LOESS) approach. For each bin, the GC content of the reference sequence is computed; bins are then grouped by GC decile and a smoothed correction factor is estimated from the relationship between GC content and observed depth across the genome. This correction factor is applied multiplicatively to produce a GC-normalised depth profile. The `gc_correction.png` diagnostic plot shows the raw and corrected depth-vs-GC scatter to confirm that the bias has been removed.

**Output:** `results/bins/{sample}_gc_corrected.tsv`, `results/plots/gc_correction.png`

### Step 9 — CNV Segmentation (`src/segment.py`)

Applies Circular Binary Segmentation (CBS) to the GC-corrected log2 read depth ratio profile (observed depth / median genome-wide depth). CBS recursively identifies statistically significant changepoints in the depth signal using a permutation test, producing a set of segments — contiguous genomic intervals with a constant estimated copy number ratio. Segments with log2 ratio > +0.3 are called as gains; segments with log2 ratio < −0.3 are called as losses (thresholds configurable). The output `.seg` file follows the standard CBS segment format compatible with tools such as IGV, GISTIC2, and cBioPortal.

**Output:** `results/cnv/{sample}.cnv.seg`

### Step 10 — Visualisation (`src/visualise.py`)

Generates three diagnostic plots: (1) a genome-wide CNV scatter plot with CBS segment lines overlaid, coloured by gain/loss status; (2) the cfDNA fragment length distribution histogram; and (3) the GC correction diagnostic. The genome-wide profile plot uses a chromosome-ordered x-axis with alternating shading, log2 ratio on the y-axis, and horizontal lines at the gain and loss thresholds.

**Output:** `results/plots/cnv_profile.png`, `results/plots/fragment_length.png`, `results/plots/gc_correction.png`

### Step 11 — Aggregated QC (`MultiQC`)

Collects QC metrics from FastQC (pre- and post-trim), Picard MarkDuplicates, and Samtools flagstat into a single interactive HTML report. Key metrics to review: mapping rate (expect > 90% for good cfDNA), duplication rate (10–40% typical), median insert size (expect ~167 bp peak), and per-base quality scores.

**Output:** `results/qc/multiqc_report.html`

---

## Configuration

Edit `config.yaml` before each run:

```yaml
sample_id: SAMPLE_001
reads_dir: data/raw/
r1: SAMPLE_001_R1.fastq.gz
r2: SAMPLE_001_R2.fastq.gz
genome: ref/hg38.fa
bin_size: 500000        # 500 kb bins (reduce to 100000 for >1x coverage)
gc_correction: true
blacklist: ref/hg38-blacklist.v2.bed   # ENCODE blacklist (recommended)
gain_threshold: 0.3     # log2 ratio above which a segment is called a gain
loss_threshold: -0.3    # log2 ratio below which a segment is called a loss
outdir: results/
```

### Running the Pipeline

```bash
# Standard run
python run_pipeline.py --config config.yaml

# Specify number of threads for BWA alignment
python run_pipeline.py --config config.yaml --threads 8

# Skip QC steps (for re-running segmentation only)
python run_pipeline.py --config config.yaml --skip-qc
```

---

## Outputs

| File | Description |
|---|---|
| `results/cnv/{sample}.cnv.seg` | CBS-segmented copy number calls: chromosome, start, end, n_bins, log2 ratio |
| `results/plots/cnv_profile.png` | Genome-wide scatter plot with CBS segment lines; gains in red, losses in blue |
| `results/plots/fragment_length.png` | cfDNA insert size histogram; expected mononucleosomal peak at ~167 bp |
| `results/plots/gc_correction.png` | Pre/post GC normalisation diagnostic; depth vs GC content scatter |
| `results/bins/{sample}_gc_corrected.tsv` | GC-corrected per-bin depth table (input to segmentation) |
| `results/bam/{sample}.dedup.bam` | Sorted, deduplicated BAM; the authoritative alignment file for the run |
| `results/qc/multiqc_report.html` | Aggregated QC report across all pipeline steps |

---

## Plots

### Genome-Wide CNV Profile

![CNV Profile](results/plots/cnv_profile.png)

Each point in this scatter plot represents one 500 kb genomic bin, positioned by its chromosomal coordinate on the x-axis and its GC-corrected log2 read depth ratio on the y-axis. Chromosomes are ordered from 1 to 22 followed by X and Y, with alternating background shading to distinguish adjacent chromosomes. Overlaid horizontal segment lines show the CBS output: the algorithm fits a piecewise-constant function through the noisy per-bin depth signal, and each flat plateau represents a genomic interval estimated to be at a uniform copy number state. Segments coloured red sit above the gain threshold (log2 ratio > +0.3); segments coloured blue sit below the loss threshold (log2 ratio < −0.3); segments at the diploid baseline are shown in grey.

**Biological interpretation:** Broad plateaus spanning entire chromosome arms reflect arm-level copy number events — whole-arm gains and losses that arise from chromosome missegregation during mitosis and are common in advanced solid tumours. Narrow elevated segments confined to a sub-chromosomal region indicate focal amplifications, which often harbour oncogenes under positive selection: examples include *ERBB2* at 17q12, *MYC* at 8q24, and *CCND1* at 11q13. Focal deletions that are narrow and deep are often consistent with tumour suppressor loss: *RB1* at 13q14, *CDKN2A* at 9p21, and *TP53* at 17p13.

**cfDNA-specific note:** Log2 ratio amplitudes are attenuated by tumour fraction. A tumour sample with 5% ctDNA and a true heterozygous deletion (one copy) will produce a log2 ratio of approximately −0.035, far shallower than the −1.0 expected from tumour tissue. Visually flat profiles do not necessarily indicate the absence of CNVs; they may reflect a low tumour fraction below the detection threshold of this pipeline. Interpreting absolute copy number from cfDNA requires tumour fraction estimation (see ichorCNA in Future Work).

---

### cfDNA Fragment Length Distribution

![Fragment Length Distribution](results/plots/fragment_length.png)

This histogram plots the frequency of sequenced fragment insert sizes, binned in 10 bp increments from ~50 bp to ~500 bp. The x-axis is insert size in base pairs; the y-axis is the count or proportion of read pairs at each size. A dashed vertical line marks the expected mononucleosomal peak position at 167 bp.

**Biological interpretation:** Cell-free DNA is not randomly fragmented — it is released from nucleosomes as the chromatin of dying cells is degraded. Nucleosomes protect ~147 bp of DNA from nuclease digestion, leaving a linker region of ~20 bp between them. This nucleosomal architecture produces the characteristic cfDNA fragment length ladder: a dominant mononucleosomal peak at ~167 bp (147 bp nucleosomal DNA + ~20 bp linker), a secondary dinucleosomal peak at ~340 bp, and a tertiary peak at ~510 bp. The sharpness and height of the 167 bp peak relative to background is a direct indicator of cfDNA input quality. A clean, narrow mononucleosomal peak indicates high-quality plasma-derived cfDNA with intact nucleosomal structure.

**Quality interpretation:** Deviation from this expected pattern is diagnostically important and should be investigated before interpreting copy number results. A broad flat distribution without a defined peak indicates degradation of the cfDNA sample — likely caused by freeze-thaw cycles, delayed plasma processing, or insufficient input. A peak shifted toward larger fragment sizes (> 200 bp) suggests contamination with high-molecular-weight genomic DNA released by cell lysis during blood processing — a common pre-analytical artefact when plasma separation is delayed. Conversely, a peak shifted toward very short fragments (< 140 bp) can indicate active nuclease activity in the sample or certain disease states. Tumour-derived cfDNA fragments have been reported to be modestly shorter on average than normal cell-derived cfDNA, creating a subtle enrichment of sub-nucleosomal fragments in high-tumour-fraction samples.

---

### GC Bias Correction Diagnostic

![GC Correction](results/plots/gc_correction.png)

This diagnostic plot contains two panels displayed side by side. The left panel shows the relationship between per-bin GC content (x-axis, expressed as a fraction from 0 to 1) and per-bin read depth (y-axis, normalised to the genome-wide median) before GC correction. The right panel shows the same scatter after LOESS correction has been applied. An overlaid smoothing curve in each panel visualises the trend being corrected. In the left panel, the curve typically follows an inverted U-shape: depth is low at very low GC content (< 0.35), rises to a maximum around 0.45–0.55 GC, and falls again at high GC content (> 0.65), reflecting the amplification efficiency bias of PCR and the sequencing chemistry.

**Biological interpretation:** GC bias is a systematic technical artefact introduced at two stages of library preparation: PCR amplification (high-GC regions amplify less efficiently, reducing their representation in the final library) and cluster generation on the flow cell (GC-rich sequences have suboptimal denaturation kinetics). In cfDNA libraries, where extensive PCR amplification is applied to low-input material, GC bias is more pronounced than in standard high-input WGS. If uncorrected, high-GC chromosome arms (e.g., chromosomes 19 and 22, which are gene-dense and GC-rich) appear falsely under-covered and are called as losses, while low-GC regions appear falsely elevated. After successful correction, the right panel should show a flat trend line at depth = 1.0 across the full GC range, with no systematic relationship between GC content and depth.

**Interpreting a failed correction:** If the right panel still shows a residual curve — particularly a persistent depression at extreme GC values (< 0.30 or > 0.70) — the LOESS correction has not fully captured the bias at the tails of the GC distribution. This can occur with very shallow coverage (< 0.1×), where bins at extreme GC values contain too few reads to estimate a reliable correction factor. In such cases, increasing bin size or applying a more robust correction method (e.g., the GC wave correction implemented in QDNAseq) is recommended before interpreting copy number results.

---

## Limitations

- **No tumour fraction estimation.** CNV log2 ratios from cfDNA are diluted by the fraction of normal DNA in the plasma. Without an estimate of the ctDNA fraction, absolute copy number cannot be inferred from segment ratios. Integration with ichorCNA or ASCAT-cfDNA would address this.
- **No matched normal.** The pipeline normalises against the genome-wide median of the same sample (tumour-only mode). A matched buffy coat (germline) sample from the same patient would enable subtraction of germline copy number polymorphisms and improve tumour-specific CNV detection. The pipeline architecture supports paired-mode extension.
- **CBS segmentation does not model tumour heterogeneity.** CBS fits a single copy number state per segment and does not account for subclonal CNVs present in only a fraction of tumour cells. Subclonal events produce intermediate log2 ratios that may not reach the calling threshold, particularly at low tumour fraction.
- **Bin size limits focal event resolution.** 500 kb bins cannot resolve amplifications spanning single genes or exons. For applications requiring focal amplification detection (e.g., *ERBB2* amplification within chromosome 17q12), smaller bins and higher coverage data are required.
- **Fragment length analysis is descriptive, not corrective.** The fragment length histogram is a QC metric but the pipeline does not perform fragment-length-informed read weighting (as implemented in Griffin or DELFI). Incorporating nucleosomal positioning signals from fragment length patterns would add an orthogonal layer of tumour signal detection.
- **Single-sample per run.** The current implementation processes one sample per config file. Batch processing and sample-level comparisons (e.g., longitudinal monitoring across serial timepoints) require manual iteration or a wrapper script.

---

## Future Work

- [ ] **ichorCNA integration** — add ctDNA fraction estimation and absolute copy number conversion to the segmentation step
- [ ] **Matched normal mode** — implement paired tumour-cfDNA / buffy coat subtraction to remove germline copy number polymorphisms
- [ ] **Snakemake workflow** — replace the Python orchestrator with a Snakemake Snakefile for dependency-aware parallel execution across sample batches
- [ ] **Focal amplification annotation** — annotate called segments against a curated list of clinically actionable oncogene and tumour suppressor coordinates
- [ ] **Fragment length-informed analysis** — integrate Griffin-style nucleosomal fragment length profiling as an orthogonal tumour signal layer
- [ ] **Longitudinal tracking module** — add a sample-series comparison mode to visualise copy number dynamics across serial cfDNA timepoints from the same patient
- [ ] **ENCODE blacklist integration** — make blacklist-based bin exclusion a default step with the hg38 v2 blacklist bundled in the repository
- [ ] **Subclonal CNV detection** — explore mixture model segmentation (e.g., HMM-based) to detect heterogeneous copy number states within segments

---

## Connections to Broader Research

This pipeline is part of a broader computational investigation of cancer genomics across molecular scales:

- **[Breast-Cancer-Survival-Risk-Model](https://github.com/g-Poulami/Breast-Cancer-Survival-Risk-Model):** Builds Cox proportional hazards survival models on the METABRIC cohort, where copy number-driven gene expression changes — HER2 amplification, MYC amplification, RB1 deletion — are key drivers of the molecular subtype differences that stratify patient survival. cfDNA CNV detection is the non-invasive clinical application of the same copy number biology characterised in tissue.
- **[GenEquityFlow](https://github.com/g-Poulami/GenEquityFlow):** Addresses whether cancer biomarkers generalise across ancestral populations. CNV-based companion diagnostics (e.g., ERBB2 amplification testing) inherit the same equity concerns: if the reference allele frequencies and copy number polymorphism catalogs used to filter germline background CNVs are European-majority, they may produce false positive somatic calls in patients of non-European ancestry.
- **[Germline-Variant-QC-BRCA](https://github.com/g-Poulami/Germline-Variant-QC-BRCA):** Provides the germline QC infrastructure needed to distinguish somatic tumour-derived copy number changes from inherited germline copy number polymorphisms — a critical distinction in cfDNA analysis where both signals are present in the same plasma DNA sample.

---

## References

1. Adalsteinsson V.A. et al. Scalable whole-exome sequencing of cell-free DNA reveals high concordance with metastatic tumour biopsies. *Nature Communications*, 8, 1324 (2017).
2. Diehl F. et al. Circulating mutant DNA to assess tumor dynamics. *Nature Medicine*, 14(9), 985–990 (2008).
3. Olshen A.B. et al. Circular binary segmentation for the analysis of array-based DNA copy number data. *Biostatistics*, 5(4), 557–572 (2004).
4. Benjamini Y. & Speed T.P. Summarizing and correcting the GC content bias in high-throughput sequencing. *Nucleic Acids Research*, 40(10), e72 (2012).
5. Snyder M.W. et al. Cell-free DNA comprises an in vivo nucleosome footprint that informs its tissues-of-origin. *Cell*, 164(1–2), 57–68 (2016).
6. Bolger A.M., Lohse M. & Usadel B. Trimmomatic: a flexible trimmer for Illumina sequence data. *Bioinformatics*, 30(15), 2114–2120 (2014).
7. Li H. & Durbin R. Fast and accurate short read alignment with Burrows-Wheeler Aligner. *Bioinformatics*, 25(14), 1754–1760 (2009).
8. Danecek P. et al. Twelve years of SAMtools and BCFtools. *GigaScience*, 10(2), giab008 (2021).
9. Cristiano S. et al. Genome-wide cell-free DNA fragmentation in patients with cancer. *Nature*, 570, 385–389 (2019).
10. Wan J.C.M. et al. Liquid biopsies come of age: towards implementation of circulating tumour DNA. *Nature Reviews Cancer*, 17(4), 223–238 (2017).

---

## Author

**Poulami Ghosh** — [@g-Poulami](https://github.com/g-Poulami)  
[LinkedIn](https://linkedin.com/in/poulami-ghosh-879439304) · [Google Scholar](https://scholar.google.com/scholar?q=Poulami+Ghosh) · poulamighosh738@gmail.com

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
