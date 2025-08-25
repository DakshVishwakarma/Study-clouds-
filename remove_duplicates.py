#!/usr/bin/env python3
"""
Script to remove repeated names from a specified column, clean up spaces, and convert to UTF-8 text.
Supports CSV, Excel, and text files as input.
"""

import pandas as pd
import sys
import os
from pathlib import Path

def clean_text(text):
    """Clean text by removing extra spaces and normalizing whitespace."""
    if pd.isna(text):
        return ""
    # Convert to string, remove extra spaces, and normalize
    cleaned = str(text).strip()
    # Replace multiple spaces with single space
    cleaned = ' '.join(cleaned.split())
    return cleaned

def remove_duplicates_and_clean(input_file, column_name, output_file=None):
    """
    Remove duplicate names from specified column, clean spaces, and save as UTF-8 text.
    
    Args:
        input_file (str): Path to input file (CSV, Excel, or text)
        column_name (str): Name of the column to process
        output_file (str): Path to output file (optional)
    """
    try:
        # Determine file type and read accordingly
        file_extension = Path(input_file).suffix.lower()
        
        if file_extension == '.csv':
            df = pd.read_csv(input_file, encoding='utf-8')
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(input_file)
        elif file_extension == '.txt':
            # Try to read as CSV first, if it fails, read as plain text
            try:
                df = pd.read_csv(input_file, encoding='utf-8')
            except:
                # Read as plain text with one column
                with open(input_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                df = pd.DataFrame({column_name: [line.strip() for line in lines]})
        else:
            print(f"Unsupported file format: {file_extension}")
            return False
        
        # Check if column exists
        if column_name not in df.columns:
            print(f"Column '{column_name}' not found in the file.")
            print(f"Available columns: {list(df.columns)}")
            return False
        
        print(f"Original data shape: {df.shape}")
        print(f"Processing column: {column_name}")
        
        # Clean the specified column
        df[column_name] = df[column_name].apply(clean_text)
        
        # Remove duplicates based on the cleaned column
        df_cleaned = df.drop_duplicates(subset=[column_name], keep='first')
        
        print(f"After removing duplicates: {df_cleaned.shape}")
        print(f"Removed {len(df) - len(df_cleaned)} duplicate entries")
        
        # Generate output filename if not provided
        if output_file is None:
            base_name = Path(input_file).stem
            output_file = f"{base_name}_cleaned.txt"
        
        # Save as UTF-8 text file
        with open(output_file, 'w', encoding='utf-8') as f:
            for value in df_cleaned[column_name]:
                if value:  # Only write non-empty values
                    f.write(f"{value}\n")
        
        print(f"Cleaned data saved to: {output_file}")
        print(f"File encoding: UTF-8")
        
        return True
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False

def main():
    """Main function to handle user input and execute the script."""
    print("=== Duplicate Name Remover and Text Cleaner ===")
    print("This script removes duplicate names, cleans spaces, and converts to UTF-8 text.\n")
    
    # Get input file
    while True:
        input_file = input("Enter the path to your input file (CSV, Excel, or text): ").strip()
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