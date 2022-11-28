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
# <li><a class="reference external" href="https://docs.python.org/release/3.11.0/">Python 3.11.0</a>, documentation released on 24 October 2022.</li>
link = div.find("li")

# x.contents will be something like ['Python 3.11.0']
x = link.find("a", attrs={"href": re.compile("^https*://")})

# extract the latest version which will be something like '3.11.0'
matches = re.search("Python (.*)$", x.contents[0])
version = matches.group(1)
print(version)
