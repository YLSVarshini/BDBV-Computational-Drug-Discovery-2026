from Bio import SeqIO, AlignIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Load alignment
alignment = AlignIO.read("genomes/aligned.fasta", "fasta")

# Get indices for BDBV sequences
names = [r.id for r in alignment]
print("Sequences in alignment:", names)

# Find BDBV sequences
bdbv_ref_idx = names.index("BDBV_REF")
bdbv_2007_idx = names.index("BDBV_2007_Uganda")
bdbv_2012_indices = [i for i, n in enumerate(names) if "2012_DRC" in n]

ref_seq = str(alignment[bdbv_ref_idx].seq)
seq_2007 = str(alignment[bdbv_2007_idx].seq)

print(f"\nReference length: {len(ref_seq)}")
print(f"2007 Uganda length: {len(seq_2007)}")

# Find mutations between REF and 2007
mutations_2007 = []
for i, (r, s) in enumerate(zip(ref_seq, seq_2007)):
    if r != s and r != '-' and s != '-':
        mutations_2007.append((i+1, r, s))

print(f"\nMutations REF vs 2007 Uganda: {len(mutations_2007)}")
for pos, ref, alt in mutations_2007[:20]:
    print(f"  Position {pos}: {ref} -> {alt}")

# Find mutations in 2012 DRC isolates
print(f"\n=== 2012 DRC MUTATIONS vs REFERENCE ===")
all_2012_mutations = []
for idx in bdbv_2012_indices:
    seq_2012 = str(alignment[idx].seq)
    muts = []
    for i, (r, s) in enumerate(zip(ref_seq, seq_2012)):
        if r != s and r != '-' and s != '-':
            muts.append(i+1)
    all_2012_mutations.append(muts)
    print(f"{names[idx]}: {len(muts)} mutations vs reference")

# Plot mutation positions across genome
fig, axes = plt.subplots(3, 1, figsize=(14, 10))
fig.suptitle('BDBV Mutation Analysis: 2007 vs 2012 Outbreaks', 
             fontsize=13, fontweight='bold')

# Plot 1: 2007 mutation positions
if mutations_2007:
    positions_2007 = [m[0] for m in mutations_2007]
    axes[0].vlines(positions_2007, 0, 1, color='blue', alpha=0.7, linewidth=1.5)
    axes[0].set_title(f'2007 Uganda Mutations vs Reference (n={len(mutations_2007)})')
    axes[0].set_xlabel('Genome Position (bp)')
    axes[0].set_xlim(0, 19000)
    axes[0].set_yticks([])

# Add gene annotations
gene_regions = {
    'NP': (470, 3026),
    'VP35': (3033, 4407),
    'VP40': (4422, 5513),
    'GP': (6038, 8068),
    'VP30': (8508, 9375),
    'VP24': (9885, 10706),
    'L': (11501, 18282)
}
colors_genes = ['#FF9999','#FFB366','#FFFF99','#99FF99','#99CCFF','#CC99FF','#FF99CC']

for ax in axes[:2]:
    for (gene, (start, end)), color in zip(gene_regions.items(), colors_genes):
        ax.axvspan(start, end, alpha=0.15, color=color, label=gene)
    ax.legend(loc='upper right', fontsize=7, ncol=7)

# Plot 2: 2012 mutations combined
all_pos_2012 = [p for muts in all_2012_mutations for p in muts]
if all_pos_2012:
    axes[1].vlines(all_pos_2012, 0, 1, color='red', alpha=0.5, linewidth=1)
    axes[1].set_title(f'2012 DRC Mutations vs Reference (combined, n={len(set(all_pos_2012))} unique positions)')
    axes[1].set_xlabel('Genome Position (bp)')
    axes[1].set_xlim(0, 19000)
    axes[1].set_yticks([])

# Plot 3: Mutation density
bins = np.arange(0, 19000, 500)
axes[2].hist(positions_2007 if mutations_2007 else [0], 
             bins=bins, color='blue', alpha=0.6, label='2007 Uganda')
axes[2].hist(all_pos_2012 if all_pos_2012 else [0], 
             bins=bins, color='red', alpha=0.6, label='2012 DRC')
axes[2].set_title('Mutation Density Across Genome (500bp windows)')
axes[2].set_xlabel('Genome Position (bp)')
axes[2].set_ylabel('Mutation Count')
axes[2].legend()
for (gene, (start, end)), color in zip(gene_regions.items(), colors_genes):
    axes[2].axvspan(start, end, alpha=0.1, color=color)

plt.tight_layout()
plt.savefig('figures/mutation_analysis.png', dpi=150, bbox_inches='tight')
print("\nFigure 2 saved: figures/mutation_analysis.png")
