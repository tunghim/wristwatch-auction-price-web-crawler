import requests
from bs4 import BeautifulSoup


def web_crawl(page, url):
    dom = requests.get(url).text
    dom_str = BeautifulSoup(dom, "html.parser")
    for link in dom_str.findAll('span', {'itemprop': 'name'}):
        description = link.get('content')
        print(description)


web_crawl(1, 'https://catalog.antiquorum.swiss/en/auctions/geneva-2011-03-27/lots?action=index&auction_id=geneva-2011-03-27&controller=lots&locale=en&page=1&per_page=100')
