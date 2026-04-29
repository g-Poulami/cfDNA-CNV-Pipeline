import numpy as np

chrom_bins = {
    "chr1": 249, "chr2": 243, "chr3": 198, "chr4": 191,
    "chr5": 181, "chr6": 171, "chr7": 159, "chr8": 146,
    "chr9": 141, "chr10": 136, "chr11": 135, "chr12": 134,
    "chr13": 115, "chr14": 107, "chr15": 102, "chr16": 90,
    "chr17": 83, "chr18": 80, "chr19": 59, "chr20": 63,
    "chr21": 48, "chr22": 51, "chrX": 155
}

tumour_fraction = 0.3

out = open("data/synthetic.wig", "w")

for chrom, n_bins in chrom_bins.items():

    out.write(f"fixedStep chrom={chrom} start=1 step=1000000 span=1000000\n")

    cn = np.ones(n_bins) * 2

    if chrom == "chr8":
        cn[20:80] = 3
    if chrom == "chr17":
        cn[10:40] = 1

    obs_cn = (1 - tumour_fraction) * 2 + tumour_fraction * cn
    reads = np.random.poisson(obs_cn * 20)

    for r in reads[:n_bins]:
        out.write(f"{int(r)}\n")

out.close()
print("Synthetic CNV generated → data/synthetic.wig")
