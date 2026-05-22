import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# BDBV Outbreak Data (from WHO/CDC public reports)
outbreaks = {
    '2007\nUganda': {'cases': 116, 'deaths': 39, 'cfr': 33.6, 'duration': 90},
    '2012\nDRC': {'cases': 36, 'deaths': 13, 'cfr': 36.1, 'duration': 30},
    '2026\nDRC/Uganda': {'cases': 575, 'deaths': 148, 'cfr': 25.7, 'duration': 7},
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Bundibugyo Ebolavirus (BDBV): Epidemiological Comparison\nAll Three Known Outbreaks (2007, 2012, 2026)',
             fontsize=13, fontweight='bold')

names = list(outbreaks.keys())
cases = [outbreaks[o]['cases'] for o in names]
deaths = [outbreaks[o]['deaths'] for o in names]
cfr = [outbreaks[o]['cfr'] for o in names]
colors = ['#FF7F0E', '#2CA02C', '#D62728']

# Plot 1: Cases vs Deaths
x = np.arange(len(names))
width = 0.35
axes[0,0].bar(x - width/2, cases, width, label='Cases', color=colors, alpha=0.8)
axes[0,0].bar(x + width/2, deaths, width, label='Deaths',
              color=colors, alpha=0.4, edgecolor='black')
axes[0,0].set_xticks(x)
axes[0,0].set_xticklabels(names)
axes[0,0].set_ylabel('Count')
axes[0,0].set_title('Cases vs Deaths by Outbreak')
axes[0,0].legend()
for i, (c, d) in enumerate(zip(cases, deaths)):
    axes[0,0].text(i - width/2, c + 5, str(c), ha='center', fontsize=9)
    axes[0,0].text(i + width/2, d + 5, str(d), ha='center', fontsize=9)

# Plot 2: CFR comparison
bars = axes[0,1].bar(names, cfr, color=colors, alpha=0.8, edgecolor='black')
axes[0,1].set_ylabel('Case Fatality Rate (%)')
axes[0,1].set_title('Case Fatality Rate by Outbreak')
axes[0,1].set_ylim(0, 50)
axes[0,1].axhline(y=36.1, color='gray', linestyle='--', alpha=0.5, label='2012 CFR baseline')
for bar, val in zip(bars, cfr):
    axes[0,1].text(bar.get_x() + bar.get_width()/2, val + 0.5,
                   f'{val}%', ha='center', fontsize=11, fontweight='bold')

# Plot 3: BDBV vs Zaire EBOV CFR comparison
species_cfr = {
    'BDBV\n(avg)': 31.8,
    'Zaire EBOV\n(2014 W.Africa)': 70.8,
    'Sudan SUDV\n(2022)': 55.0,
}
sp_names = list(species_cfr.keys())
sp_cfr = list(species_cfr.values())
sp_colors = ['#D62728', '#9467BD', '#8C564B']
bars2 = axes[1,0].bar(sp_names, sp_cfr, color=sp_colors, alpha=0.8)
axes[1,0].set_ylabel('Case Fatality Rate (%)')
axes[1,0].set_title('CFR Comparison: BDBV vs Other Ebolaviruses')
axes[1,0].set_ylim(0, 90)
for bar, val in zip(bars2, sp_cfr):
    axes[1,0].text(bar.get_x() + bar.get_width()/2, val + 1,
                   f'{val}%', ha='center', fontsize=11, fontweight='bold')

# Plot 4: Timeline
years = [2007, 2012, 2026]
case_sizes = [116, 36, 575]
axes[1,1].scatter(years, case_sizes, s=[c*2 for c in case_sizes],
                  c=colors, alpha=0.8, edgecolors='black', linewidth=1.5)
axes[1,1].plot(years, case_sizes, 'k--', alpha=0.3)
for y, c, name in zip(years, case_sizes, ['2007 Uganda', '2012 DRC', '2026 DRC/Uganda']):
    axes[1,1].annotate(f'{name}\n({c} cases)',
                       xy=(y, c), xytext=(10, 10),
                       textcoords='offset points', fontsize=9,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
axes[1,1].set_xlabel('Year')
axes[1,1].set_ylabel('Confirmed/Suspected Cases')
axes[1,1].set_title('BDBV Outbreak Timeline (2007-2026)')
axes[1,1].set_xlim(2004, 2029)

plt.tight_layout()
plt.savefig('figures/epidemiology.png', dpi=150, bbox_inches='tight')
print("Epidemiology figure saved!")
print("\n=== KEY EPIDEMIOLOGICAL FINDINGS ===")
print(f"2026 outbreak is {575/116:.1f}x larger than 2007 outbreak in case count")
print(f"2026 CFR ({25.7}%) lower than 2007 ({33.6}%) and 2012 ({36.1}%)")
print(f"BDBV average CFR ({31.8}%) significantly lower than Zaire EBOV ({70.8}%)")
print(f"First PHEIC declaration for BDBV: May 17, 2026")
