#!/bin/bash
cd ~/ebola_project
for L in decoys/pdbqt/*.pdbqt; do
  N=$(basename "$L" .pdbqt)
  [ -s results/decoy_vinardo/${N}_out.pdbqt ] && continue
  vina --receptor proteins/4YPI_receptor_H.pdbqt --ligand "$L" --scoring vinardo \
       --center_x 128.50 --center_y 11.32 --center_z -123.47 \
       --size_x 24 --size_y 24 --size_z 24 \
       --exhaustiveness 16 --num_modes 9 --seed 42 \
       --out results/decoy_vinardo/${N}_out.pdbqt > /dev/null 2>&1
done
echo "DONE $(date)" > results/decoy_vinardo/FINISHED
