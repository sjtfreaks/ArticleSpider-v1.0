# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    #start_urls = ['http://blog.jobbole.com/113532/']  获取指定文章
    start_urls = ['http://blog.jobbole.com/all-posts/']
    def parse(self, response):
        #获取文章列表页URL并交给解析函数进行具体字段的解析
        #获取下一页的URl并交给scrapy进行下载，下载完成后交给parse
        #提取了所有的URL
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            #request.url + post_urls  当不存在域名时
            #request(url = post_url,callback = self.parse_detail())
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url),meta={"front_image_url":image_url}, callback=self.parse_detail)
            #print(post_url)
            #提取下一页并下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url), callback=self.parse)


    def parse_detail(self,response):   #提取文章的具体数据
        article_item = JobBoleArticleItem()

        # #标题
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0].strip()
        # #日期
        # date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text() ').extract()[0].strip().replace("·","").strip()
        # #点赞数
        #praise_nums = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        # #收藏数
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*",fav_nums)
        # if match_re:
        #     #取数组中的第一个
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        #
        # #评论数
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*",comment_nums)
        # if match_re:
        #     # 取数组中的第一个
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # #简介
        # content = response.xpath("//div[@class='entry']").extract()[0]
        # list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # #去重复
        # list = [element for element in list if not element.strip().endswith("评论")]
        # tags = ",".join(list)

        #通过css选择器提取字段
        #文章封面图
        front_image_url = response.meta.get("front_image_url","")
        title =  response.css(".entry-header h1::text").extract()[0]
        date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip()
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        fav_nums = response.css("span.bookmark-btn::text").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            # 取数组中的第一个
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums =  response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            # 取数组中的第一个
            comment_nums =int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.css("div.entry").extract()[0]

        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()[0]
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        article_item["title"] = title
        article_item["url"] = response.url
        article_item["date"] = date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["content"] = content
        article_item["url_object_id"] = get_md5(response.url)

        yield article_item
