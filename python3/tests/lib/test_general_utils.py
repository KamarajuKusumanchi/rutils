from lib.general_utils import in_chunks


def test_in_chunks():
    seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    size = 3
    expected = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10]]
    got = list(in_chunks(seq, size))
    assert got == expected, \
        'in_chunks is broken. got = {}, ' \
        'expected = {}'.format(got, expected)
