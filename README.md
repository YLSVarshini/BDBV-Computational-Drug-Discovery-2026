# BDBV Computational Drug Discovery 2026

## In Silico Comparative Genomic Analysis and Molecular Docking of Antiviral Compounds Against Bundibugyo Ebolavirus Nucleoprotein (NP) in the Context of the 2026 PHEIC Outbreak

**Author:** Yedavalli Lakshmi Sai Varshini

---

## Background

On May 17, 2026, WHO declared a Public Health Emergency of International Concern (PHEIC) for the Bundibugyo ebolavirus (BDBV) outbreak in DRC and Uganda — the third known BDBV outbreak and the first ever PHEIC for this species. Unlike Zaire ebolavirus, for which FDA-approved treatments exist, BDBV has no approved vaccines or therapeutics. This study presents the first dedicated in silico drug target analysis specifically focused on BDBV proteins.

---

## Repository Structure

    BDBV-Computational-Drug-Discovery-2026/
    |
    |-- data/
    |   |-- genomes/       # 26 BDBV + 4 Orthoebolavirus genome sequences
    |   |-- proteins/      # PDB structures + PDBQT files
    |   |-- ligands/       # 10 antiviral compounds (SDF + PDBQT)
    |
    |-- scripts/
    |   |-- 01_genomic_analysis.py
    |   |-- 02_alignment_phylogenetics.py
    |   |-- 03_tree_visualization.py
    |   |-- 04_mutation_analysis.py
    |   |-- 05_epidemiology.py
    |   |-- 06_docking_visualization.py
    |   |-- 07_autodock_vina_docking.py
    |
    |-- results/
    |   |-- docking/
    |   |-- tree/
    |   |-- docking_results.json
    |
    |-- figures/
    |   |-- genomic_overview.png
    |   |-- phylogenetic_tree.png
    |   |-- mutation_analysis.png
    |   |-- epidemiology.png
    |   |-- docking_results.png
    |
    |-- README.md

---

## Methods Summary

| Step | Tool | Version |
|------|------|---------|
| Genome download | NCBI Entrez via Biopython | 1.86 |
| Multiple sequence alignment | MAFFT | 7.490 |
| Phylogenetic inference | IQ-TREE | 2.0.7 |
| Protein structure | RCSB PDB 5VKD | 1.749 Angstrom resolution |
| Ligand preparation | OpenBabel | 3.1.1 |
| Molecular docking | AutoDock Vina | 1.2.5 |
| ADMET profiling | SwissADME | Web server |

---

## Key Results

### Docking Results — BDBV NP (PDB: 5VKD)

| Rank | Compound | Affinity (kcal/mol) | Interpretation |
|------|----------|---------------------|----------------|
| 1 | Imatinib | -8.006 | Strong |
| 2 | Sertraline | -7.123 | Strong |
| 3 | Clomiphene | -6.816 | Moderate |
| 4 | Remdesivir | -6.709 | Moderate |
| 5 | Toremifene | -6.687 | Moderate |

### Genomic Findings

- 26 BDBV genomes analysed spanning 2007 Uganda and 2012 DRC outbreaks
- Mean GC content: 42.12% — highest among all Ebolaviruses
- Approximately 250 mutations between 2007 and 2012 outbreak isolates
- BDBV forms a phylogenetically distinct clade with 100% bootstrap support
- 2026 outbreak is 5x larger than 2007 outbreak in case count

---

## How to Reproduce

### Requirements

```bash
conda install biopython matplotlib seaborn scipy numpy -y
sudo apt install mafft iqtree openbabel -y
```

AutoDock Vina: download from https://github.com/ccsb-scripps/AutoDock-Vina

### Run Pipeline

```bash
python3 scripts/01_genomic_analysis.py
python3 scripts/02_alignment_phylogenetics.py
python3 scripts/04_mutation_analysis.py
python3 scripts/05_epidemiology.py
python3 scripts/07_autodock_vina_docking.py
python3 scripts/06_docking_visualization.py
```

## Scope and Limitations

**What was screened.** PDB 5VKD is the BDBV nucleoprotein (NP) C-terminal domain in complex with a Fab fragment. The receptor used here is chain A, residues 638-739. The structure contains no small-molecule ligand (only water), so the docking could not be validated by re-docking a co-crystallised ligand.

**Pocket not targeted.** A hydrophobic pocket on the NP core (around residues F280 and L284, EBOV numbering) binds VP35 and has been targeted by small molecules in Ebola virus work (Easton et al., 2018, https://doi.org/10.1016/j.antiviral.2018.06.003). That pocket lies outside the region docked here, so these results do not address it.

**Other limitations.**
- Docking is a single rigid-receptor AutoDock Vina run with a grid box centred on the protein, not on a defined pocket. Scores are rankings, not measured affinities.
- No positive control or decoy set was used, so scoring performance is unbenchmarked.
- Only 10 compounds were screened, and ADMET (SwissADME) was run for the top 3 only. No toxicity prediction was done.
- The 2007 isolate is the source of the reference genome, so the 2007-vs-reference comparison shows 0 mutations and is uninformative. The 2012 isolates differ from the reference by about 250 positions.
- No 2026 outbreak sequences were used, and nothing here has been tested experimentally.

## Acknowledgements

Genome sequences from NCBI GenBank. Protein structures from RCSB PDB. ADMET profiling via SwissADME. All analyses conducted using publicly available data and open source tools.
