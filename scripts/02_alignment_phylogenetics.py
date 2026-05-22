import subprocess
import os

# Step 1: Combine reference + all BDBV + other species for alignment
print("=== PREPARING ALIGNMENT DATASET ===")

combined = []
from Bio import SeqIO

# Add BDBV reference
for r in SeqIO.parse("genomes/bdbv_reference.fasta", "fasta"):
    r.id = "BDBV_REF"
    r.description = ""
    combined.append(r)

# Add 2007 outbreak genome
for r in SeqIO.parse("genomes/bdbv_all.fasta", "fasta"):
    if r.id == "FJ217161.1":
        r.id = "BDBV_2007_Uganda"
        r.description = ""
        combined.append(r)

# Add 2012 outbreak genomes
for r in SeqIO.parse("genomes/bdbv_all.fasta", "fasta"):
    if r.id in ["KC545393.1", "KC545394.1", "KC545395.1", "KC545396.1"]:
        r.id = r.id.replace(".1", "_2012_DRC")
        r.description = ""
        combined.append(r)

# Add other species
species_map = {
    "Zaire_EBOV": "genomes/Zaire_EBOV.fasta",
    "Sudan_SUDV": "genomes/Sudan_SUDV.fasta",
    "Reston_RESTV": "genomes/Reston_RESTV.fasta",
    "TaiForest_TAFV": "genomes/TaiForest_TAFV.fasta"
}
for name, f in species_map.items():
    for r in SeqIO.parse(f, "fasta"):
        r.id = name
        r.description = ""
        combined.append(r)

SeqIO.write(combined, "genomes/combined_for_alignment.fasta", "fasta")
print(f"Combined {len(combined)} sequences for alignment")

# Step 2: Run MAFFT alignment
print("\n=== RUNNING MAFFT ALIGNMENT ===")
result = subprocess.run(
    ["mafft", "--auto", "--thread", "4",
     "genomes/combined_for_alignment.fasta"],
    capture_output=True, text=True
)
with open("genomes/aligned.fasta", "w") as f:
    f.write(result.stdout)
print("Alignment complete! Saved to genomes/aligned.fasta")

# Step 3: Run IQ-TREE phylogenetics
print("\n=== RUNNING IQ-TREE PHYLOGENETICS ===")
os.makedirs("results/tree", exist_ok=True)
result = subprocess.run(
    ["iqtree", "-s", "genomes/aligned.fasta",
     "-m", "GTR+G",
     "-bb", "1000",
     "-pre", "results/tree/bdbv_tree",
     "-nt", "AUTO", "-redo"],
    capture_output=True, text=True
)
print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
if os.path.exists("results/tree/bdbv_tree.treefile"):
    print("\nPhylogenetic tree saved: results/tree/bdbv_tree.treefile")
else:
    print("Tree file not found, check errors")
    print(result.stderr[-300:])
