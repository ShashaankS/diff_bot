#!/usr/bin/env python3

import os
import sys
import subprocess

def convert_xacro_to_sdf(xacro_file, sdf_file):
    """
    Converts a .xacro file to an .sdf file.

    Args:
        xacro_file (str): Path to the input .xacro file.
        sdf_file (str): Path to the output .sdf file.
    """
    try:
        # Check if the xacro file exists
        if not os.path.exists(xacro_file):
            raise FileNotFoundError(f"Xacro file '{xacro_file}' does not exist.")

        # Generate a temporary URDF file
        urdf_file = xacro_file.replace(".xacro", ".urdf")
        
        # Convert xacro to URDF
        subprocess.run(f"xacro {xacro_file} > {urdf_file}", shell=True, check=True)
        # print(f"Converted Xacro to URDF: {urdf_file}")

        # Convert URDF to SDF
        subprocess.run(f"gz sdf -p {urdf_file} > {sdf_file}", shell=True, check=True)
        # print(f"Converted URDF to SDF: {sdf_file}")
        print(f"Converted XACRO to SDF: {sdf_file}")

        # Clean up the temporary URDF file
        if os.path.exists(urdf_file):
            os.remove(urdf_file)
            # print(f"Deleted temporary URDF file: {urdf_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 convert_xacro_to_sdf.py <input_xacro_file> <output_sdf_file>")
        sys.exit(1)

    xacro_file = sys.argv[1]
    sdf_file = sys.argv[2]

    convert_xacro_to_sdf(xacro_file, sdf_file)
