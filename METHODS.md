# Computational Environment and Methods

## System
- OS: Ubuntu 22.04.5 LTS (WSL2 on Windows 11)
- Python: 3.13 (Miniconda)
- RAM: 16GB
- CPU: 16 threads

## Tool Versions
- Biopython: 1.86
- MAFFT: 7.490
- IQ-TREE: 2.0.7
- AutoDock Vina: 1.2.5
- OpenBabel: 3.1.1
- pandas: 2.3.3
- matplotlib: 3.10.9
- seaborn: 0.13.2
- scipy: 1.15.3
- numpy: 2.2.6

## Databases Used
- NCBI GenBank (genome sequences)
- RCSB PDB (protein structures)
- PubChem (ligand structures)
- SwissADME (ADMET profiling)

## Key Commands

### Genome Download
```python
from Bio import Entrez
Entrez.email = "your@email.com"
handle = Entrez.esearch(db="nucleotide",
    term="Bundibugyo ebolavirus[Organism] complete genome",
    retmax=100)
```

### MAFFT Alignment
```bash
mafft --auto --thread 4 combined_sequences.fasta > aligned.fasta
```

### IQ-TREE Phylogenetics
```bash
iqtree -s aligned.fasta -m GTR+G -bb 1000 -nt AUTO
```

### AutoDock Vina Docking
```bash
vina --receptor receptor.pdbqt --ligand ligand.pdbqt \
     --center_x 56.99 --center_y 66.40 --center_z 49.82 \
     --size_x 30 --size_y 30 --size_z 30 \
     --exhaustiveness 16 --num_modes 9
```
