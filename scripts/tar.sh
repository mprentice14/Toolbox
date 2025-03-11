#!/bin/bash

# Get list of directories in the current directory (/home/)
dirs=(*/)
dirs=("${dirs[@]%/}")  # Remove trailing slashes from directory names

# Check if there are any directories
if [ ${#dirs[@]} -eq 0 ]; then
    echo "No directories found in /home/"
    exit 1
fi

# Display the menu of directories to choose from
echo "Select a directory to compress:"
select dir in "${dirs[@]}"; do
    if [ -n "$dir" ]; then
        # Compress the selected directory and save the archive in /tmp/
        if tar -cvzf "/tmp/${dir}.tar.gz" "$dir"; then
            echo "Compressed $dir into /tmp/${dir}.tar.gz"
        else
            echo "Failed to compress $dir"
        fi
        break
    else
        echo "Invalid choice. Please select a number from the list."
    fi
done