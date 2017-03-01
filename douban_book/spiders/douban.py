# -*- coding: utf-8 -*-
import scrapy
from douban_book.items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["book.douban.com"]
    start_urls = ['https://book.douban.com/top250']

    def parse(self, response):
        bList = '//tr[@class="item"]'
        for con in response.xpath(bList):
            item = DoubanItem()
            bName = con.xpath('td/div[@class="pl2"]/a/@title').extract()
            # bName = bName.replace(' ','').replace('\n','')
            item['bookName'] = bName
            item['bookUrl'] = con.xpath('td/div[@class="pl2"]/a/@href').extract()
            bRate =  con.xpath('td/div[@class="star clearfix"]/span/text()').extract()[0]
            bRate = bRate.replace(' ','').replace('\n','')
            item['bookRate'] = bRate 
            item['bookDes'] = con.xpath('td/p[@class="quote"]/span/text()').extract()
            yield item

            nextPage = response.xpath('//span[@class="next"]/link/@href').extract()
            if nextPage:
                next = nextPage[0]
                yield scrapy.http.Request(next,callback=self.parse)
