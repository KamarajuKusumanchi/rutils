# tags | distribute N element array over p workers, break array into smaller
# chunks

import pandas as pd

def partition_tasks(N, p):
    '''
    The idea here is to uniformly partition N tasks over p workers
    by breaking a hypothetical N element array into p contiguous chunks.
    When N is divisible by p, each chunk will have equal number of tasks.
    When N is not divisible by p, the first N modulo(p) tasks have one
    extra task.

    It returns a Series with p+1 elements corresponding to the
    partition boundaries.

    Example: For N=13, p=4 the return Series is [0,4,7,10,13] which means
    the partitions are [0:4], [4:7], [7:10], [10:13]
    :param N:
    :param p:
    :return:
    '''
    # assume N >0, p>0
    quotient = int(N/p)
    remainder = N % p
    nelem = pd.Series([quotient]* p)
    nelem[0:remainder] += 1
    partitionIndex = pd.Series([0]).append(nelem.cumsum(), ignore_index=True)
    return partitionIndex

a = partition_tasks(12, 4)
print(a)
a = partition_tasks(13, 4)
print(a)
a = partition_tasks(14, 4)
print(a)
a = partition_tasks(15, 4)
print(a)
a = partition_tasks(16, 4)
print(a)