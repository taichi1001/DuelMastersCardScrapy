# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
from dataclasses import dataclass

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst


def rm_ideographic_space(value):
    return value.strip("\u3000")


def split_slash(value):
    return value.split("/")


def split_effect(value):

    value = value.split("■")
    if len(value) != 1:
        del value[0]
    return value


def make_expansion(value):
    date = value[:5]
    expansion = value[6:]
    regex_result = re.findall("[A-Z]*-\\S*", expansion)
    if regex_result:
        id = regex_result[0]
        name = rm_ideographic_space(expansion.lstrip(id + " "))
    else:
        id = ""
        name = rm_ideographic_space(expansion)
    return Expansion(id=id, date=date, name=name)


class Card(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(rm_ideographic_space),
    )
    type = scrapy.Field(
        input_processor=MapCompose(rm_ideographic_space, split_slash),
    )
    civilization = scrapy.Field(
        input_processor=MapCompose(rm_ideographic_space, split_slash),
    )
    tribe = scrapy.Field(
        input_processor=MapCompose(rm_ideographic_space, split_slash),
    )
    cost = scrapy.Field(
        input_processor=MapCompose(rm_ideographic_space),
    )
    power = scrapy.Field(
        input_processor=MapCompose(rm_ideographic_space),
    )
    effect = scrapy.Field(
        input_processor=MapCompose(rm_ideographic_space, split_effect),
    )


@dataclass
class Expansion:
    id: str
    date: str
    name: str


class Recording(scrapy.Item):
    expansion = scrapy.Field(
        input_processor=MapCompose(make_expansion),
    )
    rarity = scrapy.Field()
    number = scrapy.Field()
    foil = scrapy.Field()
    flavor = scrapy.Field()
    drawer = scrapy.Field()


class DuelMastersCardItem(scrapy.Item):
    name = scrapy.Field()
    collections = scrapy.Field()
    cards = scrapy.Field()
