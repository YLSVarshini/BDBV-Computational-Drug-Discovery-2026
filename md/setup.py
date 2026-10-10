import sys
from openmm.app import *
from pdbfixer import PDBFixer
from openff.toolkit import Molecule

name = sys.argv[1]
smiles = {"Sertraline":"CNC1CCC(c2ccccc2)c2ccc(Cl)c(Cl)c21",
          "Tolcapone":"Cc1ccc(C(=O)c2cc(O)c(O)c([N+](=O)[O-])c2)cc1"}[name]

mol = Molecule.from_smiles(smiles, allow_undefined_stereo=True)
heavy = sum(1 for a in mol.atoms if a.atomic_number > 1)
posed = PDBFile(f"md/{name}_pose.pdb")
pheavy = sum(1 for a in posed.topology.atoms() if a.element.symbol != "H")
print(f"{name}: SMILES heavy={heavy}, pose heavy={pheavy}, match={heavy==pheavy}")

fixer = PDBFixer("proteins/4YPI_chainA_receptor.pdb")
fixer.findMissingResidues()
print("missing residues:", fixer.missingResidues)
fixer.missingResidues = {}
fixer.findNonstandardResidues(); fixer.replaceNonstandardResidues()
fixer.findMissingAtoms()
print("residues missing atoms:", len(fixer.missingAtoms))
fixer.addMissingAtoms()
fixer.addMissingHydrogens(7.4)
PDBFile.writeFile(fixer.topology, fixer.positions, open("md/protein_fixed.pdb","w"))
print("protein prepared:", fixer.topology.getNumAtoms(), "atoms")
