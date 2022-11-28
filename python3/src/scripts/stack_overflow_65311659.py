# This script gives the latest python version number only.
# This is to address
# https://stackoverflow.com/questions/65311659/getting-the-latest-python-3-version-programmatically
#
# Most likely, you may want to use the release_history.py instead of this.
# That script is more generic in the sense that it can give the entire python
# release history with release dates and version numbers in a dataframe. For
# example
#
# $ ./release_history.py python --limit 5
#       date    tag
# 2022-10-24 3.11.0
# 2022-10-08 3.10.8
# 2022-09-06 3.10.7
# 2022-08-08 3.10.6
# 2022-06-06 3.10.5
#
# compare this with
#
# $ python stack_overflow_65311659.py
# 3.11.0

import requests
from bs4 import BeautifulSoup
import re

url = "https://www.python.org/doc/versions/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Search for
# <div class="section" id="python-documentation-by-version">
# ...
# </div>
div = soup.find("div", attrs={"id": "python-documentation-by-version"})

# Get the first link. It will be something like
# <li><a class="reference external" href="https://docs.python.org/release/3.11.0/">Python 3.11.0</a>,
#  documentation released on 24 October 2022.</li>
link = div.find("li")

# x.contents will be something like ['Python 3.11.0']
x = link.find("a", attrs={"href": re.compile("^https*://")})

# extract the latest version which will be something like '3.11.0'
matches = re.search("Python (.*)$", x.contents[0])
version = matches.group(1)
print(version)
