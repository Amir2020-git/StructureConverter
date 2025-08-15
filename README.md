Structure Conversion Tools

This repository provides two Python utilities for converting atomistic simulation data between different formats commonly used in RuNNer, LAMMPS, and VASP workflows.

Contents

1. VASP → RuNNer Converter
- Reads POSCAR (atomic positions, lattice vectors) and OUTCAR (energies, forces) from VASP calculations
- Converts lengths from Ångström to Bohr and energies from eV to Hartree
- Outputs RuNNer-formatted input.data files with:
    - Lattice vectors
    - Atomic positions and types
    - Forces (in Hartree/Bohr)
    - Total energy (in Hartree)

2. RuNNer → LAMMPS Converter
- Converts RuNNer-format structure/trajectory files into LAMMPS-readable data files.
