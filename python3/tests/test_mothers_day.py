import pytest

from mothers_day import get_mothers_day


@pytest.mark.parametrize('year, mdate_expected', [
    (2020, '2020-05-10'),
    (2021, '2021-05-09'),
    ('2022', '2022-05-08'),
    ('2023', '2023-05-14')
])
def test_get_mothers_day(year, mdate_expected):
    mdate_got = get_mothers_day(year)
    assert (
        mdate_got == mdate_expected
    ), "Expecting {} as mothers day but got {} instead".format(mdate_expected, mdate_got)
