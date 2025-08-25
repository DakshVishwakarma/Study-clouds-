# Duplicate Name Remover

A Python script that removes duplicate names from a specified column in data files and cleans unwanted spaces before converting to UTF-8 text format.

## Features

- **Multiple file format support**: CSV, Excel (.xlsx, .xls), TSV, and TXT files
- **Duplicate removal**: Removes duplicate names (case-insensitive)
- **Space cleaning**: Removes leading/trailing whitespace and extra spaces between words
- **UTF-8 output**: Saves cleaned, unique names to UTF-8 encoded text file
- **Interactive mode**: Prompts user for input if not provided via command line
- **Command line support**: Can be run with arguments for automation

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode
```bash
python remove_duplicate_names.py
```
The script will prompt you for:
- Input file path
- Column name or number to process
- Output file path (optional, uses default if not specified)

### Command Line Mode
```bash
python remove_duplicate_names.py <input_file> <column_name> [output_file]
```

**Examples:**
```bash
# Process "Name" column from data.csv
python remove_duplicate_names.py data.csv "Name"

# Process column 1 from users.xlsx and save to clean_names.txt
python remove_duplicate_names.py users.xlsx 1 clean_names.txt

# Process "Full Name" column from contacts.tsv
python remove_duplicate_names.py contacts.tsv "Full Name" unique_contacts.txt
```

## Input File Formats

- **CSV files** (`.csv`): Comma-separated values
- **Excel files** (`.xlsx`, `.xls`): Microsoft Excel format
- **TSV files** (`.tsv`): Tab-separated values
- **Text files** (`.txt`): Auto-detects delimiter (comma or tab)

## What the Script Does

1. **Reads** your input file and displays available columns
2. **Cleans** the specified column by:
   - Removing leading and trailing whitespace
   - Replacing multiple consecutive spaces with single spaces
   - Converting empty/null values to empty strings
3. **Removes duplicates** while preserving the order of first occurrence (case-insensitive)
4. **Saves** the unique, cleaned names to a UTF-8 encoded text file

## Example

If your input data contains:
```
  John Doe  
JANE   SMITH
john doe
  Jane Smith  
Bob Johnson
```

The output will be:
```
John Doe
JANE SMITH
Jane Smith
Bob Johnson
```

## Error Handling

- Validates file existence before processing
- Checks if specified column exists in the data
- Provides helpful error messages for unsupported file formats
- Handles encoding issues gracefully

## Output

- Creates a text file with one unique name per line
- Uses UTF-8 encoding for international character support
- Displays summary statistics (original vs. unique count)