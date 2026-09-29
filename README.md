# ER Counter

Computational enumeration of distinct effective resistance values in connected graphs.

## Overview

For a connected graph $G$, the **effective resistance** $R_G(u,v)$ measures the electrical resistance between vertices $u$ and $v$ when every edge is treated as a unit resistor.

This project asks:

> **How many distinct effective resistance values occur among all connected graphs on $n$ vertices?**

Define

$$
D_n =
\bigcup_{\substack{G\text{ connected}\\|V(G)|=n}}
\{R_G(u,v) : u,v\in V(G)\},
$$

and let

$$
d(n)=|D_n|.
$$

`er-counter` computes $d(n)$ by enumerating connected unlabeled graphs and collecting the effective resistance values that occur in each graph.

## Current Results

The computation currently gives:

| $n$ | $d(n)$ |
|---:|---:|
| 1 | 0 |
| 2 | 1 |
| 3 | 3 |
| 4 | 36 |
| 5 | 190 |
| 6 | 1,450 |
| 7 | 14,905 |
| 8 | 287,573 |
| 9 | 10,262,122 |

The rapid growth of the sequence makes exhaustive computation increasingly expensive as $n$ increases.

## Method

For each value of `n`:

1. `geng` enumerates all connected unlabeled graphs on `n` vertices.
2. Each graph is converted to its Laplacian matrix.
3. The Moore–Penrose pseudoinverse of the Laplacian is computed.
4. The effective resistance between every pair of vertices is computed.
5. The distinct resistance values are added to the global set.
6. The resulting count is written to `distinct_R.seq`.

For a graph $G$ with Laplacian $L$, effective resistance is computed using the
Moore–Penrose pseudoinverse $L^+$:

$$
R_G(u,v) =
L^+_{uu} + L^+_{vv} - 2L^+_{uv}.
$$

Graph isomorphism classes are enumerated using
[`nauty`](https://pallini.di.uniroma1.it/), avoiding redundant computation over
isomorphic labeled graphs.

## Usage

### Requirements

- Python 3.8+
- NumPy
- NetworkX
- [`nauty`](https://pallini.di.uniroma1.it/) with `geng` available on `PATH`

Verify that `geng` is available with:

```bash
which geng
```

### Run

Compute the value for a particular $n$:

```bash
python3 main.py n
```

For example:

```bash
python3 main.py 9
```

If $d(9)$ has not already been computed, the program enumerates the connected graphs on 9 vertices and updates `distinct_R.seq`.

Previously computed values are retained, so individual values can be computed incrementally.

## Output

Results are stored in `distinct_R.seq` as:

```text
1,0
2,1
3,3
4,36
5,190
6,1450
7,14905
8,287573
9,10262122
```

The file is maintained in increasing order of \(n\), and existing values are not recomputed.

## Implementation

The current implementation is intentionally small.

- `main.py` — graph enumeration, effective-resistance computation, sequence management, and experiment logging.
- `distinct_R.seq` — accumulated sequence of computed values.

The effective resistance calculation uses the graph Laplacian and its numerical pseudoinverse via NumPy.

## Reproducibility

The computation is deterministic for a fixed $n$: `geng` provides the graph enumeration and no random sampling is used.

Because effective resistances are currently computed using floating-point linear algebra, numerical equality is determined by the resulting floating-point values. Exact-arithmetic validation is a potential direction for future work.

## Research Context

This computation is related to my work on graph inference from effective resistance measurements and the information contained in resistance-distance data.

For the corresponding research, see:

**Graph Inference with Effective Resistance Queries**

[Paper](https://proceedings.mlr.press/v313/warton26a.html)

## Status

This is a research/computational experiment rather than a production software package.

The primary purpose of the project is to explore the combinatorial structure of effective resistance values across graphs and to generate data for further mathematical investigation.
