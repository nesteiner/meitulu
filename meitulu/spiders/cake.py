import scrapy
from scrapy import Spider
from meitulu.items import Image
import re
class CakeSpider(Spider):
    name = "cake"

    def __init__(self, start_url=None, album_name=None, *args, **kwargs):
        if start_url == None:
            raise Exception("usage: -a start_url=...")
        elif album_name == None:
            raise Exception("usage: -a album_name=...")
        else:
            super(Spider, self).__init__(*args, **kwargs)
            self.start_url = start_url
            self.album_name = album_name

    def start_requests(self):
        yield scrapy.Request(url = self.start_url, callback=self.parse, cb_kwargs=dict(count = 1))

    def parse(self, response, **kwargs):
        count = kwargs.get("count")
        urls = response.css("div.container-inner-fix-m img::attr(src)").extract()
        image_urls = list(map(lambda url: response.urljoin(url), urls))

        for url in image_urls:
            name = str(count) + ".jpg"
            yield Image(url=url, name=name, album_name=self.album_name, from_url=response.url)
            count += 1

        anchors = response.css("div.container ul.pagination li a.page-link").extract()
        pages = response.css("div.container ul.pagination li a.page-link::attr(href)").extract()

        next_page_anchor = anchors[-1]
        pattern = re.compile(r"href")

        if re.search(pattern, next_page_anchor) != None:
            next_page = response.urljoin(pages[-1])
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                cb_kwargs=dict(count=count+1))
