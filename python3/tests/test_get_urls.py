from get_urls import get_urls


def test_get_urls():
    url = "https://news.ycombinator.com/item?id=25271676"
    urls = get_urls(url)
    nurls_got = len(urls)
    nurls_expected = 53
    assert (
        nurls_got == nurls_expected
    ), "Expecting {} urls but got {} urls instead".format(nurls_expected, nurls_got)
