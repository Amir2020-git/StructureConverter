import os

# Conversion factors
ANGSTROM_TO_BOHR = 1.88973
EV_TO_HARTREE = 0.0367493
FORCE_CONVERSION = EV_TO_HARTREE / ANGSTROM_TO_BOHR

def read_poscar(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        scale_factor = float(lines[1].strip())
        lattice_vectors = [list(map(lambda x: float(x) * ANGSTROM_TO_BOHR, line.split())) for line in lines[2:5]]
        element_symbols = lines[5].split()
        num_atoms = list(map(int, lines[6].split()))
        total_atoms = sum(num_atoms)
        atom_positions = [list(map(lambda x: float(x) * ANGSTROM_TO_BOHR, lines[8 + i].split())) for i in range(total_atoms)]
        atom_types = []
        for i, count in enumerate(num_atoms):
            atom_types.extend([element_symbols[i]] * count)
        return scale_factor, lattice_vectors, atom_positions, atom_types

def read_outcar(file_path, num_atoms):
    forces = []
    energy = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'energy(sigma->0)' in line:
                energy = float(line.split()[-1]) * EV_TO_HARTREE
            if 'TOTAL-FORCE' in line:
                start_index = lines.index(line) + 2
                for i in range(start_index, start_index + num_atoms):
                    forces.append(list(map(lambda x: float(x) * FORCE_CONVERSION, lines[i].split()[3:])))
                break
    if len(forces) != num_atoms:
        raise ValueError(f"Number of forces read ({len(forces)}) does not match number of atoms ({num_atoms})")
    return energy, forces

def write_runner_input(output_file, subfolder, lattice_vectors, atom_positions, atom_types, forces, energy):
    if energy is None:
        raise ValueError("Energy value is None")
    with open(output_file, 'a') as file:
        file.write(f"# Structure from {subfolder}\n")  # Comment indicating source folder
        file.write("begin\n")
        for vector in lattice_vectors:
            file.write(f"lattice {' '.join(f'{v:.6f}' for v in vector)}\n")
        for i, pos in enumerate(atom_positions):
            file.write(f"atom {' '.join(f'{p:.10f}' for p in pos)} {atom_types[i]} 0.000 0.0 {' '.join(f'{f:.6f}' for f in forces[i])}\n")
        file.write(f"energy {energy:.8f}\n")
        file.write("charge 0.0\n")
        file.write("end\n")

def process_structures(structures_dir, output_file):
    subfolders = sorted([f.path for f in os.scandir(structures_dir) if f.is_dir()])  # Ensure alphabetical order
    for subfolder in subfolders:
        poscar_path = os.path.join(subfolder, 'POSCAR')
        outcar_path = os.path.join(subfolder, 'OUTCAR')
        if os.path.exists(poscar_path) and os.path.exists(outcar_path):
            try:
                scale_factor, lattice_vectors, atom_positions, atom_types = read_poscar(poscar_path)
                num_atoms = len(atom_positions)
                energy, forces = read_outcar(outcar_path, num_atoms)
                write_runner_input(output_file, subfolder, lattice_vectors, atom_positions, atom_types, forces, energy)
            except ValueError as ve:
                print(f"ValueError processing {subfolder}: {ve}")
            except Exception as e:
                print(f"Error processing {subfolder}: {e}")

if __name__ == "__main__":
    structures_directory = "structures"  # Change this to the path of your structures directory
    output_data_file = "input.data"
    
    # Remove the existing output file if it exists
    if os.path.exists(output_data_file):
        os.remove(output_data_file)
    
    process_structures(structures_directory, output_data_file)
