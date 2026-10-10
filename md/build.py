import sys
from openmm.app import *
from openmm import *
from openmm.unit import *
from openff.toolkit import Molecule
from openmmforcefields.generators import SMIRNOFFTemplateGenerator

name = sys.argv[1]

installed = SMIRNOFFTemplateGenerator.INSTALLED_FORCEFIELDS
sage = sorted([f for f in installed if f.startswith("openff-2")])
ligff = sage[-1] if sage else sorted(f for f in installed if f.startswith("openff"))[-1]
print("ligand force field:", ligff)

mol = Molecule.from_file(f"md/{name}_lig.sdf")
mol.name = "LIG"
print(f"{name}: {mol.n_atoms} atoms, formal charge {mol.total_charge}")

prot = PDBFile("md/protein_fixed.pdb")
ff = ForceField("amber14-all.xml", "amber14/tip3p.xml")
ff.registerTemplateGenerator(
    SMIRNOFFTemplateGenerator(molecules=[mol], forcefield=ligff).generator)

model = Modeller(prot.topology, prot.positions)
model.add(mol.to_topology().to_openmm(), mol.conformers[0].to_openmm())
print("complex:", model.topology.getNumAtoms(), "atoms")

model.addSolvent(ff, padding=1.0*nanometer, ionicStrength=0.15*molar, model='tip3p')
print("solvated:", model.topology.getNumAtoms(), "atoms")
PDBFile.writeFile(model.topology, model.positions, open(f"md/{name}_solvated.pdb","w"))

system = ff.createSystem(model.topology, nonbondedMethod=PME,
                         nonbondedCutoff=1.0*nanometer, constraints=HBonds)
system.addForce(MonteCarloBarostat(1*bar, 300*kelvin))
integ = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
sim = Simulation(model.topology, system, integ, Platform.getPlatformByName('CUDA'))
sim.context.setPositions(model.positions)

print("minimising...")
sim.minimizeEnergy()
st = sim.context.getState(getPositions=True, getEnergy=True)
print("energy after minimisation:", st.getPotentialEnergy())
with open(f"md/{name}_min.pdb","w") as f:
    PDBFile.writeFile(model.topology, st.getPositions(), f)
sim.saveState(f"md/{name}_min.xml")
print("ready")
