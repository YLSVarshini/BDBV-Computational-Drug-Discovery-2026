from Bio import SeqIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

records = list(SeqIO.parse("genomes/bdbv_all.fasta", "fasta"))
print("=== GC CONTENT ANALYSIS ===")
gc_data = []
for r in records:
    seq = str(r.seq).upper()
    gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
    gc_data.append((r.id, len(r.seq), round(gc, 2)))
    print(f"{r.id}: {len(r.seq)} bp | GC: {round(gc,2)}%")

print("\n=== INTER-SPECIES GC COMPARISON ===")
species_files = {
    "BDBV": "genomes/bdbv_reference.fasta",
    "Zaire EBOV": "genomes/Zaire_EBOV.fasta",
    "Sudan SUDV": "genomes/Sudan_SUDV.fasta",
    "Reston RESTV": "genomes/Reston_RESTV.fasta",
    "TaiForest TAFV": "genomes/TaiForest_TAFV.fasta"
}
species_gc = {}
for sp, f in species_files.items():
    rec = list(SeqIO.parse(f, "fasta"))[0]
    seq = str(rec.seq).upper()
    gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
    species_gc[sp] = round(gc, 2)
    print(f"{sp}: {len(rec.seq)} bp | GC: {round(gc,2)}%")

lengths = [len(r.seq) for r in records]
ids = [r.id for r in records]
gc_values = [x[2] for x in gc_data]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Bundibugyo Ebolavirus (BDBV) Genomic Analysis', fontsize=14, fontweight='bold')

axes[0,0].barh(range(len(ids)), lengths, color='steelblue', alpha=0.8)
axes[0,0].set_yticks(range(len(ids)))
axes[0,0].set_yticklabels([i.split('.')[0] for i in ids], fontsize=7)
axes[0,0].set_xlabel('Genome Length (bp)')
axes[0,0].set_title('BDBV Genome Lengths')
axes[0,0].axvline(x=18940, color='red', linestyle='--', label='Reference (18,940 bp)')
axes[0,0].legend(fontsize=8)

axes[0,1].bar(range(len(ids)), gc_values, color='forestgreen', alpha=0.8)
axes[0,1].set_xticks(range(len(ids)))
axes[0,1].set_xticklabels([i.split('.')[0] for i in ids], rotation=90, fontsize=6)
axes[0,1].set_ylabel('GC Content (%)')
axes[0,1].set_title('GC Content Across BDBV Genomes')
axes[0,1].set_ylim(39, 43)

sp_names = list(species_gc.keys())
sp_gc = list(species_gc.values())
colors = ['red' if s == 'BDBV' else 'steelblue' for s in sp_names]
axes[1,0].bar(sp_names, sp_gc, color=colors, alpha=0.8)
axes[1,0].set_ylabel('GC Content (%)')
axes[1,0].set_title('GC Content: BDBV vs Other Ebolaviruses')
axes[1,0].tick_params(axis='x', rotation=20)
for i, v in enumerate(sp_gc):
    axes[1,0].text(i, v + 0.05, str(v), ha='center', fontsize=9)

sp_lengths = []
for sp, f in species_files.items():
    rec = list(SeqIO.parse(f, "fasta"))[0]
    sp_lengths.append(len(rec.seq))
axes[1,1].bar(sp_names, sp_lengths, color=colors, alpha=0.8)
axes[1,1].set_ylabel('Genome Length (bp)')
axes[1,1].set_title('Genome Length: BDBV vs Other Ebolaviruses')
axes[1,1].tick_params(axis='x', rotation=20)
axes[1,1].set_ylim(18000, 19200)
for i, v in enumerate(sp_lengths):
    axes[1,1].text(i, v + 20, str(v), ha='center', fontsize=8)

plt.tight_layout()
plt.savefig('figures/genomic_overview.png', dpi=150, bbox_inches='tight')
print("\nFigure 1 saved!")
print(f"Total BDBV genomes: {len(records)}")
print(f"Mean genome length: {sum(lengths)/len(lengths):.1f} bp")
print(f"Mean GC content: {sum(gc_values)/len(gc_values):.2f}%")
