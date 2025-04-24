import os

from get_urls import get_urls


def test_get_urls_count():
    url = "https://news.ycombinator.com/item?id=25271676"
    urls_got = get_urls(url)
    nurls_got = len(urls_got)
    nurls_expected = 54
    assert (
        nurls_got == nurls_expected
    ), "Expecting {} urls but got {} urls instead".format(nurls_expected, nurls_got)


def test_get_urls_text():
    url = "https://news.ycombinator.com/item?id=25271676"
    urls_got = get_urls(url)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(dir_path, "data")
    fname = os.path.join(data_dir, "urls_hn_25271676.txt")
    with open(fname, "r") as fh:
        urls_expected = [line.rstrip() for line in fh]
    assert urls_got == urls_expected, "urls do not match"
