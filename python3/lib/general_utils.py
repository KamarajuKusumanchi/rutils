import psutil


def worker_count(keep_free=1):
    """
    The idea here is to get the number of worker processes that can be
    started while keeping some resources free. The total number of
    resources is assumed to be the logical cpu count (physical cores *
    number of hyper threads)
    :param keep_free: Number of resources to be kept free
    :return: workers to use
    """
    available = psutil.cpu_count()
    if available > keep_free:
        available -= keep_free
    return available


def in_chunks(seq, size):
    """
    Return sequence in 'chunks' of size defined by size
    """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


if __name__ == '__main__':
    workers_available = worker_count()
    print('workers available = ', workers_available)
