"""
Connor Vardakis
Version 0.3.0
 - Restructured interface so source file and input file are requested at the beginning of the file
 - Reinstated check for file overwriting
 - Created tmp_file function to write names to each file

Version 0.2.3 RC
 - Fixed reference issue with OUTPUT_FILE constant
  
Version 0.2.2
 - Added proper loop for if two calculations want to be submitted at once
 - Added array for output file so slrm script can iterate through

Version 0.2.1
 - Cleaned up formatting on input commands
 - Altered pe_last_line for cleaner user experience
 - Corrected write_file function to support potential energy scans
 - Removed old hardcoded file generation

Version 0.2.0
 - Created template_reader function to pull files from templates instead of having scripts hardcoded into program
 - Manipulated main to incorporate template_reader
 - Created write_file to generate output files
 - Added os file check for existing files for overwriting purposes
 - Added termination support at each input location
 - Defined constants for templates

Version 0.1.1
 - Repairs command line input

Version 0.1.0
- This version is ready for initial testing
- Builds foundation for coordinate extraction
- Builds foundation for file building for calculation
- Builds foundation for text based interface for file selection
"""

import sys
import os.path

# CONSTANTS
TEMPLATES_DIRECTORY = "/uufs/chpc.utah.edu/common/home/u1191173/summer_research/interface/templates/"
TEMPLATES = ["geomopt.com", "pe_scan.com", "ts_calc.com", "irc_calc.com"]
DIRECTORY = str(sys.argv[1])


def main():
    # Inside the main file the text interface is executed
    print("The program may be terminated at any time by submitting Q as a response.")
    source = input("Please provide the source coordinate file with file extension: ")
    if source.upper() == "Q":
        exit()
    source_file = DIRECTORY + "/" + source
    if os.path.isfile(source_file):
        pass
    else:
        print("ERROR: Source file could not be located.")

    coordinates = extract_coordinate(source_file)
    first_pass = True
    generated_files = []
    while True:
        if not first_pass:
            proceed = input("Would you like to submit another calculation using these coordinates? [Y][N]\n")
            if proceed.upper() == "Y":
                pass
            elif proceed.upper() == "N":
                tmp_file(generated_files)
                exit()

        file_name = input("Input the new file name including extension\n")
        new_file = str(sys.argv[1]) + "/" + file_name
        output_file = new_file
        if os.path.isfile(output_file):
            selection = input(
                "This file " + output_file + " already exits. Proceeding will overwrite this file. Continue? [Y][N]\n")
            if selection.upper() == "Y":
                os.remove(output_file)
            else:
                print("ERROR: OUTPUT FILE ALREADY EXISTS")
                exit()

        selection = input("""Which calculation would you like to submit?\n A) Geometry Optimization 
 B) Potential Energy Scan \n C) Transition State Calculation\n D) Intrinsic Reaction Coordinate\n""")

        if selection.upper() == "A":
            template = template_reader(0)
            write_file(output_file, template, coordinates, False)
            generated_files.append(output_file)
            first_pass = False
        elif selection.upper() == "B":
            template = template_reader(1)
            write_file(output_file, template, coordinates, True)
            generated_files.append(output_file)
            first_pass = False
        elif selection.upper() == "C":
            template = template_reader(2)
            write_file(output_file, template, coordinates, False)
            generated_files.append(output_file)
            first_pass = False
        elif selection.upper() == "D":
            template = template_reader(3)
            write_file(output_file, template, coordinates, False)
            generated_files.append(output_file)
            first_pass = False
        elif selection.upper() == "Q":
            exit()
        else:
            print("Invalid input\n")


def extract_coordinate(input_file):
    coordinates = []
    coords = False
    # /Users/connorvardakis/Documents/coordinates.txt
    if os.path.isfile(input_file):
        docu = open(input_file, "r")
        for line in docu.readlines():
            if coords is True and line == "\n":
                break
            if coords is True:
                coordinates.append(line)
            if line == "1 1\n":
                coords = True
                coordinates.append(line)
        docu.close()
        return coordinates
    else:
        print("ERROR: CANNOT LOCATE COORDINATE SOURCE FILE")
        exit()


def template_reader(selection):
    template_location = TEMPLATES_DIRECTORY + TEMPLATES[selection]
    if os.path.isfile(template_location):
        template = open(template_location, "r")
        template_content = template.readlines()
        template.close()
        return template_content
    else:
        print("ERROR: CANNOT LOCATE TEMPLATE FILE")
        exit()


def write_file(file, template, coordinates, pe_scan):
    results = open(file, "w")
    if pe_scan:
        last_line = pe_last_line()
        for line in template:
            if "CONTENT" in line:
                for point in coordinates:
                    results.write(point)

                results.write("\n" + last_line)

            else:
                results.write(line)

    else:
        for line in template:
            if "CONTENT" in line:
                for point in coordinates:
                    results.write(point)

            else:
                results.write(line)

    results.close()


def pe_last_line():
    scan_type = None
    while True:
        selection = input("Which type of scan\n A) Dihedral Angle; 4 atoms\n B) Bond Length; 2 atoms\n")
        if selection.upper() == "A":
            scan_type = "D"
        elif selection.upper() == "B":
            scan_type = "B"
        elif selection.upper() == "Q":
            exit()
        else:
            print("Invalid selection please choose again")

        atoms = input("List out the atoms you are manipulating using spaces in between the number. ex 1 2 or 4 5 2 1\n")
        steps = input("Please provide the number of steps.\n")
        step_length = input("Please provide the step length.\n")

        last_line = scan_type + " " + atoms + " S " + steps + " " + step_length

        submission = input(
            f"This is what the final line of your PE scan will look like:\n" + last_line + "\nDoes this look correct?[Y][N]\n")
        if submission.upper() == "Y":
            return last_line
        elif submission.upper() == "N":
            continue
        elif submission.upper() == "Q":
            print("Program Terminated")
            exit()


def tmp_file(files):
    tmp_directory = DIRECTORY + "/tmp"
    file_path = os.path.join(tmp_directory, "file_names.txt")
    file_names = open(file_path, "w")
    for file in files:
        file_names.write(file + "\n")


if __name__ == "__main__":
    main()
