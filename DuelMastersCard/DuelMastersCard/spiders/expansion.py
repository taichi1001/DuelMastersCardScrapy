import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Card, DuelmasterscardItem, Expansion


class ExpansionSpider(CrawlSpider):
    name = "expansion"
    allowed_domains = ["dmvault.ath.cx"]
    start_urls = [
        "https://dmvault.ath.cx/card/?cardtype=%E3%81%99%E3%81%B9%E3%81%A6&civilization=%E3%81%99%E3%81%B9%E3%81%A6&race=%E3%81%99%E3%81%B9%E3%81%A6&power=%E3%81%99%E3%81%B9%E3%81%A6&cost=%E3%81%99%E3%81%B9%E3%81%A6&pks__filter=&expansion=&cardname=&status=&sortby=%E3%81%AA%E3%81%97",
    ]

    rules = (
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
        Rule(
            LinkExtractor(allow=(r".*?offset=",)),
        ),
    )

    def parse_item(self, response):
        names = response.xpath("//h1/text()")[0].get().split("／")
        print(names)
        cards = []
        detail_tables = response.xpath('//*[@id="pane0"]/div[1]/div/div[1]/div/table')
        for i, details in enumerate(detail_tables):
            details_bs = BeautifulSoup(details.get(), "lxml")
            type = details_bs.find_all("td")[0].text.split()
            civilization = details_bs.find_all("td")[1].text.split()
            tribe = details_bs.find_all("td")[2].text.split()
            power = details_bs.find_all("td")[3].text.split()
            cost = details_bs.find_all("td")[4].text.split()
            effect = details_bs.find_all("td")[5].text.split()
            cards.append(
                Card(
                    name=names[i].split(),
                    type=type,
                    civilization=civilization,
                    tribe=tribe,
                    power=power,
                    cost=cost,
                    effect=effect,
                )
            )

        expansion_details = response.xpath(
            '//*[@id="pane0"]/div[1]/div/div[1]/div/form/div/div/table//tr/td'
        )

        collections = []
        collection = Expansion(expansion="", rarity="", number="", flavor="")
        for i, detail in enumerate(expansion_details):
            detail_bs = BeautifulSoup(detail.get(), "lxml").text.split()
            if i % 7 == 0:
                pass
            if i % 7 == 1:
                collection.expansion = detail_bs
            if i % 7 == 2:
                collection.rarity = detail_bs
            if i % 7 == 3:
                collection.number = detail_bs
            if i % 7 == 4:
                collection.foil = detail_bs
            if i % 7 == 5:
                collection.flavor = detail_bs
            if i % 7 == 6:
                collection.drawer = detail_bs
                collections.append(collection)

        item = DuelmasterscardItem()
        item["cards"] = cards
        item["collections"] = collections

        yield item
