#!/usr/bin/env python3
"""
day3.py

Process battery bank lines from a file. For each line (a string of digits):
- Find the largest digit in the string from the start up to the second-last digit (prefix max).
- Find the largest digit after that prefix position (suffix max).
- Return the two digits concatenated as a string (e.g., '98').

Usage:
  python3 day3.py [input_file]

If no file is given the script uses `day3-sample.txt`.
"""

from __future__ import annotations
from pathlib import Path
import sys
from typing import List


def process_bank(bank: str) -> str:
    """Given a digit string `bank`, return the two-digit result as described.

    The first digit is the maximum digit found from index 0 up to index len(bank)-2
    (inclusive). The second digit is the maximum digit found strictly after that
    first-digit position (i.e., from first_pos+1 to end).

    Returns a two-character string containing the two digits.
    """
    if len(bank) < 2:
        raise ValueError("bank string must have at least 2 digits")

    # find max digit and its first occurrence in prefix (0..len-2)
    prefix = bank[: len(bank) - 1]
    max_prefix = max(prefix)
    first_pos = prefix.index(max_prefix)

    # suffix is everything after first_pos
    suffix = bank[first_pos + 1 :]
    if not suffix:
        raise ValueError("no suffix after chosen prefix position")
    max_suffix = max(suffix)

    return f"{max_prefix}{max_suffix}"


def main(argv: List[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    input_path = argv[0] if argv else "day3-sample.txt"
    p = Path(input_path)
    if not p.exists():
        print(f"Input file {p} not found")
        return

    lines = [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    results = []
    for l in lines:
        res = process_bank(l)
        print(res)
        results.append(res)

    # Final output: sum of all returned results interpreted as integers
    int_sum = sum(int(r) for r in results)
    print(int_sum)
    # also return results (useful for tests)
    return results


if __name__ == "__main__":
    main()
