# List_pngs.sh - Auto-updated documentation
# Author: Charles Bucher
# Description: Add description here

#!/bin/bash

# Script to list all .png files in a repository
# Usage: ./list_pngs.sh [directory_path]
# If no directory is specified, it searches the current directory

# Set the search directory (use provided argument or current directory)
SEARCH_DIR="${1:-.}"

# Check if directory exists
if [ ! -d "$SEARCH_DIR" ]; then
    echo "Error: Directory '$SEARCH_DIR' does not exist"
    exit 1
fi

echo "Searching for PNG files in: $SEARCH_DIR"
echo "----------------------------------------"

# Find and list all .png files
find "$SEARCH_DIR" -type f -iname "*.png" | while read -r file; do
    echo "$file"
done

# Count total PNG files found
total=$(find "$SEARCH_DIR" -type f -iname "*.png" | wc -l)
echo "----------------------------------------"
echo "Total PNG files found: $total"