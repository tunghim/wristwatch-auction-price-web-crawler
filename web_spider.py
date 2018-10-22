from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        "webui": {
            "username": "admin",
            "password": "password",
            "need-auth": True
        }
    }

    def on_start(self):
        self.crawl('https://catalog.antiquorum.swiss/en/auctions/geneva-2011-03-27/lots?action=index&auction_id=geneva-2011-03-27&controller=lots&locale=en&page=1&per_page=100', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
