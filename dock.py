import subprocess
import os
import json

CENTER_X = 56.99
CENTER_Y = 66.40
CENTER_Z = 49.82
SIZE_X = 30
SIZE_Y = 30
SIZE_Z = 30

ligands = ['Remdesivir','Favipiravir','Toremifene','Clomiphene',
           'Amodiaquine','Chloroquine','Emetine','Bepridil','Sertraline','Imatinib']

os.makedirs('results/docking', exist_ok=True)
results = {}

print("=== AUTODOCK VINA DOCKING: BDBV NP (5VKD Chain A) ===\n")

for ligand in ligands:
    lig_path = f'ligands/{ligand}.pdbqt'
    out_path = f'results/docking/{ligand}_out.pdbqt'

    print(f"\nDocking {ligand}...")
    cmd = [
        'vina',
        '--receptor', 'proteins/5VKD_receptor.pdbqt',
        '--ligand', lig_path,
        '--out', out_path,
        '--center_x', str(CENTER_X),
        '--center_y', str(CENTER_Y),
        '--center_z', str(CENTER_Z),
        '--size_x', str(SIZE_X),
        '--size_y', str(SIZE_Y),
        '--size_z', str(SIZE_Z),
        '--exhaustiveness', '16',
        '--num_modes', '9',
    ]

    result = subprocess.run(cmd, capture_output=False, text=True)

    # Parse from stdout
    best = None
    for line in (result.stdout or '').split('\n'):
        line = line.strip()
        if line.startswith('1 ') or line.startswith('1\t'):
            parts = line.split()
            try:
                best = float(parts[1])
                break
            except:
                pass

    # If stdout parsing failed, re-run and capture
    if not best:
        result2 = subprocess.run(cmd, capture_output=True, text=True)
        for line in result2.stdout.split('\n'):
            line = line.strip()
            if line.startswith('1'):
                parts = line.split()
                try:
                    best = float(parts[1])
                    break
                except:
                    pass

    if best:
        results[ligand] = best
        print(f">>> {ligand}: {best} kcal/mol")
    else:
        print(f">>> {ligand}: parsing failed")

print("\n\n=== FINAL DOCKING RESULTS ===")
print(f"{'Rank':<5} {'Compound':<15} {'Affinity (kcal/mol)':<20} {'Interpretation'}")
print("-" * 65)
sorted_results = sorted(results.items(), key=lambda x: x[1])
for rank, (lig, aff) in enumerate(sorted_results, 1):
    interp = "Strong" if aff <= -7 else "Moderate" if aff <= -5 else "Weak"
    print(f"{rank:<5} {lig:<15} {aff:<20} {interp}")

with open('results/docking_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved to results/docking_results.json")
