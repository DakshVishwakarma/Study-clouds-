# Duplicate Name Remover and Text Cleaner

A Python script that removes duplicate names from a specified column, cleans up unwanted spaces, and converts the output to UTF-8 text format.

## Features

- **Multi-format support**: Works with CSV, Excel (.xlsx, .xls), and text files
- **Duplicate removal**: Removes repeated names while keeping the first occurrence
- **Space cleaning**: Removes extra spaces and normalizes whitespace
- **UTF-8 output**: Ensures proper encoding for international characters
- **Interactive interface**: User-friendly command-line interface

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Mode
Run the script and follow the prompts:
```bash
python remove_duplicates.py
```

The script will ask for:
1. Input file path
2. Column name to process
3. Output file path (optional)

### Example
```bash
$ python remove_duplicates.py
=== Duplicate Name Remover and Text Cleaner ===
This script removes duplicate names, cleans spaces, and converts to UTF-8 text.

Enter the path to your input file (CSV, Excel, or text): example_data.csv
Enter the column name to process: name
Enter output file path (press Enter for default): 

Processing file: example_data.csv
Original data shape: (8, 3)
Processing column: name
After removing duplicates: (4, 3)
Removed 4 duplicate entries
Cleaned data saved to: example_data_cleaned.txt
File encoding: UTF-8

✅ Processing completed successfully!
```

## Input File Formats

- **CSV files**: Standard comma-separated values
- **Excel files**: .xlsx and .xls formats
- **Text files**: Plain text files (will be treated as single column)

## Output

The script generates a UTF-8 encoded text file with:
- One cleaned name per line
- No duplicate entries
- Normalized spacing
- Proper UTF-8 encoding

## Example Data

The `example_data.csv` file contains sample data with duplicates:
- Original: 8 rows with 4 duplicate names
- After processing: 4 unique names

## Error Handling

The script includes comprehensive error handling for:
- File not found
- Invalid column names
- Unsupported file formats
- Encoding issues
- Data processing errors

## Dependencies

- pandas: Data manipulation and analysis
- openpyxl: Excel file reading
- xlrd: Legacy Excel file support 
