import sys

def sync(tumour_path, ref_path, out_path):
    with open(tumour_path) as f:
        tumour_lines = f.readlines()
    with open(ref_path) as f:
        ref_lines = f.readlines()
    
    # Keep only lines from ref that exist in tumour
    tumour_headers = {line for line in tumour_lines if line.startswith("fixedStep")}
    synced = []
    # We match by line index for fixedStep WIGs of the same resolution
    for i in range(min(len(tumour_lines), len(ref_lines))):
        if tumour_lines[i].startswith("fixedStep"):
            synced.append(tumour_lines[i])
        else:
            synced.append(ref_lines[i])
            
    with open(out_path, "w") as f:
        f.writelines(synced)

sync("data/tumour_final.wig", "data/gc_hg38_1000kb.wig", "data/gc_synced.wig")
sync("data/tumour_final.wig", "data/map_hg38_1000kb.wig", "data/map_synced.wig")
