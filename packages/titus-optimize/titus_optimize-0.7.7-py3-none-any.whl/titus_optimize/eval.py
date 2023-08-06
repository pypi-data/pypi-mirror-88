from collections import Counter

import numpy as np

class SolutionStatistics:
    def __init__(self, res, weights, k, c, n, b):
        self.usage_per_core = np.full(c, np.nan, dtype=np.float32)
        self.usage_per_socket = np.full(n, np.nan, dtype=np.float32)
        if weights is not None:
            for l in range(c):
                s = 0.0
                for j, alloc in enumerate(res):
                    if alloc[2 * l] == 1:
                        s += weights[j]
                    if alloc[2 * l + 1] == 1:
                        s += weights[j]
                if s > 0:
                    self.usage_per_core[l] = s

            
            for t in range(n):
                s = 0.0
                for j, alloc in enumerate(res):
                    for u in range(t * b, (t + 1) * b):
                        if alloc[u] == 1:
                            s += weights[j]
                if s > 0:
                    self.usage_per_socket[t] = s

        self.num_xsockets = 0
        for j, alloc in enumerate(res):
            num_sockets = 0
            for t in range(n):
                num_sockets += np.sum(alloc[t * b : (t+1) * b]) > 0
            if num_sockets > 1:
                self.num_xsockets += 1
        self.num_workloads = len(res)
    
        self.num_numa_violations = number_numa_violations(res, n)
        self.num_empty_cores = number_empty_cores(res)
        self.num_full_cores = number_full_cores(res)


    def __str__(self):
        return str(vars(self))

def number_numa_violations(allocations, num_sockets):
    d = len(allocations[0])
    b = d // num_sockets

    violations = 0
    for job in allocations:
        cnt = Counter()
        for ii, e in enumerate(job):
            if e == 1:
                cnt[ii // b] += 1
        top_index = cnt.most_common()[0][0]
        violations += sum(v for k, v in cnt.items() if k != top_index)
    return violations


def number_empty_sockets(allocations, num_sockets):
    d = len(allocations[0])
    b = d // num_sockets
    empty = [True] * num_sockets
    for a in allocations:
        for i, v in enumerate(a):
            empty[i // b] &= v == 0
    return sum(empty)


def number_empty_cores(allocations):
    d = len(allocations[0])
    c = d // 2
    empty = [True] * c
    for a in allocations:
        for i, v in enumerate(a):
            empty[i // 2] &= v == 0
    return sum(empty)


def number_full_cores(allocations):
    d = len(allocations[0])
    c = d // 2
    full = [0] * c
    for a in allocations:
        for i, v in enumerate(a):
            full[i // 2] += v
    return sum([1 if e == 2 else 0 for e in full])
