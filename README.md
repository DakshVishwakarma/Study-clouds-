# Duplicate Name Remover and Text Cleaner

A Python script that removes repeated names from a specified column, cleans up unwanted spaces, and converts the output to UTF-8 text format.

## Features

- **Multiple file format support**: CSV, Excel (.xlsx, .xls), and text files
- **Duplicate removal**: Removes repeated names from specified columns
- **Space cleaning**: Removes extra spaces and normalizes whitespace
- **UTF-8 output**: Ensures proper encoding for international characters
- **Interactive interface**: User-friendly command-line interface

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Mode (Recommended)
```bash
python remove_duplicates.py
```

The script will prompt you for:
- Input file path
- Column name to process
- Output file path (optional)

### Example Session
```
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

### CSV Files
- Standard comma-separated values
- UTF-8 encoding recommended
- First row should contain column headers

### Excel Files
- Supports .xlsx and .xls formats
- First row should contain column headers

### Text Files
- Plain text with one entry per line
- Or CSV format without headers

## Output

The script generates a UTF-8 encoded text file with:
- One cleaned name per line
- No duplicate entries
- Normalized spacing
- Empty lines removed

## Example

**Input (example_data.csv):**
```csv
name,age,city
John Doe,25,New York
Jane Smith,30,Los Angeles
John Doe,25,New York
Bob Johnson,35,Chicago
Jane Smith,30,Los Angeles
Alice Brown,28,Boston
  John Doe  ,25,New York
Bob Johnson,35,Chicago
```

**Output (example_data_cleaned.txt):**
```
John Doe
Jane Smith
Bob Johnson
Alice Brown
```

## Error Handling

The script includes comprehensive error handling for:
- File not found
- Invalid file formats
- Missing columns
- Encoding issues
- Processing errors

## Dependencies

- `pandas`: Data manipulation and analysis
- `openpyxl`: Excel file reading (.xlsx)
- `xlrd`: Excel file reading (.xls)

## License

This script is provided as-is for educational and practical use. 
