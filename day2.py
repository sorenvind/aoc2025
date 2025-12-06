#!/usr/bin/env python3
"""
day2.py

Plumbing for parsing comma-separated number ranges from a single input line
and a placeholder to compute "invalid IDs" for each range.

Usage:
  python3 day2.py [input_file]

If no file is given the script reads `day2-input.txt` in the project root.
"""

from __future__ import annotations

from pathlib import Path
import sys
import re
from typing import List, Tuple


def parse_ranges(line: str) -> List[Tuple[int, int]]:
    """Parse a single line containing comma-separated ranges like "10-20,94-1145".

    Returns a list of (start, end) inclusive integer ranges.
    Raises ValueError for malformed tokens.
    """
    tokens = [tok.strip() for tok in line.split(",") if tok.strip()]
    pattern = re.compile(r"^(\d+)-(\d+)$")
    ranges: List[Tuple[int, int]] = []
    for tok in tokens:
        m = pattern.match(tok)
        if not m:
            raise ValueError(f"Invalid range token: {tok!r}")
        start = int(m.group(1))
        end = int(m.group(2))
        if start > end:
            raise ValueError(f"Range start greater than end: {tok!r}")
        ranges.append((start, end))
    return ranges


def compute_invalid_ids(rng: Tuple[int, int]) -> List[int]:
    """Compute invalid IDs for the given (start, end) inclusive range.

    An ID is invalid if:
    - it starts with '0', or
    - it is composed of two equal halves (e.g. '1212' -> '12'+'12').

    This function iterates the inclusive integer range [start, end], checks
    each ID (as a string) for the invalid conditions, collects and returns
    the list of invalid integer IDs.
    """
    start, end = rng
    if start > end:
        return []

    invalid: List[int] = []
    for n in range(start, end + 1):
        s = str(n)
        # starts with '0'
        if s.startswith("0"):
            invalid.append(n)
            continue

        # repeated pattern: only consider even-length strings
        if len(s) % 2 == 0:
            half = len(s) // 2
            if s[:half] == s[half:]:
                invalid.append(n)
                continue

    # print invalid IDs as requested
    if invalid:
        print("Invalid IDs:", invalid)
    else:
        print("Invalid IDs: []")
    return invalid


def main(argv: List[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    input_path = argv[0] if argv else "day2-input.txt"
    p = Path(input_path)
    if not p.exists():
        print(f"Input file {p} not found")
        return

    # Read the first non-empty line
    lines = p.read_text(encoding="utf-8").splitlines()
    line = next((l.strip() for l in lines if l.strip()), "")
    if not line:
        print("No non-empty input line found")
        return

    try:
        ranges = parse_ranges(line)
    except ValueError as exc:
        print(f"Error parsing ranges: {exc}")
        return

    print(f"Parsed {len(ranges)} ranges: {ranges}")

    # Call compute_invalid_ids for each range and accumulate the sum
    total_sum = 0
    for rng in ranges:
        invalid = compute_invalid_ids(rng)
        print(f"Range {rng} -> {len(invalid)} invalid IDs")
        total_sum += sum(invalid)

    # Final output: sum of all invalid IDs
    print(f"Total sum of invalid IDs: {total_sum}")


if __name__ == "__main__":
    main()
