# Usage Guide for Duplicate Name Remover Script

## Quick Start

1. **Run the script:**
   ```bash
   python3 remove_duplicates_simple.py
   ```

2. **Follow the prompts:**
   - Enter input file path
   - Enter column name
   - Enter output file path (optional)

## Examples

### Example 1: Processing CSV File

**Input file (example_data.csv):**
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

**Command:**
```bash
echo -e "example_data.csv\nname\n" | python3 remove_duplicates_simple.py
```

**Output (example_data_cleaned.txt):**
```
John Doe
Jane Smith
Bob Johnson
Alice Brown
```

### Example 2: Processing Text File

**Input file (example_names.txt):**
```
John Doe
Jane Smith
  John Doe  
Bob Johnson
Jane Smith
Alice Brown
  Bob Johnson  
```

**Command:**
```bash
echo -e "example_names.txt\ncontent\n" | python3 remove_duplicates_simple.py
```

**Output (example_names_cleaned.txt):**
```
John Doe
Jane Smith
Bob Johnson
Alice Brown
```

## Supported File Formats

### CSV Files (.csv)
- Must have column headers in first row
- Specify the exact column name as it appears in the header
- UTF-8 encoding recommended

### Text Files (.txt)
- One entry per line
- Column name will automatically be set to 'content'
- UTF-8 encoding recommended

## Features

✅ **Duplicate Removal**: Removes repeated entries based on the specified column
✅ **Space Cleaning**: Removes extra spaces and normalizes whitespace
✅ **UTF-8 Output**: Ensures proper encoding for international characters
✅ **No Dependencies**: Uses only Python standard library
✅ **Error Handling**: Comprehensive error messages and validation
✅ **Flexible Input**: Supports multiple file formats

## Troubleshooting

### Common Issues

1. **"File not found"**
   - Check the file path is correct
   - Ensure the file exists in the current directory
   - Use absolute path if needed

2. **"Column not found"**
   - Check the exact column name (case-sensitive)
   - For CSV files, verify the header row
   - For text files, use 'content' as column name

3. **"No data found"**
   - Ensure the file is not empty
   - Check file encoding (try UTF-8 or Latin-1)
   - Verify file format is supported

4. **Encoding Issues**
   - The script automatically tries UTF-8 first
   - Falls back to Latin-1 if UTF-8 fails
   - Ensure your input file uses a supported encoding

### File Encoding Tips

- **UTF-8**: Best for international characters
- **Latin-1**: Fallback for older files
- **Avoid**: Special encodings that may cause issues

## Advanced Usage

### Batch Processing

You can process multiple files by creating a simple script:

```bash
#!/bin/bash
files=("file1.csv" "file2.csv" "file3.csv")
column="name"

for file in "${files[@]}"; do
    echo "Processing $file..."
    echo -e "$file\n$column\n" | python3 remove_duplicates_simple.py
done
```

### Non-Interactive Mode

For automation, you can pipe input directly:

```bash
echo -e "input.csv\ncolumn_name\noutput.txt" | python3 remove_duplicates_simple.py
```

## Output Format

The script generates a clean text file with:
- One entry per line
- No duplicate entries
- Normalized spacing
- UTF-8 encoding
- Empty lines removed

## Performance

- **Small files** (< 1MB): Near-instant processing
- **Medium files** (1-10MB): Seconds to process
- **Large files** (> 10MB): May take longer, consider splitting

## Limitations

- Only supports CSV and text files
- No Excel file support (use CSV export instead)
- Column-based duplicate removal only
- No advanced data validation

## Support

If you encounter issues:
1. Check the error messages carefully
2. Verify file format and encoding
3. Ensure column names match exactly
4. Test with a simple example file first