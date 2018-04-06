import urllib
import re
from bs4 import BeautifulSoup
from random import randint

JOKES = [
    "What did the bee say to the flower?  Hi, honey.",
    "What do two oceans do when they meet? Nothing! Just wave",
    "What do you call a old snowman? Water.",
    "What's the richest kind of air? Billionaire.",
    "If God didn't want us to eat animals, he wouldn't have made them out of food.",
    "I went to buy some camouflage trousers the other day but I couldn't find any..",
    # "I bought some shoes from a drug dealer. I don't know what he laced them with, but I've been tripping all day.",
    "I told my girlfriend she drew her eyebrows too high. She seemed surprised.",
    "I couldn't figure out why the baseball kept getting larger. Then it hit me.",
    "What do you call a fake noodle? An Impasta",
    "How do you make an octopus laugh? With ten-tickles",
    "My friend thinks he is smart. He told me an onion is the only food that makes you cry, so I threw a coconut at his face.",
    "I’ve just written a song about tortillas; actually, it’s more of a rap.",
]

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

def getCleanJoke():
    index = randint(0, len(JOKES) - 1)
    return JOKES[index]

