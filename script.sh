#!/bin/bash

source_scripts="/uufs/chpc.utah.edu/common/home/u1191173/summer_research/interface"
current_directory=$(pwd)
tmp_directory="$current_directory/tmp"
file_names="$tmp_directory/file_names.txt"

# Create temporary directory
mkdir -p "$tmp_directory"

# Run Python script
cd "$source_scripts" || exit
python interface.py "$current_directory"
cd "$tmp_directory" || exit

# Check if file_names.txt exists
if [ -f "$file_names" ]; then
    # Read file names from file_names.txt
    files=()
    while IFS= read -r line; do
        files+=("$line")
    done < "$file_names"

    # Process each file
    for file in "${files[@]}"; do
        base_file=$(basename "$file")
        python "$source_scripts/slurm_edit.py" "$current_directory" "$base_file"
	cd "$tmp_directory"
        sbatch g16_slurm.scr
    done
    
    # Move output files to parent directory
    cd "$tmp_directory"
    mv *.out* ..
else
    echo "No calculations were submitted because file_names.txt did not exist."
fi

# Clean up temporary directory
cd "$current_directory" || exit
rm -rf "$tmp_directory"
