import scrapy
import json
import requests
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "wristwatch_auction_price_web_crawler"
    start_urls = [
        'https://catalog.antiquorum.swiss/en/auctions/geneva-2011-03-27/lots',
    ]

    def parse(self, response):
        listing_page_res = self.listing_page(response)
        for i in listing_page_res:
            detail_page_dom = requests.get(
                'https://catalog.antiquorum.swiss' + i['lot_detail_page']).text
            detail_page_soup = BeautifulSoup(detail_page_dom, "html.parser")
            detail_page_res = self.detail_page(detail_page_soup)
            for i in detail_page_res:
                yield i

        # # Navigate to next page.
        # next_page = response.css('span.next a::attr("href")').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

    def listing_page(self, response):
        res = []
        for i in response.css('div.col-md-3'):
            if i.css('div#lot_number > h2::text').extract_first() is not None:
                res.append({
                    'lot_number': i.css('div#lot_number > h2::text').extract_first(),
                    'lot_price': i.css('div.lots_price > p::text').extract_first(),
                    'lot_detail_page': i.css('div.lots_thumbail a::attr("href")').extract_first()
                })

        return res

    def detail_page(self, soup):
        res = []
        res.append({
            'type': soup.h3.get_text().strip()
        })

        return res
