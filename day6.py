#!/usr/bin/env python3
"""
day6.py

Read a file where the last line contains N operator symbols (non-whitespace),
and the preceding lines contain rows of N numbers separated by whitespace.

We compute N partial results. For each column i we apply the operator symbols[i]
between the partial result and each number in column i, in the order of rows.
Operators supported: +, -, *, / (integer division). Partial results start at 0
for + and - (0), and 1 for * and / to make sense.

Finally print each partial and the final sum of partials.
"""
from __future__ import annotations
from pathlib import Path
import sys
from typing import List


def parse_operators(line: str) -> List[str]:
    return [ch for ch in line if not ch.isspace()]


def apply_op(acc: int, op: str, value: int) -> int:
    if op == "+":
        return acc + value
    if op == "-":
        return acc - value
    if op == "*":
        return acc * value
    if op == "/":
        # integer division, protect division by zero
        return acc // value if value != 0 else acc
    raise ValueError(f"Unsupported op: {op}")


def main(argv: List[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    path = argv[0] if argv else "day6-sample.txt"
    p = Path(path)
    if not p.exists():
        print(f"Input file {p} not found")
        return

    lines = [l.rstrip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(lines) < 2:
        print("Need at least one data line and one operator line")
        return

    op_line = lines[-1]
    ops = parse_operators(op_line)
    N = len(ops)

    # initialize partials: for +,- start at 0; for *,/ start at 1
    partials = []
    for op in ops:
        if op in ("+", "-"):
            partials.append(0)
        elif op in ("*", "/"):
            partials.append(1)
        else:
            raise ValueError(f"Unsupported operator {op}")

    # process data lines
    for data_line in lines[:-1]:
        parts = data_line.split()
        if len(parts) != N:
            raise ValueError(f"Expected {N} numbers per line, got {len(parts)}: {data_line!r}")
        for i, tok in enumerate(parts):
            val = int(tok)
            partials[i] = apply_op(partials[i], ops[i], val)

    for pval in partials:
        print(pval)
    print(sum(partials))


if __name__ == "__main__":
    main()
