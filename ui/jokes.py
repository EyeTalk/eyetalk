import urllib
import re
from bs4 import BeautifulSoup


def getJoke():
    urlToRead = "http://www.jokesyou.com"
    handle = urllib.request.urlopen(urlToRead)
    htmlGunk = handle.read()
    soup = BeautifulSoup(htmlGunk, "html.parser")
    joke = soup.findAll('div', {'class': 'right'})[0].findAll('p')[0]
    joke = str(joke)
    # Regex replace
    joke = re.sub(r'<p>', r'', joke)
    joke = re.sub(r'</p>|<br/>', r'\n', joke)
    return joke
