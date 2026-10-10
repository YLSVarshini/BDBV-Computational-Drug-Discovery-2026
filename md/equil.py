import sys, time
from openmm.app import *
from openmm import *
from openmm.unit import *
from openff.toolkit import Molecule
from openmmforcefields.generators import SMIRNOFFTemplateGenerator

name = sys.argv[1]
mol = Molecule.from_file(f"md/{name}_lig.sdf"); mol.name="LIG"
ligff = sorted(f for f in SMIRNOFFTemplateGenerator.INSTALLED_FORCEFIELDS if f.startswith("openff-2"))[-1]
ff = ForceField("amber14-all.xml","amber14/tip3p.xml")
ff.registerTemplateGenerator(SMIRNOFFTemplateGenerator(molecules=[mol], forcefield=ligff).generator)

pdb = PDBFile(f"md/{name}_min.pdb")
system = ff.createSystem(pdb.topology, nonbondedMethod=PME,
                         nonbondedCutoff=1.0*nanometer, constraints=HBonds)
system.addForce(MonteCarloBarostat(1*bar, 300*kelvin))
integ = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
sim = Simulation(pdb.topology, system, integ, Platform.getPlatformByName('CUDA'))
sim.loadState(f"md/{name}_min.xml")

print("heating + equilibrating 250 ps...")
sim.context.setVelocitiesToTemperature(300*kelvin)
t0=time.time(); sim.step(125000); dt=time.time()-t0
nsday = (250/1000) / (dt/86400)
print(f"250 ps took {dt/60:.1f} min  ->  {nsday:.1f} ns/day")
sim.saveState(f"md/{name}_equil.xml")
st=sim.context.getState(getPositions=True)
PDBFile.writeFile(pdb.topology, st.getPositions(), open(f"md/{name}_equil.pdb","w"))
print("equilibrated")
