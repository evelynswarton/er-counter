# ER Counter

## Overview

main.py computes a the number of distinct effective resistance values for all graphs of size n and maintains a persistent record of computed values in distinct_R.seq.

Each run:

* computes number of distinct ER values d(n) for all graphs of size n
* appends n, d(n) to distinct_R.seq
* only if n is not already present
* keeps entries sorted by n

---

## Requirements

* Python 3.8+
* Program `geng` installed and available on PATH

To verify:

which geng

If this fails or gives an alias, ensure geng is installed and exported to your environment path.

---

## Usage

Run for a single value:

python3 main.py n

Example:

python3 main.py 10

This will:

* compute d(10)
* update distinct_R.seq if 10 is not already recorded

---

## Output File: distinct_R.seq

A simple CSV-style file:

n,d(n)
1,0
2,1
3,2
...

* Automatically created if it does not exist
* Kept sorted in ascending order of n
* Duplicate n entries are ignored


