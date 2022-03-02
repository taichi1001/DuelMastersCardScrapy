from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from ..items import Card, DuelmasterscardItem, Recording


class ExpansionSpider(CrawlSpider):
    name = "expansion"
    allowed_domains = ["dmvault.ath.cx"]
    start_urls = [
        "https://dmvault.ath.cx/card/?cardtype=%E3%81%99%E3%81%B9%E3%81%A6&civilization=%E3%81%99%E3%81%B9%E3%81%A6&race=%E3%81%99%E3%81%B9%E3%81%A6&power=%E3%81%99%E3%81%B9%E3%81%A6&cost=%E3%81%99%E3%81%B9%E3%81%A6&pks__filter=&expansion=&cardname=&status=&sortby=%E3%81%AA%E3%81%97",
    ]

    rules = (
        # 一覧ページから個別ページへ遷移するルール
        Rule(
            LinkExtractor(
                deny=(
                    r".*/decks.html",
                    r".*/evaluations.html",
                    r".*/combos.html",
                    r".*/faqs.html",
                    r".*/links.html",
                ),
                restrict_xpaths=[
                    '//*[@class="table-responsive"]',
                ],
            ),
            callback="parse_item",
            follow=False,
        ),
        # 一覧ページから次一覧ページへ遷移するルール
        Rule(
            LinkExtractor(allow=(r".*?offset=",)),
        ),
    )

    def parse_item(self, response):
        names = response.xpath("//h1/text()")[0].get().split("／")
        cards = []
        detail_tables = response.xpath('//*[@id="pane0"]/div[1]/div/div[1]/div/table')
        for i, detail_table in enumerate(detail_tables):
            card = ItemLoader(item=Card())
            detail_table = BeautifulSoup(detail_table.get(), "lxml").find_all("td")
            card.add_value("name", names[i])
            card.add_value("type", detail_table[0].text)
            card.add_value("civilization", detail_table[1].text)
            card.add_value("tribe", detail_table[2].text)
            card.add_value("power", detail_table[3].text)
            card.add_value("cost", detail_table[4].text)
            card.add_value("effect", detail_table[5].text)
            cards.append(card.load_item())

        expansion_details = response.xpath(
            '//*[@id="pane0"]/div[1]/div/div[1]/div/form/div/div/table//tr/td'
        )
        collections = []
        collection = ItemLoader(item=Recording())
        for i, detail_table in enumerate(expansion_details):
            detail_bs = BeautifulSoup(detail_table.get(), "lxml").text
            if i % 7 == 0:
                collection = ItemLoader(item=Recording())
            if i % 7 == 1:
                collection.add_value("expansion", detail_bs)
            if i % 7 == 2:
                collection.add_value("rarity", detail_bs)
            if i % 7 == 3:
                collection.add_value("number", detail_bs)
            if i % 7 == 4:
                collection.add_value("foil", detail_bs)
            if i % 7 == 5:
                collection.add_value("flavor", detail_bs)
            if i % 7 == 6:
                collection.add_value("drawer", detail_bs)
                collections.append(collection.load_item())

        item = ItemLoader(item=DuelmasterscardItem())
        item.add_value("cards", cards)
        item.add_value("collections", collections)

        yield item.load_item()
