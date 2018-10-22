import requests
from bs4 import BeautifulSoup


def web_crawl(page, url):
    dom = requests.get(url).text
    soup = BeautifulSoup(dom, "html.parser")
    for n in soup.findAll('span', {'itemprop': 'name'}):
        name = n.get('content')
        print(name)


web_crawl(1, 'https://catalog.antiquorum.swiss/en/auctions/geneva-2011-03-27/lots')
