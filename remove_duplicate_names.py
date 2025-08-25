#!/usr/bin/env python3
"""
Script to remove duplicate names from a specified column and clean unwanted spaces.
Converts output to UTF-8 text format.
"""

import pandas as pd
import sys
import os
from pathlib import Path


def clean_text(text):
    """
    Clean text by removing leading/trailing whitespace and extra spaces.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    if pd.isna(text) or text is None:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Remove leading/trailing whitespace and replace multiple spaces with single space
    cleaned = ' '.join(text.strip().split())
    
    return cleaned


def get_file_extension(filepath):
    """Get file extension in lowercase."""
    return Path(filepath).suffix.lower()


def read_data_file(filepath):
    """
    Read data file based on its extension.
    
    Args:
        filepath (str): Path to the input file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    extension = get_file_extension(filepath)
    
    try:
        if extension == '.csv':
            return pd.read_csv(filepath, encoding='utf-8')
        elif extension in ['.xlsx', '.xls']:
            return pd.read_excel(filepath)
        elif extension == '.tsv':
            return pd.read_csv(filepath, sep='\t', encoding='utf-8')
        elif extension == '.txt':
            # Try to detect delimiter
            with open(filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if '\t' in first_line:
                    return pd.read_csv(filepath, sep='\t', encoding='utf-8')
                elif ',' in first_line:
                    return pd.read_csv(filepath, encoding='utf-8')
                else:
                    # Assume single column
                    return pd.read_csv(filepath, header=None, names=['data'], encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file format: {extension}")
            
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def process_column(df, column_name):
    """
    Process the specified column to remove duplicates and clean spaces.
    
    Args:
        df (pd.DataFrame): Input dataframe
        column_name (str): Name of the column to process
        
    Returns:
        list: List of unique, cleaned names
    """
    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in the data.")
        print(f"Available columns: {', '.join(df.columns.tolist())}")
        sys.exit(1)
    
    # Extract the column and clean the text
    column_data = df[column_name].astype(str)
    
    # Clean spaces and remove empty entries
    cleaned_data = [clean_text(name) for name in column_data if clean_text(name)]
    
    # Remove duplicates while preserving order
    unique_names = []
    seen = set()
    
    for name in cleaned_data:
        # Case-insensitive duplicate check
        name_lower = name.lower()
        if name_lower not in seen:
            seen.add(name_lower)
            unique_names.append(name)
    
    return unique_names


def save_to_utf8_text(data, output_filepath):
    """
    Save data to UTF-8 text file.
    
    Args:
        data (list): List of strings to save
        output_filepath (str): Output file path
    """
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(f"{item}\n")
        print(f"Successfully saved {len(data)} unique names to '{output_filepath}'")
    except Exception as e:
        print(f"Error saving file: {e}")
        sys.exit(1)


def main():
    """Main function to execute the script."""
    print("=== Duplicate Name Remover ===")
    print("This script removes duplicate names from a specified column and saves to UTF-8 text format.\n")
    
    # Get input file path
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = input("Enter the path to your input file: ").strip()
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    # Read the data
    print(f"Reading data from '{input_file}'...")
    df = read_data_file(input_file)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    
    # Display available columns
    print(f"\nAvailable columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    # Get column name from user
    if len(sys.argv) > 2:
        column_name = sys.argv[2]
    else:
        column_input = input("\nEnter the column name or number: ").strip()
        
        # Check if input is a number
        if column_input.isdigit():
            col_num = int(column_input) - 1
            if 0 <= col_num < len(df.columns):
                column_name = df.columns[col_num]
            else:
                print(f"Error: Invalid column number. Please choose between 1 and {len(df.columns)}.")
                sys.exit(1)
        else:
            column_name = column_input
    
    # Process the column
    print(f"\nProcessing column '{column_name}'...")
    unique_names = process_column(df, column_name)
    
    print(f"Found {len(unique_names)} unique names after removing duplicates and cleaning spaces.")
    
    # Get output file path
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
    else:
        default_output = f"unique_names_{column_name.replace(' ', '_').lower()}.txt"
        output_file = input(f"Enter output file path (default: {default_output}): ").strip()
        if not output_file:
            output_file = default_output
    
    # Save to UTF-8 text file
    save_to_utf8_text(unique_names, output_file)
    
    # Display summary
    print(f"\n=== Summary ===")
    print(f"Input file: {input_file}")
    print(f"Column processed: {column_name}")
    print(f"Original entries: {len(df[column_name])}")
    print(f"Unique entries: {len(unique_names)}")
    print(f"Output file: {output_file}")
    print("Encoding: UTF-8")


if __name__ == "__main__":
    main()