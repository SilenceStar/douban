# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field

class DoubanItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = Field()#名字
    movie_director = Field()#导演
    movie_lanuage = Field()#语言
    movie_date = Field()#上映时间
    movie_star = Field()#评分
    movie_rate = Field()#参与投票的人数
    movie_type = Field()#电影类型
    movie_description = Field()#描述
