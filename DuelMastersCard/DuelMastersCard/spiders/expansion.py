import dataclasses
import logging

import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import DuelmasterscardItem


@dataclasses.dataclass()
class Expansion:
    expansion: str = ""
    rarity: str = ""
    number: str = ""
    foil: str = ""
    flavor: str = ""
    drawer: str = ""


class ExpansionSpider(CrawlSpider):
    name = "expansion"
    allowed_domains = ["dmvault.ath.cx"]
    start_urls = [
        "https://dmvault.ath.cx/card/?cardtype=%E3%81%99%E3%81%B9%E3%81%A6&civilization=%E3%81%99%E3%81%B9%E3%81%A6&race=%E3%81%99%E3%81%B9%E3%81%A6&power=%E3%81%99%E3%81%B9%E3%81%A6&cost=%E3%81%99%E3%81%B9%E3%81%A6&pks__filter=&expansion=&cardname=&status=&sortby=%E3%81%AA%E3%81%97"
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
    )

    def parse_item(self, response):
        name = response.xpath("//h1/text()")[0].get()

        detail_table = response.xpath('//*[@id="pane0"]/div[1]/div/div[1]/div/table')
        type = detail_table.xpath("//tr/td/text()")[0].get()
        civilization = detail_table.xpath("//tr/td/text()")[1].get()
        tribe = detail_table.xpath("//tr/td/text()")[2].get()
        power = detail_table.xpath("//tr/td/text()")[3].get()
        cost = detail_table.xpath("//tr/td/text()")[4].get()
        effect = detail_table.xpath("//tr/td/text()")[5].get()

        expansion_details = response.xpath(
            '//*[@id="pane0"]/div[1]/div/div[1]/div/form/div/div/table//tr/td'
        )

        collections = []
        collection = Expansion(expansion="", rarity="", number="", flavor="")
        for i, detail in enumerate(expansion_details):
            detail_bs = BeautifulSoup(detail.get(), "lxml").text
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
        item["name"] = name
        item["type"] = type
        item["civilization"] = civilization
        item["tribe"] = tribe
        item["cost"] = cost
        item["power"] = power
        item["effect"] = effect
        item["collections"] = collections

        yield item
