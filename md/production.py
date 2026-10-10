import sys
from openmm.app import *
from openmm import *
from openmm.unit import *
from openff.toolkit import Molecule
from openmmforcefields.generators import SMIRNOFFTemplateGenerator

name, ns = sys.argv[1], float(sys.argv[2])
mol = Molecule.from_file(f"md/{name}_lig.sdf"); mol.name="LIG"
ligff = sorted(f for f in SMIRNOFFTemplateGenerator.INSTALLED_FORCEFIELDS if f.startswith("openff-2"))[-1]
ff = ForceField("amber14-all.xml","amber14/tip3p.xml")
ff.registerTemplateGenerator(SMIRNOFFTemplateGenerator(molecules=[mol], forcefield=ligff).generator)

pdb = PDBFile(f"md/{name}_equil.pdb")
system = ff.createSystem(pdb.topology, nonbondedMethod=PME,
                         nonbondedCutoff=1.0*nanometer, constraints=HBonds)
system.addForce(MonteCarloBarostat(1*bar, 300*kelvin))
integ = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
sim = Simulation(pdb.topology, system, integ, Platform.getPlatformByName('CUDA'))
sim.loadState(f"md/{name}_equil.xml")

steps = int(ns*1000/0.002)
sim.reporters.append(DCDReporter(f"md/{name}_traj.dcd", 25000))     # every 50 ps
sim.reporters.append(StateDataReporter(f"md/{name}_log.csv", 25000, step=True,
    time=True, potentialEnergy=True, temperature=True, volume=True, speed=True))
sim.reporters.append(CheckpointReporter(f"md/{name}.chk", 250000))
print(f"running {ns} ns = {steps} steps")
sim.step(steps)
sim.saveState(f"md/{name}_final.xml")
open(f"md/{name}_PRODUCTION_DONE","w").write("done\n")
print("done")
