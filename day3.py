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


def process_bank(bank: str, k: int = 12) -> str:
    """Given a digit string `bank`, select `k` digits greedily and return them as a string.

    Selection rule (greedy): for i in 0..k-1 choose the left-most occurrence of the
    maximum digit in the window bank[start : n - (k - i) + 1], where start is the
    position after the previously chosen digit (initially 0). This ensures there is
    room to pick the remaining digits.

    Returns a string of length `k` containing the selected digits.
    """
    n = len(bank)
    if k <= 0:
        raise ValueError("k must be positive")
    if n < k:
        raise ValueError(f"bank string must have at least {k} digits")

    result_chars: List[str] = []
    start = 0
    for i in range(k):
        # window end (exclusive) to leave room for remaining selections
        end_exclusive = n - (k - i) + 1
        window = bank[start:end_exclusive]
        if not window:
            raise ValueError("unable to find next digit; window empty")
        # find the maximum digit and its left-most index in the window
        max_digit = max(window)
        rel_idx = window.index(max_digit)
        abs_idx = start + rel_idx
        result_chars.append(max_digit)
        # next search starts after the chosen position
        start = abs_idx + 1

    return "".join(result_chars)


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
        res = process_bank(l, k=12)
        print(res)
        results.append(res)

    # Final output: sum of all returned results interpreted as integers
    int_sum = sum(int(r) for r in results)
    print(int_sum)
    # also return results (useful for tests)
    return results


if __name__ == "__main__":
    main()
