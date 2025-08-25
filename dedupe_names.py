#!/usr/bin/env python3
"""
Deduplicate rows by a user-provided column (e.g., a name column),
normalizing spaces and casing, and export the unique values to a UTF-8 .txt file.

Features:
- Reads CSV/TSV or delimited text via Python's csv module
- Trims leading/trailing spaces and collapses internal multiple spaces
- Optional case-insensitive matching when deduplicating
- Writes output as UTF-8 encoded plain text, one value per line

Usage examples:
  python dedupe_names.py input.csv --column Name --out names.txt
  python dedupe_names.py input.tsv --column 0 --delimiter "\t" --out names.txt
  python dedupe_names.py input.csv --column name --ignore-case --keep-order
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from typing import Iterable, List, Optional, Set, Tuple


def normalize_spaces(text: str) -> str:
    """Strip leading/trailing spaces and collapse consecutive internal whitespace to single spaces."""
    # Replace any run of whitespace characters with a single space, then strip
    # Using split/join avoids importing regex and handles tabs/newlines as well
    return " ".join(text.split()).strip()


def read_values(
    input_path: str,
    column: str,
    delimiter: Optional[str] = None,
    encoding: str = "utf-8",
    has_header: Optional[bool] = None,
) -> Tuple[List[str], List[str]]:
    """
    Read values from a delimited file for the specified column.

    - column: either a header name or a zero-based column index as string
    - delimiter: if not provided, autodetects via csv.Sniffer
    - has_header: if None, attempt to detect header; otherwise force behavior

    Returns (values, header).
    """
    values: List[str] = []
    header: List[str] = []

    with open(input_path, "r", encoding=encoding, newline="") as f:
        sample = f.read(4096)
        f.seek(0)

        # Detect dialect if delimiter not provided
        if delimiter is None:
            try:
                dialect = csv.Sniffer().sniff(sample)
                detected_delimiter = dialect.delimiter
            except Exception:
                detected_delimiter = ","
        else:
            detected_delimiter = delimiter

        # Detect header if not specified
        if has_header is None:
            try:
                has_header = csv.Sniffer().has_header(sample)
            except Exception:
                has_header = True

        reader = csv.reader(f, delimiter=detected_delimiter)
        if has_header:
            try:
                header = next(reader)
            except StopIteration:
                return [], []

        # Resolve column index
        col_index: Optional[int] = None
        if column.isdigit():
            col_index = int(column)
        else:
            if not header:
                raise ValueError(
                    "Column specified by name but no header row detected. Use --no-header or specify index."
                )
            try:
                col_index = header.index(column)
            except ValueError as exc:
                raise ValueError(f"Column '{column}' not found in header: {header}") from exc

        for row in reader:
            if col_index is None or col_index >= len(row):
                # Skip malformed rows
                continue
            values.append(row[col_index])

    return values, header


def dedupe_values(
    values: Iterable[str],
    ignore_case: bool = False,
    keep_order: bool = True,
) -> List[str]:
    """Return de-duplicated values after normalizing spaces. Optionally ignore case and preserve order."""
    seen: Set[str] = set()
    result: List[str] = []

    for value in values:
        if value is None:
            continue
        cleaned = normalize_spaces(value)
        if cleaned == "":
            continue
        key = cleaned.lower() if ignore_case else cleaned
        if key in seen:
            continue
        seen.add(key)
        result.append(cleaned)

    if not keep_order:
        result.sort(key=lambda s: s.lower() if ignore_case else s)

    return result


def write_txt(values: Iterable[str], output_path: str, encoding: str = "utf-8") -> None:
    """Write one value per line to a UTF-8 text file."""
    with open(output_path, "w", encoding=encoding, newline="\n") as f:
        for value in values:
            f.write(f"{value}\n")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Remove repeated names by a chosen column after trimming/collapsing spaces; output UTF-8 txt."
        )
    )
    parser.add_argument("input", help="Path to input CSV/TSV/delimited file")
    parser.add_argument(
        "--column",
        required=True,
        help="Column to use for names. Header name or zero-based index",
    )
    parser.add_argument(
        "--delimiter",
        default=None,
        help="Field delimiter. If omitted, tries to auto-detect (defaults to comma on failure).",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Treat the file as having no header row",
    )
    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Ignore case when deduplicating",
    )
    parser.add_argument(
        "--keep-order",
        action="store_true",
        help="Preserve original order (default). If omitted with --sort, results are sorted",
    )
    parser.add_argument(
        "--sort",
        action="store_true",
        help="Sort output alphabetically (case-insensitive if --ignore-case)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output .txt path. Defaults to <input_basename>_unique.txt",
    )

    args = parser.parse_args(argv)
    return args


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    input_path = args.input
    column = args.column
    delimiter = args.delimiter
    has_header = not args.no_header
    ignore_case = args.ignore_case
    keep_order = not args.sort  # --sort overrides order keeping

    if not os.path.isfile(input_path):
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        values, _ = read_values(
            input_path=input_path,
            column=column,
            delimiter=delimiter,
            has_header=has_header,
        )
    except Exception as exc:
        print(f"Failed to read values: {exc}", file=sys.stderr)
        return 2

    unique_values = dedupe_values(values, ignore_case=ignore_case, keep_order=keep_order)

    output_path = args.out
    if not output_path:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}_unique.txt"

    try:
        write_txt(unique_values, output_path)
    except Exception as exc:
        print(f"Failed to write output: {exc}", file=sys.stderr)
        return 3

    print(f"Wrote {len(unique_values)} unique value(s) to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

