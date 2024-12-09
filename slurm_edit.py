"""
Connor Vardakis
Purpose:
    This program serves to edit the slurm script for each calculation

Version 0.1.0 RC
 - Created remove_file_extension to remove the extention off of submitted file
 - Defined constants for the template, slurm script location, directory, and file
 - Main function defined to read template and generate new g16 file to submit calculation
"""

import os.path
import sys

# CONSTANTS
TEMPLATES_SLURM = "/uufs/chpc.utah.edu/common/home/u1191173/summer_research/interface/templates/slurm_template.scr"
DIRECTORY = sys.argv[1]
TMP_DIRECTORY = DIRECTORY + "/tmp"
SLURM_LOCATION = os.path.join(TMP_DIRECTORY, "g16_slurm.scr")
FILE = sys.argv[2]


def main():
    slurm = open(TEMPLATES_SLURM, "r")

    g16_file = open(SLURM_LOCATION, "w")
    for line in slurm:
        g16_file.write(line)
    g16_file.close()

    print("Submitting Calculation for: " + FILE)
    time = input("Provide duration for calculation in form of HH:MM:SS\n")

    g16_file = open(SLURM_LOCATION, "r")
    g16_content = g16_file.read()

    g16_content = g16_content.replace("TIME", time)
    g16_content = g16_content.replace("DIRECTORY", DIRECTORY)
    g16_content = g16_content.replace("CALCULATION", remove_file_extension(FILE))

    os.remove(SLURM_LOCATION)

    g16_file = open(SLURM_LOCATION, "w")
    g16_file.write(g16_content)


def remove_file_extension(file_name):
    file_name, _ = os.path.splitext(file_name)
    return file_name

if __name__ == "__main__":
    main()

