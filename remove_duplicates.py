#!/usr/bin/env python3
"""remove_duplicates.py

A utility script to extract unique names from a column in a delimited text file
(CSV/TSV/etc.), remove redundant whitespace, and save the result to a UTF-8
encoded plain-text file.

Usage
-----
$ python remove_duplicates.py input.csv --column 0 --delimiter "," -o unique_names.txt

Arguments
~~~~~~~~~
 positional:
    input_path           Path to the input delimited text file (e.g., CSV).
 optional:
    -c, --column         Column index (0-based) OR column header/field name
                         containing the names. Required.
    -d, --delimiter      Field delimiter for the input file. Default is ','.
    -o, --output         Output .txt file path. Default <input>_unique.txt
    -q, --quotechar      Quote character used in the CSV. Default '"'.
    --lowercase          Deduplicate ignoring case (converts to lower case).
    --strip-internal     Also collapse multiple internal spaces to a single
                         space (default just strips leading/trailing).

The resulting text file will be encoded as UTF-8 with one unique name per line.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable, List, Set, Union


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract unique names from a column, strip whitespace, and save to UTF-8 .txt",
    )
    parser.add_argument("input_path", type=Path, help="Path to the input CSV/TSV file.")
    parser.add_argument(
        "-c",
        "--column",
        required=True,
        help="Column index (0-based) or column header containing the names.",
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        default=",",
        help="Field delimiter used in the input file (default ',').",
    )
    parser.add_argument(
        "-q",
        "--quotechar",
        default="\"",
        help="Quote character used in the CSV (default '"').",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output .txt file path (default: <input>_unique.txt).",
    )
    parser.add_argument(
        "--lowercase",
        action="store_true",
        help="Treat names case-insensitively when deduplicating (convert to lower case).",
    )
    parser.add_argument(
        "--strip-internal",
        action="store_true",
        help="Reduce multiple internal spaces to a single space as well.",
    )

    return parser.parse_args(argv)


def normalise_name(name: str, *, lowercase: bool = False, strip_internal: bool = False) -> str:
    """Strip whitespace and optionally collapse internal spaces and lowercase."""
    name = name.strip()
    if strip_internal:
        # Collapse runs of whitespace inside the string to a single space
        name = " ".join(name.split())
    if lowercase:
        name = name.lower()
    return name


def extract_unique_names(
    input_file: Path,
    column: Union[int, str],
    *,
    delimiter: str = ",",
    quotechar: str = "\"",
    lowercase: bool = False,
    strip_internal: bool = False,
) -> List[str]:
    """Read *input_file* and return unique normalised names from *column*."""
    unique: Set[str] = set()
    output: List[str] = []

    with input_file.open("r", newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
        header_row: List[str] | None = None
        idx: int | None = None

        # Determine index if column is header string
        if isinstance(column, str) and not column.isdigit():
            try:
                header_row = next(reader)
            except StopIteration:
                return []
            try:
                idx = header_row.index(column)
            except ValueError:
                raise SystemExit(
                    f"Column header '{column}' not found in file {input_file}. Headers: {header_row}"
                )
        else:
            idx = int(column)

        # If we already consumed header (when column is header string), reuse reader for remaining rows
        if header_row is not None:
            row_iter = reader  # already positioned after header
        else:
            row_iter = reader

        for row_number, row in enumerate(row_iter, start=(2 if header_row else 1)):
            if idx >= len(row):
                # Warn and skip rows that don't have the expected column
                sys.stderr.write(
                    f"Warning: row {row_number} has only {len(row)} columns; expected index {idx}. Skipped.\n"
                )
                continue
            raw_name = row[idx]
            name = normalise_name(raw_name, lowercase=lowercase, strip_internal=strip_internal)
            if name and name not in unique:
                unique.add(name)
                output.append(raw_name.strip())  # Preserve original spacing except leading/trailing

    return output


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)

    column = args.column
    try:
        # Allow numeric strings for column index
        column = int(column) if str(column).isdigit() else column
    except ValueError:
        pass  # keep as string

    output_path: Path = args.output or args.input_path.with_suffix("_unique.txt")

    names = extract_unique_names(
        args.input_path,
        column,
        delimiter=args.delimiter,
        quotechar=args.quotechar,
        lowercase=args.lowercase,
        strip_internal=args.strip_internal,
    )

    # Write to output as UTF-8, one per line
    with output_path.open("w", encoding="utf-8", newline="\n") as out:
        for name in names:
            out.write(f"{name}\n")

    print(f"Saved {len(names)} unique name(s) to {output_path}")


if __name__ == "__main__":
    main()