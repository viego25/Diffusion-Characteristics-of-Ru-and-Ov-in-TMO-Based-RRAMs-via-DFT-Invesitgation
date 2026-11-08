import os
import glob
import numpy as np

def parse_cube_header(file_path):
    """
    Parses the header of a Gaussian Cube file.
    """
    with open(file_path, 'r') as f:
        comment_1 = f.readline()
        comment_2 = f.readline()
        
        # Line 3: Natoms, Origin (X, Y, Z)
        line3 = f.readline().split()
        natoms = int(line3[0])
        origin = [float(x) for x in line3[1:4]]
        
        # Lines 4-6: Ngrid, Voxel vector (X, Y, Z)
        grid_info = []
        for _ in range(3):
            line = f.readline().split()
            grid_info.append({
                'n': int(line[0]),
                'vec': [float(x) for x in line[1:4]]
            })
            
        # Lines 7 to 7+natoms-1: Atomic positions
        atoms = []
        for _ in range(abs(natoms)):
            line = f.readline().split()
            atoms.append({
                'atomic_num': int(line[0]),
                'charge': float(line[1]),
                'pos': [float(x) for x in line[2:5]]
            })
            
        return comment_1, comment_2, natoms, origin, grid_info, atoms

def read_cube_data(file_path, shape):
    """
    Reads the 3D volumetric numerical data from a cube file.
    """
    with open(file_path, 'r') as f:
        # Skip header lines: 2 comments + 1 origin + 3 vectors + natoms
        line3 = None
        for i in range(3):
            line = f.readline()
            if i == 2:
                line3 = line
        
        natoms = abs(int(line3.split()[0]))
        
        # Skip remaining header lines
        for _ in range(3 + natoms):
            f.readline()
            
        # Read volumetric data values
        data = np.fromstring(f.read(), sep=' ')
        return data.reshape(shape)

def sum_cube_files(input_dir, output_file):
    """
    Sums all .cube files in input_dir and saves the result to output_file.
    """
    cube_files = sorted(glob.glob(os.path.join(input_dir, "*.cube")))
    
    if not cube_files:
        print(f"No .cube files found in directory: '{input_dir}'")
        return

    print(f"Found {len(cube_files)} cube file(s):")
    for file in cube_files:
        print(f"  - {os.path.basename(file)}")

    # Parse header from the first file to establish structure template
    template_file = cube_files[0]
    comment1, comment2, natoms, origin, grid_info, atoms = parse_cube_header(template_file)
    
    # Calculate grid shape (NX, NY, NZ)
    shape = (grid_info[0]['n'], grid_info[1]['n'], grid_info[2]['n'])
    
    # Initialize array to store summed grid values
    summed_data = np.zeros(shape, dtype=np.float64)

    # Accumulate data from all files
    for file in cube_files:
        data = read_cube_data(file, shape)
        if data.shape != shape:
            raise ValueError(f"Grid shape mismatch in file {file}. Expected {shape}, got {data.shape}")
        summed_data += data

    # Write the output sum cube file
    with open(output_file, 'w') as f:
        f.write(f"Summed Cube File generated via Python script\n")
        f.write(f"Sum of {len(cube_files)} input cube files\n")
        
        # Line 3: Natoms, Origin
        f.write(f"{natoms:5d} {origin[0]:12.6f} {origin[1]:12.6f} {origin[2]:12.6f}\n")
        
        # Lines 4-6: Grid dimensions and voxel vectors
        for g in grid_info:
            f.write(f"{g['n']:5d} {g['vec'][0]:12.6f} {g['vec'][1]:12.6f} {g['vec'][2]:12.6f}\n")
            
        # Atomic coordinate section
        for atom in atoms:
            f.write(f"{atom['atomic_num']:5d} {atom['charge']:12.6f} "
                    f"{atom['pos'][0]:12.6f} {atom['pos'][1]:12.6f} {atom['pos'][2]:12.6f}\n")
            
        # Volumetric data output formatted in 6 columns (standard format)
        flat_data = summed_data.flatten()
        for i, val in enumerate(flat_data):
            f.write(f" {val:13.5E}")
            if (i + 1) % 6 == 0:
                f.write("\n")
        if len(flat_data) % 6 != 0:
            f.write("\n")

    print(f"\nSuccessfully written summed cube file to: '{output_file}'")


# --- Execution Configuration ---
if __name__ == "__main__":
    # Directory containing your .cube files
    input_folder = "."  # Change to your folder path
    
    # Output file path
    output_cube = "summed_output.cube"

    # Run the summation
    sum_cube_files(input_folder, output_cube)