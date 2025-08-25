#!/usr/bin/env python3
"""
Simple script to remove repeated names from a specified column, clean up spaces, and convert to UTF-8 text.
Uses only Python standard library - no external dependencies required.
"""

import csv
import sys
import os
from pathlib import Path

def clean_text(text):
    """Clean text by removing extra spaces and normalizing whitespace."""
    if text is None:
        return ""
    # Convert to string, remove extra spaces, and normalize
    cleaned = str(text).strip()
    # Replace multiple spaces with single space
    cleaned = ' '.join(cleaned.split())
    return cleaned

def read_csv_file(file_path):
    """Read CSV file and return data as list of dictionaries."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            print(f"Error reading file with latin-1 encoding: {str(e)}")
            return None

def read_text_file(file_path):
    """Read text file and return as list of dictionaries with a single column."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.strip():  # Skip empty lines
                    data.append({'content': line.strip()})
        return data
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if line.strip():  # Skip empty lines
                        data.append({'content': line.strip()})
            return data
        except Exception as e:
            print(f"Error reading file with latin-1 encoding: {str(e)}")
            return None

def remove_duplicates_and_clean(input_file, column_name, output_file=None):
    """
    Remove duplicate names from specified column, clean spaces, and save as UTF-8 text.
    
    Args:
        input_file (str): Path to input file (CSV or text)
        column_name (str): Name of the column to process
        output_file (str): Path to output file (optional)
    """
    try:
        # Determine file type and read accordingly
        file_extension = Path(input_file).suffix.lower()
        
        if file_extension == '.csv':
            data = read_csv_file(input_file)
            if data is None:
                return False
        elif file_extension == '.txt':
            data = read_text_file(input_file)
            if data is None:
                return False
            # For text files, use 'content' as the column name
            column_name = 'content'
        else:
            print(f"Unsupported file format: {file_extension}")
            print("Supported formats: .csv, .txt")
            return False
        
        if not data:
            print("No data found in the file.")
            return False
        
        # Check if column exists
        if column_name not in data[0]:
            print(f"Column '{column_name}' not found in the file.")
            print(f"Available columns: {list(data[0].keys())}")
            return False
        
        print(f"Original data count: {len(data)}")
        print(f"Processing column: {column_name}")
        
        # Clean the specified column and collect unique values
        unique_values = set()
        cleaned_data = []
        
        for row in data:
            value = row[column_name]
            cleaned_value = clean_text(value)
            
            if cleaned_value and cleaned_value not in unique_values:
                unique_values.add(cleaned_value)
                cleaned_data.append(cleaned_value)
        
        print(f"After removing duplicates: {len(cleaned_data)}")
        print(f"Removed {len(data) - len(cleaned_data)} duplicate entries")
        
        # Generate output filename if not provided
        if output_file is None:
            base_name = Path(input_file).stem
            output_file = f"{base_name}_cleaned.txt"
        
        # Save as UTF-8 text file
        with open(output_file, 'w', encoding='utf-8') as f:
            for value in cleaned_data:
                f.write(f"{value}\n")
        
        print(f"Cleaned data saved to: {output_file}")
        print(f"File encoding: UTF-8")
        
        return True
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False

def main():
    """Main function to handle user input and execute the script."""
    print("=== Simple Duplicate Name Remover and Text Cleaner ===")
    print("This script removes duplicate names, cleans spaces, and converts to UTF-8 text.")
    print("No external dependencies required - uses only Python standard library.\n")
    
    # Get input file
    while True:
        input_file = input("Enter the path to your input file (CSV or text): ").strip()
        if os.path.exists(input_file):
            break
        print("File not found. Please enter a valid file path.")
    
    # Get column name
    column_name = input("Enter the column name to process: ").strip()
    
    # Get output file (optional)
    output_file = input("Enter output file path (press Enter for default): ").strip()
    if not output_file:
        output_file = None
    
    # Process the file
    print(f"\nProcessing file: {input_file}")
    success = remove_duplicates_and_clean(input_file, column_name, output_file)
    
    if success:
        print("\n✅ Processing completed successfully!")
    else:
        print("\n❌ Processing failed. Please check the error messages above.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)