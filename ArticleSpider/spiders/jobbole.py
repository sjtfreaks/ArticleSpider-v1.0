# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/113532/']

    def parse(self, response):
        #标题
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0].strip()
        #日期
        date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text() ').extract()[0].strip().replace("·","").strip()
        #点赞数
        praise_nums = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        #收藏数
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(".*(\d+).*",fav_nums)
        if match_re:
            #取数组中的第一个
            fav_nums = match_re.group(1)


        #评论数
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(".*(\d+).*",comment_nums)
        if match_re:
            # 取数组中的第一个
            fav_nums = match_re.group(1)

        #简介
        cotent = response.xpath("//div[@class='entry']").extract()[0]
        list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        #去重
        list = [element for element in list if not element.strip().endswtich("评论")]
        tags = ",".join(list)
        pass
