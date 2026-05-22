import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import json

# Load results
with open('results/docking_results.json') as f:
    results = json.load(f)

sorted_results = sorted(results.items(), key=lambda x: x[1])
compounds = [r[0] for r in sorted_results]
affinities = [r[1] for r in sorted_results]

colors = []
for a in affinities:
    if a <= -7: colors.append('#D62728')
    elif a <= -6: colors.append('#FF7F0E')
    else: colors.append('#2CA02C')

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Molecular Docking Results: Drug Candidates vs BDBV VP35\n(PDB: 5VKD | AutoDock Vina v1.2.5 | Exhaustiveness=16)',
             fontsize=13, fontweight='bold')

# Plot 1: Binding affinities
bars = axes[0].barh(compounds, affinities, color=colors, alpha=0.85, edgecolor='black')
axes[0].set_xlabel('Binding Affinity (kcal/mol)', fontsize=11)
axes[0].set_title('Binding Affinities Against BDBV VP35', fontsize=11)
axes[0].axvline(x=-7.0, color='red', linestyle='--', alpha=0.7, label='Strong binding threshold (-7.0)')
axes[0].axvline(x=-5.0, color='orange', linestyle='--', alpha=0.7, label='Moderate binding threshold (-5.0)')
axes[0].legend(fontsize=9)
for bar, val in zip(bars, affinities):
    axes[0].text(val - 0.05, bar.get_y() + bar.get_height()/2,
                 f'{val:.3f}', va='center', ha='right', fontsize=9, color='white', fontweight='bold')

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#D62728', label='Strong (≤ -7.0 kcal/mol)'),
    Patch(facecolor='#FF7F0E', label='Moderate (-7.0 to -5.0 kcal/mol)'),
    Patch(facecolor='#2CA02C', label='Weak (> -5.0 kcal/mol)'),
]
axes[0].legend(handles=legend_elements, loc='lower right', fontsize=9)

# Plot 2: Radar/comparison chart
top5 = sorted_results[:5]
top_names = [r[0] for r in top5]
top_affs = [abs(r[1]) for r in top5]

bar_colors = ['#D62728', '#D62728', '#FF7F0E', '#FF7F0E', '#FF7F0E']
bars2 = axes[1].bar(top_names, top_affs, color=bar_colors, alpha=0.85, edgecolor='black')
axes[1].set_ylabel('|Binding Affinity| (kcal/mol)', fontsize=11)
axes[1].set_title('Top 5 Drug Candidates Against BDBV VP35', fontsize=11)
axes[1].tick_params(axis='x', rotation=20)
axes[1].set_ylim(0, 10)

for bar, val, (name, aff) in zip(bars2, top_affs, top5):
    axes[1].text(bar.get_x() + bar.get_width()/2, val + 0.1,
                 f'{aff:.3f}\nkcal/mol', ha='center', fontsize=9, fontweight='bold')

axes[1].text(0.02, 0.95,
             'Imatinib (cancer drug) and\nSertraline (antidepressant)\nshow strongest binding —\nnovel repurposing candidates\nfor BDBV treatment',
             transform=axes[1].transAxes, fontsize=9,
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='orange'),
             verticalalignment='top')

plt.tight_layout()
plt.savefig('figures/docking_results.png', dpi=150, bbox_inches='tight')
print("Docking results figure saved!")
