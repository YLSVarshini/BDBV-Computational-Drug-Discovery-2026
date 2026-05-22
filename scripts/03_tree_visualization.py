import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Bio import Phylo
import io

# Read and plot the phylogenetic tree
tree = Phylo.read("results/tree/bdbv_tree.treefile", "newick")

fig, ax = plt.subplots(figsize=(12, 8))
Phylo.draw(tree, axes=ax, do_show=False)
ax.set_title("Maximum Likelihood Phylogenetic Tree of Ebolaviruses\n(BDBV 2007 & 2012 outbreaks vs other species)", 
             fontsize=12, fontweight='bold')
ax.set_xlabel("Branch Length (substitutions/site)")
plt.tight_layout()
plt.savefig("figures/phylogenetic_tree.png", dpi=150, bbox_inches='tight')
print("Phylogenetic tree figure saved!")

# Print tree in text format
print("\n=== TREE TOPOLOGY ===")
Phylo.draw_ascii(tree)
