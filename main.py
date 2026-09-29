import networkx as nx
import numpy as np
import subprocess
import sys
import asyncio
import csv
import os

SEQ_FILE = "distinct_R.seq"
LOG_FILE = "counter.log"
SPINNER = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

def log(s):
    with open(LOG_FILE, "a") as f:
        f.write(f"{s}\n")

def enumerate_graphs(n):
    proc = subprocess.Popen(
            ["geng", "-c", str(n)],
            stdout=subprocess.PIPE,
            text=True)
    next(proc.stdout)
    for line in proc.stdout:
        yield nx.from_graph6_bytes(line.strip().encode())

def resistance_matrix(G):
    n = G.number_of_nodes()
    L = nx.laplacian_matrix(G).astype(float).toarray()
    Lplus = np.linalg.pinv(L)
    d = np.diag(Lplus)
    return (d[:, None] + d[None, :] - 2 * Lplus)


def count_distinct_R(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    distinct = set()
    for i, G in enumerate(enumerate_graphs(n)):
        log(f"computing # of unique R vals for graph isomorphism class {i}")
        R = resistance_matrix(G)
        R_unique = np.unique(R.flatten())
        log(f"{len(R_unique)} distinct vals found")
        distinct = distinct.union(set(R_unique))
        log(f"current total: {len(distinct)}")
    return len(distinct)

async def spinner(task):
    i = 0
    while not task.done():
        sys.stdout.write("\033[?25l")  # hide cursor
        sys.stdout.write(f"\r{SPINNER[i % len(SPINNER)]} computing # of distinct R...\r")
        sys.stdout.flush()
        i += 1
        await asyncio.sleep(0.08)
    sys.stdout.write("\r✔ done                    \n")
    print("\033[?25h", end="")
    sys.stdout.flush()

async def run_count(n):
    loop = asyncio.get_running_loop()
    task = loop.run_in_executor(None, count_distinct_R, n)
    spin_task = asyncio.create_task(spinner(task))
    result = await task
    await spin_task
    return result

def load_existing():
    data = {}
    if not os.path.exists(SEQ_FILE):
        return data
    with open(SEQ_FILE, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            k, v = int(row[0]), row[1]
            data[k] = v
    return data

def write_sorted(data):
    with open(SEQ_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        for k in sorted(data):
            writer.writerow([k, data[k]])

def main():
    open(LOG_FILE, "w").close()
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <n>")
        sys.exit(1)
    log("reading command line arguments")
    n = int(sys.argv[1])
    log(f"read: n={n}")
    log("checking for existing sequence value")
    seq = load_existing()
    if n not in seq:
        log(f"n={n} not yet computed")
        log(f"computing sequence value for {n}")
        seq[n] = asyncio.run(run_count(n))
        log(f"value computed: [{n},{seq[n]}]")
        log("writing to sequence file")
        write_sorted(seq)
        log("done")
    else:
        log(f"n={n} already computed")

if __name__ == "__main__":
    main()
