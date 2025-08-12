def convert_runner_to_lammps(input_filename, output_filename):
    BOHR_TO_ANGSTROM = 0.529177

    with open(input_filename, 'r') as infile:
        data = infile.readlines()

    atoms = []
    lattice = []
    atom_types = set()
    structure_blocks = []
    in_atom_block = False

    for line in data:
        if line.startswith('begin'):
            atoms = []
            lattice = []
            in_atom_block = True
        elif line.startswith('end'):
            structure_blocks.append((lattice, atoms))
            in_atom_block = False
        elif in_atom_block:
            if line.startswith('lattice'):
                lattice.append([float(x) * BOHR_TO_ANGSTROM for x in line.split()[1:]])
            elif line.startswith('atom'):
                parts = line.split()
                atom_info = {
                    'element': parts[4],
                    'x': float(parts[1]) * BOHR_TO_ANGSTROM,
                    'y': float(parts[2]) * BOHR_TO_ANGSTROM,
                    'z': float(parts[3]) * BOHR_TO_ANGSTROM
                }
                atoms.append(atom_info)
                atom_types.add(parts[4])

    with open(output_filename, 'w') as outfile:
        outfile.write("ITEM: TIMESTEP\n0\n")
        for step, (lattice, atoms) in enumerate(structure_blocks):
            xlo, xhi = 0.0, lattice[0][0]
            ylo, yhi = 0.0, lattice[1][1]
            zlo, zhi = 0.0, lattice[2][2]

            outfile.write("ITEM: NUMBER OF ATOMS\n")
            outfile.write(f"{len(atoms)}\n")
            outfile.write("ITEM: BOX BOUNDS pp pp pp\n")
            outfile.write(f"{xlo} {xhi}\n")
            outfile.write(f"{ylo} {yhi}\n")
            outfile.write(f"{zlo} {zhi}\n")

            outfile.write("ITEM: ATOMS id type x y z\n")
            for i, atom in enumerate(atoms):
                outfile.write(f"{i+1} {atom['element']} {atom['x']} {atom['y']} {atom['z']}\n")

            if step < len(structure_blocks) - 1:
                outfile.write("ITEM: TIMESTEP\n")
                outfile.write(f"{step+1}\n")

# Use the function to convert your file
convert_runner_to_lammps('input.data-add', 'input.data-add.lammpstrj')
