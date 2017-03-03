# coding=utf-8
import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from douban.items import DoubanItem
from scrapy.http import HtmlResponse
import re

class DoubanSpider(CrawlSpider):
    name = "douban"
    start_urls = ['http://movie.douban.com/top250']
    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        #首先将DobanItem()实例化成一个item对象
        item = DoubanItem()
        selector = Selector(response)
        #Movies为一个大信息块
        Movies = selector.xpath('//div[@class="item"]')

        #用for循环进行展开然后对每一个进行抓取
        for eachMoive in Movies:
            # 标题，电影名称
            moviename = eachMoive.xpath('div[@class="pic"]/a/img/@alt').extract()
            # //导演、演员、电影类型、国家、年代
            movieInfo = eachMoive.xpath('div[@class="info"]/div[@class="bd"]/p/text()').extract()
            #print type(movieInfo)
            #print movieInfo
            str1 = ''.join(movieInfo[0])
            #print str1
            str2 = ''.join(movieInfo[1])
            #print str2
            #有些电影没有显示主演wor
            if (str1.split("主演")):
                moviedirector = str1.split("主演:")[0].split("导演:")[1].strip()
            else:
                moviedirector = str1.split("导演:")[0]

            mode = re.compile(r'\d+')
            moviedate = mode.findall(str2)[0].strip()
            movielanuage = str2.split("/")[1].strip()
            movietype = str2.split("/")[2].strip()
            #评分、评价人数。
            moviestar = eachMoive.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            movierate = eachMoive.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[not(@class)]/text()').extract()
            #电影中的流行语
            moviedescription = eachMoive.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            # quote可能为空，因此需要先进行判断
            if moviedescription:
                #不为空就直接取第一个值（因为只有一个）
                moviedescription = moviedescription[0]
            else:
                moviedescription = "无"
            #给item赋值
            item['movie_name'] = moviename
            item['movie_director'] = moviedirector
            #item['movie_director'] = ';'.join(movieInfo)
            item['movie_lanuage'] = movielanuage
            item['movie_date'] = moviedate
            item['movie_star'] = moviestar
            item['movie_rate'] = movierate
            item['movie_description'] = moviedescription
            item['movie_type'] = movietype
            #将item提交
            yield item
            #提取下一页的link
            nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
            #nextlink不为空说明有下一页
            if nextLink:
                nextLink = nextLink[0]
                #print "下一页链接："
                print nextLink
                #构造下一页的链接
                yield Request(self.url + nextLink, callback = self.parse)
