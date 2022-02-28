# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass


@dataclass
class Card:
    name: str = ""
    type: str = ""
    civilization: str = ""
    tribe: str = ""
    cost: str = ""
    power: str = ""
    effect: str = ""


@dataclass
class Expansion:
    expansion: str = ""
    rarity: str = ""
    number: str = ""
    foil: str = ""
    flavor: str = ""
    drawer: str = ""


class DuelmasterscardItem(scrapy.Item):
    collections = scrapy.Field()
    cards = scrapy.Field()
