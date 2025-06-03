# tags | distribute N element array over p workers, break array into smaller
# chunks

import pandas as pd


def partition_tasks(N, p):
    """
    The idea here is to uniformly partition N tasks over p workers
    by breaking a hypothetical N element array into p contiguous chunks.
    When N is divisible by p, each chunk will have equal number of tasks.
    When N is not divisible by p, the first N modulo(p) tasks have one
    extra task.

    It returns a Series with p+1 elements corresponding to the
    partition boundaries.

    Example: For N=13, p=4 the return Series is [0,4,7,10,13] which means
    the partitions are [0:4], [4:7], [7:10], [10:13]
    :param N: positive integer
    :param p: positive integer
    :return: a pd.Series with p+1 elements
    """
    quotient = int(N / p)
    remainder = N % p
    nelem = pd.Series([quotient] * p)
    nelem[0:remainder] += 1
    partitionIndex = pd.Series([0]).append(nelem.cumsum(), ignore_index=True)
    return partitionIndex


if __name__ == "__main__":
    N = 12
    p = 4
    a = partition_tasks(N, p)
    assert a.equals(
        pd.Series([0, 3, 6, 9, 12])
    ), "partition_tasks returned unexpected results for N = %d, p = %d" % (N, p)

    N = 13
    p = 4
    a = partition_tasks(N, p)
    assert a.equals(
        pd.Series([0, 4, 7, 10, 13])
    ), "partition_tasks returned unexpected results for N = %d, p = %d" % (N, p)

    N = 14
    p = 4
    a = partition_tasks(N, p)
    assert a.equals(
        pd.Series([0, 4, 8, 11, 14])
    ), "partition_tasks returned unexpected results for N = %d, p = %d" % (N, p)

    N = 15
    p = 4
    a = partition_tasks(N, p)
    assert a.equals(
        pd.Series([0, 4, 8, 12, 15])
    ), "partition_tasks returned unexpected results for N = %d, p = %d" % (N, p)

    N = 16
    p = 4
    a = partition_tasks(N, p)
    assert a.equals(
        pd.Series([0, 4, 8, 12, 16])
    ), "partition_tasks returned unexpected results for N = %d, p = %d" % (N, p)
