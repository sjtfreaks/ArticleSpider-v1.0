# -*- coding: utf-8 -*-

# Define your item pipelines here
#数据存储
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
class JsonWithEncodingPipeline(object):
    #打开json文件
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding ="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleexport.json','wb')
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value["path"]
            item["front_image_path"] = image_file_path
            return item

