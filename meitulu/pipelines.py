# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging, os, scrapy

# class MeituluPipeline:
#     logger = logging.getLogger()

#     def process_item(self, item, spider):
#         self.logger.info('albumName: {}'.format(item['albumName']))
#         self.logger.info('url: {}'.format(item['url']))
#         self.logger.info('name: {}'.format(item['name']))
#         self.logger.info('from: {}'.format(item['fromUrl']))

from scrapy.pipelines.images import FilesPipeline

class MeituluPipeline(FilesPipeline):
    default_headers = {
        'Accept': 'image/avif,image/webp,*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Host': 'image.meitulu.cn',
        'Referer': 'http://meitulu.cn/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0'
    }
    
    def file_path(self, request, response=None, info=None, *, item=None):
        dirname = item['albumName']
        basename = item['name']
        
        return os.path.join(dirname, basename)

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'], headers=self.default_headers)

    def item_completed(sefl, results, item, info):
        return item